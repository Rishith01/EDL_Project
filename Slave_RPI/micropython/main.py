"""
Entry point for slave Pico W firmware.
"""
import uasyncio as asyncio
import config
from config import MASTER_INT_PIN, DEBUG
from encoder import QuadratureEncoder
from i2c_slave import read_command, write_status

# set up encoder(s)
enc = QuadratureEncoder(*config.ENCODER_PINS[0])

async def handle_master():
    while True:
        # wait for master interrupt - busy-wait or use micropython.schedule
        if MASTER_INT_PIN.value() == 1:
            cmd = read_command()
            if cmd:
                if DEBUG:
                    print("got I2C cmd", cmd)
                # process command
            # clear or acknowledge by lowering pin
        await asyncio.sleep_ms(50)


def setup():
    loop = asyncio.get_event_loop()
    loop.create_task(handle_master())
    loop.run_forever()


if __name__ == "__main__":
    setup()
