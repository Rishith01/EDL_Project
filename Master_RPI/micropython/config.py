"""
Configuration constants and pin assignments for Pico W master firmware.
This file should be imported by every other module.
"""
from machine import Pin

# ---------- UART (GUI) ----------
UART_PORT = 0                  # use UART0 TX=Pin(0), RX=Pin(1)
UART_BAUDRATE = 115200

# ---------- I2C (master <-> slave & motor driver) ----------
I2C_SCL = 5                    # GP5
I2C_SDA = 4                    # GP4
I2C_FREQ = 400_000             # 400kHz
SLAVE_I2C_ADDR = 0x10         # example
MOTOR_DRIVER_I2C_ADDR = 0x60  # Adafruit MotorKit default

# ---------- SPI (port expander) ----------
SPI_SCK = 18                   # GP18
SPI_MOSI = 19                  # GP19
SPI_MISO = 16                  # GP16
SPI_CS = 17                    # GP17
SPI_FREQ = 1_000_000           # 1MHz

# ---------- GPIO interrupts ----------
INT_MASTER_TO_SLAVE = Pin(20, Pin.OUT)
# for a future SPI expander interrupt
INT_SPI_EXPANDER = Pin(21, Pin.IN, Pin.PULL_UP)

# ---------- Encoders ----------
# assign pins for quadrature encoders; list of (A, B) pairs
ENCODER_PINS = [ (2, 3), (6, 7), (8, 9) ]  # example

# ---------- Limit switches ----------
NUM_LIMIT_SWITCHES = 16

# ---------- Misc ----------
DEBUG = True
CONTROL_LOOP_HZ = 10
