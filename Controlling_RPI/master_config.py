"""
Configuration file for Master RPi Robotic Arm Motor Control System
"""

# UART Configuration
UART_PORT = '/dev/ttyAMA0'  # Raspberry Pi UART port
UART_BAUDRATE = 9600

# I2C Addresses
PWM_GENERATOR_ADDRESS = 0x40      # PCA9685 PWM generator
GPIO_EXPANDER_1_ADDRESS = 0x20    # MCP23017 for motor directions
GPIO_EXPANDER_2_ADDRESS = 0x21    # MCP23017 for limit switches
SLAVE_RPI_ADDRESS = 0x50          # Slave RPi for encoder readings

# Motor Configuration
NUM_MOTORS = 8
TENTACLE_MOTORS = [0, 1]          # Tentacle end effector motors
CONTINUUM_MOTORS = [2, 3, 4, 5, 6, 7]  # Continuum robot motors

# PWM Configuration
PWM_FREQUENCY = 50  # Hz for servo motors
PWM_MAX_VALUE = 4095  # 12-bit PWM

# Control Parameters
DEAD_ZONE_THRESHOLD = 0.1  # Minimum speed to activate motors
CONTROL_LOOP_FREQUENCY = 10  # Hz

# Safety Limits
MAX_MOTOR_SPEED = 1.0
EMERGENCY_STOP_TIMEOUT = 1.0  # seconds

# Encoder Configuration
ENCODER_BITS = 16  # 16-bit encoders
ENCODER_UPDATE_RATE = 10  # Hz

# Limit Switch Configuration
NUM_LIMIT_SWITCHES = 16
LIMIT_SWITCH_UPDATE_RATE = 10  # Hz

# Debug Settings
DEBUG_MODE = True
SIMULATION_MODE = False  # Set to True for testing without hardware