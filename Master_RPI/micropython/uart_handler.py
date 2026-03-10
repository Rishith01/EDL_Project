"""
UART driver for receiving commands from the laptop GUI.
Uses hardware interrupt on Rx to enqueue bytes; final decoding happens in
main loop/task so the ISR stays short.
"""
from machine import UART
import uasyncio as asyncio
from collections import deque
from config import UART_PORT, UART_BAUDRATE

uart = UART(UART_PORT, baudrate=UART_BAUDRATE)
# buffer for received data
_rx_queue = deque()


def _uart_irq(_):
    # called in interrupt context whenever data arrives
    while uart.any():
        _rx_queue.append(uart.read(1))

# attach irq to receive any character
uart.irq(handler=_uart_irq, trigger=UART.RX_ANY)


async def command_listener(callback):
    """Coroutine that collects complete lines and calls callback(line)."""
    line = b""
    while True:
        while _rx_queue:
            ch = _rx_queue.popleft()
            if ch == b'\n' or ch == b'\r':
                if line:
                    try:
                        callback(line.decode())
                    except Exception as e:
                        print("UART callback error", e)
                line = b""
            else:
                line += ch
        await asyncio.sleep_ms(10)


def send_response(s: str):
    """Send a line back to GUI; safe from tasks but not from ISR."""
    uart.write(s + "\r\n")
