"""
=====================================================================================
This module acts as the Hardware Abstraction Layer (HAL) for the physical DC motors. 
It interfaces with a daisy-chained array of Adafruit Motor Shields (PCA9685 chips) 
over a single I2C bus to drive the tendon-actuation and lead screw mechanisms.

Core Responsibilities:
1. Flat-Index Mapping        : Abstracts multiple physical I2C boards into a single, 
                               continuous array, so the Master script doesn't have to calculate board addresses.
2. PWM Scaling               : Translates speed percentages (0-100%) into 12-bit hardware duty cycles (0-4095).


Software Dependencies:
1. pca9685.py (Standard MicroPython PCA9685 driver library)
=====================================================================================
"""

from pca9685 import PCA9685

class FeatherDriver:
    # Pin mappings for the Adafruit Motor Shield V2 / FeatherWing
    # Format: (PWM_Pin, IN1_Pin, IN2_Pin)
    MOTOR_PINS = [
        (8, 10, 9),   # Motor 1 (M1 on board)
        (13, 11, 12), # Motor 2 (M2 on board)
        (2, 4, 3),    # Motor 3 (M3 on board)
        (7, 5, 6)     # Motor 4 (M4 on board)
    ]

    def __init__(self, i2c_bus, addresses=[0x60, 0x61, 0x62]):
        self.boards = []
        # Initialize each PCA9685 board found in the address list
        for addr in addresses:
            board = PCA9685(i2c_bus, address=addr)
            board.freq(1600)  # Standard PWM frequency for DC motors
            self.boards.append(board)
            
        self.PWM_MAX = 4095
        self.PWM_TENSION = 800   # Low holding voltage to keep tendons tight
        self.PWM_HOLD = 0        

    def set_motor(self, global_motor_index, speed, direction_forward=True):
        # Calculate which physical board and which local motor port to use
        board_idx = global_motor_index // 4
        local_motor_idx = global_motor_index % 4
        
        if board_idx >= len(self.boards):
            return 
            
        board = self.boards[board_idx]
        pwm_pin, in1_pin, in2_pin = self.MOTOR_PINS[local_motor_idx]
        
        board.duty(pwm_pin, speed)
        
        if speed == 0:
            # Both pins must be 4095 (HIGH) to lock the shaft
            board.duty(in1_pin, 4095)
            board.duty(in2_pin, 4095)
        elif direction_forward:
            board.duty(in1_pin, 4095) 
            board.duty(in2_pin, 0)    
        else:
            board.duty(in1_pin, 0)    
            board.duty(in2_pin, 4095) 

    def state_move(self, motor_index, forward=True, speed=100):
        # High-level command to move a motor using 0-100% speed scaling.
        clamped_speed = max(0, min(100, speed))
        pwm_value = int((clamped_speed / 100.0) * 4095)
        self.set_motor(motor_index, pwm_value, forward)

    def state_tension(self, motor_index, forward=True):
        #Applies a low holding voltage to spool up slack cable.
        self.set_motor(motor_index, self.PWM_TENSION, forward)

    def state_hold(self, motor_index, forward=True):
        #Instantly halts and locks the motor shaft.
        self.set_motor(motor_index, self.PWM_HOLD, forward)

    def set_grasp(self, is_grasping):
        #Dedicated helper function for the Gripper actuator (Motor 8).
        self.set_motor(8, self.PWM_MAX if is_grasping else 0, True)
