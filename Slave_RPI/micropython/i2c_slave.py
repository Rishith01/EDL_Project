"""
Minimal I2C slave implementation using the Pico's I2C peripheral in
handshake/interrupt mode.  MicroPython doesn't currently support slave mode
natively on all ports; this may require low-level register access or use of
an external library such as https://github.com/micropython/micropython/issues/...

For now we show a placeholder that polls in a task after being triggered by
master interrupt.
"""
from machine import I2C
from config import I2C_SCL, I2C_SDA, I2C_FREQ, SLAVE_I2C_ADDR

# if there is a driver available:
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=I2C_FREQ)


def read_command():
    # placeholder; master should write commands starting with a known byte
    buf = bytearray(16)
    try:
        n = i2c.readfrom_into(SLAVE_I2C_ADDR, buf)
        return buf[:n]
    except Exception:
        return b''


def write_status(data):
    try:
        i2c.writeto(SLAVE_I2C_ADDR, data)
    except Exception:
        pass
