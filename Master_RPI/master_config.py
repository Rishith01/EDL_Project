"""
Configuration file for Robotic Arm Motor Control System
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
# six continuum motors (bottom→top), two tentacle motors, plus one lead‑screw motor
NUM_MOTORS = 9
TENTACLE_MOTORS = [7, 8]          # tentacle end effector (IDs 7 and 8)
CONTINUUM_MOTORS = [1, 2, 3, 4, 5, 6]  # continuum robot motors (IDs 1-6)
LEAD_SCREW_MOTOR = 0              # motor 0 controls the lead screw for overall forward/back motion

# PWM Configuration
PWM_FREQUENCY = 50  # Hz for servo motors
PWM_MAX_VALUE = 4095  # 12-bit PWM

# Control Parameters
DEAD_ZONE_THRESHOLD = 0.1  # Minimum speed to activate motors
CONTROL_LOOP_FREQUENCY = 10  # Hz

# Safety Limits
MAX_MOTOR_SPEED = 1.0
EMERGENCY_STOP_TIMEOUT = 1.0  # seconds

# Dummy mapping from limit switches to affected motors.  In practice you can
# specify which motor(s) should be disabled when a particular switch is
# triggered.  Use indices consistent with your hardware (0-based).  Example:
# LIMIT_SWITCH_TO_MOTORS = {0: [1,2], 3: [5]} means switch 0 shields motors 1
# and 2, switch 3 shields motor 5.  Adjust in your configuration file.
LIMIT_SWITCH_TO_MOTORS = {
    0: [1, 2],   # bottom continuum module
    1: [3, 4],   # middle module
    2: [5, 6],   # top module
    3: [7, 8],   # tentacle end effector
    # other mappings as needed
}

# derived helper mapping (motor -> switches affecting it)
MOTOR_TO_LIMIT_SWITCHES = {}
for sw, motors in LIMIT_SWITCH_TO_MOTORS.items():
    for m in motors:
        MOTOR_TO_LIMIT_SWITCHES.setdefault(m, []).append(sw)

# Encoder Configuration
ENCODER_BITS = 16  # 16-bit encoders
ENCODER_UPDATE_RATE = 10  # Hz

# Limit Switch Configuration
NUM_LIMIT_SWITCHES = 16
LIMIT_SWITCH_UPDATE_RATE = 10  # Hz

# Debug Settings
DEBUG_MODE = True
SIMULATION_MODE = False  # Set to True for testing without hardware