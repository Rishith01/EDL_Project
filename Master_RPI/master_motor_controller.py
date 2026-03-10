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

    def __init__(self, uart_port=MOTOR_BUS_UART_PORT, baudrate=MOTOR_BUS_BAUDRATE):

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
    # LIMIT SWITCH CHECKING
    # ------------------------------------------------

    def _is_motion_blocked(self, motor_id, direction):
        """
        Check if a motor motion in the given direction is blocked by an active limit switch.
        Returns: (is_blocked, blocking_switches)
        """
        key = (motor_id, direction.value)
        if key not in DIRECTIONAL_LIMIT_SWITCHES:
            return False, []
        
        blocking_switches = DIRECTIONAL_LIMIT_SWITCHES[key]
        for switch_id in blocking_switches:
            if self.limit_switches[switch_id]:
                return True, blocking_switches
        
        return False, []

    def _compensate_blocked_motion(self, motor_id, direction, speed):
        """
        When a motor is blocked by a limit switch, try to compensate by moving upper modules
        in the opposite direction to relieve pressure on the blocked link.
        """
        if motor_id not in MODULE_HIERARCHY or not MODULE_HIERARCHY[motor_id]:
            return  # No upper modules to compensate
        
        compensation_strength = speed * 0.3  # Use 30% of blocked motion for compensation
        opposite_direction = MotorDirection.REVERSE if direction == MotorDirection.FORWARD else MotorDirection.FORWARD
        
        # Try to move upper modules in opposite direction to relieve pressure
        for upper_motor in MODULE_HIERARCHY[motor_id]:
            if not self._is_motion_blocked(upper_motor, opposite_direction)[0]:
                self.set_motor_speed(upper_motor, compensation_strength, opposite_direction)
                if DEBUG_MODE:
                    print(f"[MotorController] Compensating blocked motor {motor_id} by moving upper motor {upper_motor} in opposite direction")
                return
    
    # ------------------------------------------------
    # MOTOR CONTROL
    # ------------------------------------------------

    def set_motor_speed(self, motor_id, speed, direction):

        if not 0 <= motor_id < NUM_MOTORS:
            return

        # Check if motion is blocked by limit switches (only when trying to move, not on STOP)
        if direction != MotorDirection.STOP:
            is_blocked, blocking_switches = self._is_motion_blocked(motor_id, direction)
            
            if is_blocked:
                if DEBUG_MODE:
                    print(f"[MotorController] Motor {motor_id} motion in direction {direction} blocked by limit switches {blocking_switches}")
                
                # Try to compensate with upper modules
                self._compensate_blocked_motion(motor_id, direction, speed)
                
                # Stop the blocked motor
                pwm_value = 0
                direction = MotorDirection.STOP
            else:
                pwm_value = int(speed * PWM_MAX_VALUE)
        else:
            pwm_value = 0

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


    def retrace_forward_history(self):
        """Retrace stored forward motions in reverse order."""
        if not self.forward_history:
            return

        # replay in reverse to pull the lead screw back along the prior path
        for forward in reversed(self.forward_history):
            self.set_motor_speed(LEAD_SCREW_MOTOR, forward, MotorDirection.REVERSE)
            time.sleep(0.1)

        self.set_motor_speed(LEAD_SCREW_MOTOR, 0, MotorDirection.STOP)
        self.forward_history.clear()

    def get_status(self):
        """Return a snapshot of motor-controller state for monitoring."""
        return {
            'motor_speeds': self.motor_speeds.copy(),
            'motor_directions': [d.name for d in self.motor_directions],
            'encoder_values': self.encoder_values.copy(),
            'limit_switches': self.limit_switches.copy(),
            'running': self.running,
            'serial_connected': bool(self.serial and self.serial.is_open),
        }

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

    def initialize_hardware(self):
        """Backward-compatible hardware setup hook for older callers."""
        return bool(self.serial and self.serial.is_open)

    def read_encoders(self):
        """Return latest encoder values cached from status packets."""
        return self.encoder_values.copy()

    def read_limit_switches(self):
        """Return latest limit switch states cached from status packets."""
        return self.limit_switches.copy()

    def emergency_stop(self):
        for i in range(NUM_MOTORS):
            self.set_motor_speed(i, 0, MotorDirection.STOP)