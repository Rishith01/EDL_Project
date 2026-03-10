"""
Configuration file for Robotic Arm Motor Control System
"""

# ================================================
# UART COMMUNICATION
# ================================================
UART_PORT = '/dev/ttyAMA0'  # Raspberry Pi UART port
UART_BAUDRATE = 9600

# Dedicated UART used for master <-> slave/motor bus packets
MOTOR_BUS_UART_PORT = '/dev/serial0'
MOTOR_BUS_BAUDRATE = 115200

# ================================================
# MOTOR CONFIGURATION
# ================================================
NUM_MOTORS = 9
LEAD_SCREW_MOTOR = 0              # Motor 0: lead-screw for forward/backward movement
CONTINUUM_MOTORS = [1, 2, 3, 4, 5, 6]  # Motors 1-6: continuum robot links (3 modules × 2 motors)
TENTACLE_MOTORS = [7, 8]          # Motors 7-8: tentacle end effector

# ================================================
# MOTOR CONTROL PARAMETERS
# ================================================
PWM_MAX_VALUE = 4095              # 12-bit PWM range for motor speeds
DEAD_ZONE_THRESHOLD = 0.1         # Minimum speed to activate motors
CONTROL_LOOP_FREQUENCY = 10        # Hz - control loop update rate

# ================================================
# SAFETY LIMITS
# ================================================
MAX_MOTOR_SPEED = 1.0             # Maximum speed (0-1.0 normalized)
EMERGENCY_STOP_TIMEOUT = 1.0      # Seconds

# ================================================
# LIMIT SWITCH CONFIGURATION
# ================================================
NUM_LIMIT_SWITCHES = 16

# Directional Limit Switch Mappings
# Maps (motor_id, direction_value) -> list of limit switch indices that block this movement
# direction_value: 1=FORWARD, 0=REVERSE, 2=STOP
# Adjust these mappings based on your physical limit switch positions
DIRECTIONAL_LIMIT_SWITCHES = {
    # Bottom continuum (motors 1-2, left/right bending)
    (1, 1): [0],      # Motor 1 FORWARD (right) blocked by switch 0 (right limit)
    (1, 0): [4],      # Motor 1 REVERSE (left) blocked by switch 4 (left limit)
    (2, 1): [4],      # Motor 2 FORWARD (left) blocked by switch 4 (left limit)
    (2, 0): [0],      # Motor 2 REVERSE (right) blocked by switch 0 (right limit)
    
    # Middle continuum (motors 3-4, up/down bending)
    (3, 1): [1],      # Motor 3 FORWARD (up) blocked by switch 1 (up limit)
    (3, 0): [5],      # Motor 3 REVERSE (down) blocked by switch 5 (down limit)
    (4, 1): [1],      # Motor 4 FORWARD (up) blocked by switch 1 (up limit)
    (4, 0): [5],      # Motor 4 REVERSE (down) blocked by switch 5 (down limit)
    
    # Top continuum (motors 5-6, up/down bending)
    (5, 1): [2],      # Motor 5 FORWARD (up) blocked by switch 2 (up limit)
    (5, 0): [6],      # Motor 5 REVERSE (down) blocked by switch 6 (down limit)
    (6, 1): [2],      # Motor 6 FORWARD (up) blocked by switch 2 (up limit)
    (6, 0): [6],      # Motor 6 REVERSE (down) blocked by switch 6 (down limit)
    
    # Tentacle (motors 7-8)
    (7, 1): [3],      # Motor 7 FORWARD blocked by switch 3
    (7, 0): [7],      # Motor 7 REVERSE blocked by switch 7
    (8, 1): [3],      # Motor 8 FORWARD blocked by switch 3
    (8, 0): [7],      # Motor 8 REVERSE blocked by switch 7
}

# Module Hierarchy for Compensation
# When a limit switch blocks a lower module, try compensating by adjusting upper modules
MODULE_HIERARCHY = {
    0: [],           # Lead screw has no upper modules
    1: [3, 5],       # Bottom continuum compensated by middle and top
    2: [3, 5],       # Bottom continuum compensated by middle and top
    3: [5],          # Middle continuum compensated by top
    4: [5],          # Middle continuum compensated by top
    5: [],           # Top continuum has no upper modules
    6: [],           # Top continuum has no upper modules
    7: [],           # Tentacle has no upper modules
    8: [],           # Tentacle has no upper modules
}


# ================================================
# ENCODER SETUP DETAILS (SLAVE SIDE REFERENCE)
# ================================================
# GPIO BCM pin pairs used by the slave encoder interface.
# Keep this in sync with Slave_RPI/slave_encoder_interface.py.
SLAVE_ENCODER_PINS = [
    (17, 18),
    (22, 23),
    (24, 25),
    (5, 6),
    (12, 13),
    (19, 20),
    (16, 26),
    (21, 27),
]

# ================================================
# DEBUG SETTINGS
# ================================================
DEBUG_MODE = True
SIMULATION_MODE = False  # Set to True for testing without hardware