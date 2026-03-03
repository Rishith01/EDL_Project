import serial
import time
import math
import threading
from enum import Enum
from master_config import *


class MotorDirection(Enum):
    FORWARD = 1
    REVERSE = 0
    STOP = 2


class MotorController:

    def __init__(self, uart_port="/dev/serial0", baudrate=115200):

        self.serial = serial.Serial(
            port=uart_port,
            baudrate=baudrate,
            timeout=0.1
        )

        self.motor_speeds = [0] * NUM_MOTORS
        self.motor_directions = [MotorDirection.STOP] * NUM_MOTORS

        self.encoder_values = [0] * NUM_MOTORS
        self.limit_switches = [False] * NUM_LIMIT_SWITCHES

        self.forward_history = []

        self.control_thread = None
        self.running = False

    # ------------------------------------------------
    # UART COMMUNICATION
    # ------------------------------------------------

    def _send_motor_packet(self, motor_id, direction, speed_value):
        speed_value = int(speed_value)

        packet = bytearray()
        packet.append(0xAA)
        packet.append(motor_id)
        packet.append(direction.value)
        packet.append((speed_value >> 8) & 0xFF)
        packet.append(speed_value & 0xFF)

        checksum = sum(packet) & 0xFF
        packet.append(checksum)

        self.serial.write(packet)

    def _request_status(self):
        self.serial.write(b'\xCC')  # status request byte

        if self.serial.in_waiting > 0:
            data = self.serial.read(64)
            if len(data) > 0 and data[0] == 0xBB:
                # parse encoder values
                idx = 1
                for i in range(NUM_MOTORS):
                    self.encoder_values[i] = (data[idx] << 8) | data[idx + 1]
                    idx += 2

                # parse limit switches
                for i in range(NUM_LIMIT_SWITCHES):
                    self.limit_switches[i] = bool(data[idx] & (1 << i))

    # ------------------------------------------------
    # MOTOR CONTROL
    # ------------------------------------------------

    def set_motor_speed(self, motor_id, speed, direction):

        if not 0 <= motor_id < NUM_MOTORS:
            return

        pwm_value = int(speed * PWM_MAX_VALUE)

        self.motor_speeds[motor_id] = pwm_value
        self.motor_directions[motor_id] = direction

        self._send_motor_packet(motor_id, direction, pwm_value)

    # ------------------------------------------------
    # HIGH-LEVEL CONTROL LOGIC (UNCHANGED)
    # ------------------------------------------------

    def process_direction_command(self, direction_or_angle, speed, forward=None):

        if forward is None:
            angle = direction_or_angle
            speed_val = speed
            forward = max(0.0, 1.0 - speed_val)

            angle_deg = math.degrees(angle) % 360
            if 45 <= angle_deg < 135:
                direction = 'up'
            elif 135 <= angle_deg < 225:
                direction = 'left'
            elif 225 <= angle_deg < 315:
                direction = 'down'
            else:
                direction = 'right'
        else:
            direction = direction_or_angle
            speed_val = speed

        if forward > DEAD_ZONE_THRESHOLD:
            self.forward_history.append(forward)

        # Lead screw
        if forward > 0:
            self.set_motor_speed(LEAD_SCREW_MOTOR, forward, MotorDirection.FORWARD)
        else:
            self.set_motor_speed(LEAD_SCREW_MOTOR, 0, MotorDirection.STOP)

        # Stop others first
        for i in range(NUM_MOTORS):
            if i != LEAD_SCREW_MOTOR:
                self.set_motor_speed(i, 0, MotorDirection.STOP)

        if direction == 'right':
            self.set_motor_speed(1, speed_val * 0.8, MotorDirection.FORWARD)
            self.set_motor_speed(2, speed_val * 0.8, MotorDirection.REVERSE)

        elif direction == 'left':
            self.set_motor_speed(1, speed_val * 0.8, MotorDirection.REVERSE)
            self.set_motor_speed(2, speed_val * 0.8, MotorDirection.FORWARD)

        elif direction == 'up':
            self.set_motor_speed(3, speed_val * 0.7, MotorDirection.FORWARD)
            self.set_motor_speed(4, speed_val * 0.7, MotorDirection.FORWARD)

        elif direction == 'down':
            self.set_motor_speed(3, speed_val * 0.7, MotorDirection.REVERSE)
            self.set_motor_speed(4, speed_val * 0.7, MotorDirection.REVERSE)

    # ------------------------------------------------
    # CONTROL LOOP
    # ------------------------------------------------

    def start_control_loop(self):

        if self.control_thread and self.control_thread.is_alive():
            return

        self.running = True
        self.control_thread = threading.Thread(target=self._control_loop, daemon=True)
        self.control_thread.start()

    def stop_control_loop(self):
        self.running = False
        if self.control_thread:
            self.control_thread.join(timeout=1.0)

    def _control_loop(self):
        while self.running:
            try:
                self._request_status()
                time.sleep(1.0 / CONTROL_LOOP_FREQUENCY)
            except Exception as e:
                print("Control loop error:", e)
                time.sleep(1.0)

    def emergency_stop(self):
        for i in range(NUM_MOTORS):
            self.set_motor_speed(i, 0, MotorDirection.STOP)