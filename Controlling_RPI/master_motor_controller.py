"""
Motor Control System for Robotic Arm
Handles communication with slave devices for motor control
"""

import time
import math
import threading
from enum import Enum
from master_config import *


class MotorDirection(Enum):
    """Motor rotation directions"""
    FORWARD = 1
    REVERSE = 0
    STOP = 2


class MotorController:
    """
    Main motor controller for 8 motors:
    - Motors 0-1: Tentacle end effector
    - Motors 2-7: Continuum robot joints
    """

    def __init__(self, pwm_address=PWM_GENERATOR_ADDRESS, gpio_expander_1_address=GPIO_EXPANDER_1_ADDRESS,
                 gpio_expander_2_address=GPIO_EXPANDER_2_ADDRESS, slave_rpi_address=SLAVE_RPI_ADDRESS):
        """
        Initialize motor controller with slave addresses

        Args:
            pwm_address: I2C address of PWM generator
            gpio_expander_1_address: I2C address of GPIO expander for motor directions
            gpio_expander_2_address: I2C address of GPIO expander for limit switches
            slave_rpi_address: I2C address of slave RPi for encoder readings
        """
        self.pwm_address = pwm_address
        self.gpio_expander_1_address = gpio_expander_1_address
        self.gpio_expander_2_address = gpio_expander_2_address
        self.slave_rpi_address = slave_rpi_address

        # Motor states
        self.motor_speeds = [0] * NUM_MOTORS  # PWM duty cycles (0-PWM_MAX_VALUE)
        self.motor_directions = [MotorDirection.STOP] * NUM_MOTORS

        # Encoder values from slave RPi
        self.encoder_values = [0] * NUM_MOTORS

        # Limit switch states
        self.limit_switches = [False] * NUM_LIMIT_SWITCHES

        # Control thread
        self.control_thread = None
        self.running = False

        # Initialize I2C bus (placeholder - will be implemented with actual hardware)
        self.i2c_bus = None

    def initialize_hardware(self):
        """Initialize I2C communication and slave devices"""
        try:
            # Import smbus for I2C communication (Raspberry Pi)
            import smbus
            self.i2c_bus = smbus.SMBus(1)  # I2C bus 1 on RPi

            # Initialize PWM generator (PCA9685)
            self._init_pwm_generator()

            # Initialize GPIO expanders (MCP23017)
            self._init_gpio_expanders()

            print("[MotorController] Hardware initialized successfully")
            return True

        except ImportError:
            print("[MotorController] Warning: smbus not available (simulation mode)")
            return False
        except Exception as e:
            print(f"[MotorController] Hardware initialization failed: {e}")
            return False

    def _init_pwm_generator(self):
        """Initialize PCA9685 PWM generator"""
        if self.i2c_bus:
            # Set PWM frequency to configured value
            self.i2c_bus.write_byte_data(self.pwm_address, 0x00, 0x10)  # MODE1 register
            time.sleep(0.01)
            # Set frequency
            prescale = int(25000000 / (4096 * PWM_FREQUENCY) - 1)
            self.i2c_bus.write_byte_data(self.pwm_address, 0xFE, prescale)  # PRE_SCALE register
            time.sleep(0.01)
            self.i2c_bus.write_byte_data(self.pwm_address, 0x00, 0x00)  # MODE1 register

    def _init_gpio_expanders(self):
        """Initialize MCP23017 GPIO expanders"""
        if self.i2c_bus:
            # GPIO Expander 1: Motor directions (8 outputs)
            self.i2c_bus.write_byte_data(self.gpio_expander_1_address, 0x00, 0x00)  # IODIRA - all outputs
            self.i2c_bus.write_byte_data(self.gpio_expander_1_address, 0x01, 0x00)  # IODIRB - all outputs

            # GPIO Expander 2: Limit switches (16 inputs)
            self.i2c_bus.write_byte_data(self.gpio_expander_2_address, 0x00, 0xFF)  # IODIRA - all inputs
            self.i2c_bus.write_byte_data(self.gpio_expander_2_address, 0x01, 0xFF)  # IODIRB - all inputs

    def set_motor_speed(self, motor_id, speed, direction):
        """
        Set speed and direction for a specific motor

        Args:
            motor_id (int): Motor ID (0-7)
            speed (float): Speed (0.0 to 1.0)
            direction (MotorDirection): Motor direction
        """
        if not 0 <= motor_id < NUM_MOTORS:
            print(f"[MotorController] Invalid motor ID: {motor_id}")
            return

        # Convert speed to PWM duty cycle (0-PWM_MAX_VALUE)
        pwm_value = int(speed * PWM_MAX_VALUE)

        self.motor_speeds[motor_id] = pwm_value
        self.motor_directions[motor_id] = direction

        # Send to hardware
        self._update_motor_hardware(motor_id)

    def _update_motor_hardware(self, motor_id):
        """Update motor control hardware"""
        if self.i2c_bus:
            # Set PWM duty cycle
            pwm_reg = 0x06 + motor_id * 4  # LED0_ON_L + motor_id * 4
            on_value = 0
            off_value = self.motor_speeds[motor_id]

            self.i2c_bus.write_byte_data(self.pwm_address, pwm_reg, on_value & 0xFF)
            self.i2c_bus.write_byte_data(self.pwm_address, pwm_reg + 1, on_value >> 8)
            self.i2c_bus.write_byte_data(self.pwm_address, pwm_reg + 2, off_value & 0xFF)
            self.i2c_bus.write_byte_data(self.pwm_address, pwm_reg + 3, off_value >> 8)

            # Set direction via GPIO expander
            current_directions = 0
            for i in range(8):
                if self.motor_directions[i] == MotorDirection.FORWARD:
                    current_directions |= (1 << i)

            self.i2c_bus.write_byte_data(self.gpio_expander_1_address, 0x12, current_directions & 0xFF)  # GPIOA
            self.i2c_bus.write_byte_data(self.gpio_expander_1_address, 0x13, current_directions >> 8)   # GPIOB

    def read_encoders(self):
        """Read encoder values from slave RPi"""
        if self.i2c_bus:
            try:
                # Read 16 bytes (2 bytes per encoder * 8 encoders)
                data = []
                for i in range(16):
                    data.append(self.i2c_bus.read_byte_data(self.slave_rpi_address, i))

                # Convert to 16-bit values
                for i in range(8):
                    self.encoder_values[i] = (data[i*2] << 8) | data[i*2 + 1]

            except Exception as e:
                print(f"[MotorController] Encoder read failed: {e}")

        return self.encoder_values.copy()

    def read_limit_switches(self):
        """Read limit switch states from GPIO expander 2"""
        if self.i2c_bus:
            try:
                gpioa = self.i2c_bus.read_byte_data(self.gpio_expander_2_address, 0x12)
                gpiob = self.i2c_bus.read_byte_data(self.gpio_expander_2_address, 0x13)

                switches = (gpiob << 8) | gpioa
                for i in range(16):
                    self.limit_switches[i] = bool(switches & (1 << i))

            except Exception as e:
                print(f"[MotorController] Limit switch read failed: {e}")

        return self.limit_switches.copy()

    def process_direction_command(self, angle, speed):
        """
        Process direction command from GUI and translate to motor commands

        Args:
            angle (float): Direction angle in radians
            speed (float): Speed magnitude (0.0 to 1.0)
        """
        # Convert angle to degrees for easier processing
        angle_deg = math.degrees(angle) % 360

        # Basic motor mapping for continuum robot (motors 2-7)
        # This is a simplified mapping - adjust based on your robot kinematics

        # Stop all motors first
        for i in range(NUM_MOTORS):
            self.set_motor_speed(i, 0, MotorDirection.STOP)

        if speed < DEAD_ZONE_THRESHOLD:  # Dead zone
            return

        # Direction-based motor control
        if 0 <= angle_deg < 45 or 315 <= angle_deg < 360:
            # Forward/Right
            self.set_motor_speed(2, speed * 0.8, MotorDirection.FORWARD)  # Joint 1
            self.set_motor_speed(3, speed * 0.6, MotorDirection.REVERSE)  # Joint 2
        elif 45 <= angle_deg < 135:
            # Up
            self.set_motor_speed(4, speed * 0.7, MotorDirection.FORWARD)  # Joint 3
            self.set_motor_speed(5, speed * 0.5, MotorDirection.FORWARD)  # Joint 4
        elif 135 <= angle_deg < 225:
            # Left
            self.set_motor_speed(2, speed * 0.8, MotorDirection.REVERSE)  # Joint 1
            self.set_motor_speed(3, speed * 0.6, MotorDirection.FORWARD)  # Joint 2
        elif 225 <= angle_deg < 315:
            # Down
            self.set_motor_speed(4, speed * 0.7, MotorDirection.REVERSE)  # Joint 3
            self.set_motor_speed(5, speed * 0.5, MotorDirection.REVERSE)  # Joint 4

        # Tentacle end effector control (motors 0-1) - simplified
        # Could be controlled separately or based on angle
        if speed > 0.5:
            self.set_motor_speed(0, speed * 0.3, MotorDirection.FORWARD)  # Tentacle motor 1
            self.set_motor_speed(1, speed * 0.3, MotorDirection.REVERSE)  # Tentacle motor 2

        if DEBUG_MODE:
            print(f"[MotorController] Direction: {angle_deg:.1f}°, Speed: {speed:.2f}")
            print(f"[MotorController] Active motors: {[i for i, s in enumerate(self.motor_speeds) if s > 0]}")

    def start_control_loop(self):
        """Start the motor control and monitoring loop"""
        if self.control_thread and self.control_thread.is_alive():
            return

        self.running = True
        self.control_thread = threading.Thread(target=self._control_loop, daemon=True)
        self.control_thread.start()
        print("[MotorController] Control loop started")

    def stop_control_loop(self):
        """Stop the motor control loop"""
        self.running = False
        if self.control_thread:
            self.control_thread.join(timeout=1.0)
        print("[MotorController] Control loop stopped")

    def _control_loop(self):
        """Main control loop for monitoring encoders and limit switches"""
        while self.running:
            try:
                # Read encoders
                encoders = self.read_encoders()

                # Read limit switches
                switches = self.read_limit_switches()

                # Check for limit switch violations
                for i, switch in enumerate(switches):
                    if switch:
                        print(f"[MotorController] Limit switch {i} triggered!")
                        # Emergency stop motors connected to this switch
                        # This mapping depends on your hardware setup

                time.sleep(1.0 / CONTROL_LOOP_FREQUENCY)  # Configurable frequency

            except Exception as e:
                print(f"[MotorController] Control loop error: {e}")
                time.sleep(1.0)

    def emergency_stop(self):
        """Emergency stop all motors"""
        print("[MotorController] EMERGENCY STOP!")
        for i in range(8):
            self.set_motor_speed(i, 0, MotorDirection.STOP)

    def get_status(self):
        """Get current motor controller status"""
        return {
            'motor_speeds': self.motor_speeds.copy(),
            'motor_directions': [d.name for d in self.motor_directions],
            'encoder_values': self.encoder_values.copy(),
            'limit_switches': self.limit_switches.copy(),
            'control_loop_running': self.running
        }