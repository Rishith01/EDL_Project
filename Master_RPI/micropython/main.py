"""
Entry point for the master Pico W firmware.  Sets up peripherals and starts
uasyncio tasks.
"""
import uasyncio as asyncio
from config import DEBUG, CONTROL_LOOP_HZ, INT_MASTER_TO_SLAVE
from uart_handler import command_listener, send_response
from motor_driver import set_speed, emergency_stop
from limit_switch import is_blocked
from encoder import QuadratureEncoder
from interrupts import register

# create encoder instances for every motor that has one
encoders = []
for a_pin, b_pin in config.ENCODER_PINS:
    encoders.append(QuadratureEncoder(a_pin, b_pin))


async def process_line(line):
    # parse command strings and act accordingly
    print("master received", line)
    # TODO: translate into motor_driver calls


async def control_loop():
    period = 1.0 / CONTROL_LOOP_HZ
    while True:
        # read encoders, limit switches, etc.
        # send status over UART if needed
        await asyncio.sleep(period)


def slave_interrupt(pin):
    # master signalled slave; build and send data over I2C
    pass


def setup():
    # configure interrupt pin to notify slave
    INT_MASTER_TO_SLAVE.on()

    # register other IRQs (e.g. limit switch expander)
    # register(config.INT_SPI_EXPANDER, Pin.IRQ_FALLING, spi_expander_irq)
    
    # create uasyncio tasks
    loop = asyncio.get_event_loop()
    loop.create_task(command_listener(process_line))
    loop.create_task(control_loop())
    loop.run_forever()


if __name__ == "__main__":
    setup()
