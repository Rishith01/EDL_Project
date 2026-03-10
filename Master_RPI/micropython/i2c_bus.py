"""
Simple wrapper to initialise and hold a shared I2C object.
"""
from machine import I2C, Pin
from config import I2C_SCL, I2C_SDA, I2C_FREQ

# Single I2C bus instance for master
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=I2C_FREQ)


def scan():
    return i2c.scan()
