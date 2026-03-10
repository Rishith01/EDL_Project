"""
Driver for SPI port expander which reads limit switches and possibly other
inputs.  Replace the implementation when the exact chip is known.
"""
from machine import SPI, Pin
from config import SPI_SCK, SPI_MOSI, SPI_MISO, SPI_CS, SPI_FREQ

spi = SPI(0, baudrate=SPI_FREQ, polarity=0, phase=0,
          sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
cs = Pin(SPI_CS, Pin.OUT)


def read_register(addr):
    """Basic read, chip-specific details required."""
    cs.value(0)
    spi.write(bytearray([addr | 0x80]))
    result = spi.read(1)
    cs.value(1)
    return result[0]


def write_register(addr, value):
    cs.value(0)
    spi.write(bytearray([addr & 0x7F, value]))
    cs.value(1)

# TODO: add high‑level helpers once the part number is chosen
