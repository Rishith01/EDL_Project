"""
Configuration for Pico W slave firmware.
"""
from machine import Pin

# I2C slave address
I2C_SCL = 5
I2C_SDA = 4
I2C_FREQ = 400_000
SLAVE_I2C_ADDR = 0x10

# Encoder pins (if slave reads its own encoders)
ENCODER_PINS = [ (2,3) ]

# interrupt input from master to signal new command
MASTER_INT_PIN = Pin(20, Pin.IN)

DEBUG = True
