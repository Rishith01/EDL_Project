"""
Quadrature encoder reader using pin interrupt callbacks.
Each encoder instance maintains a position count and can be queried
from the main task.
"""
from machine import Pin
import micropython

class QuadratureEncoder:
    def __init__(self, pin_a, pin_b):
        self.pin_a = Pin(pin_a, Pin.IN, Pin.PULL_UP)
        self.pin_b = Pin(pin_b, Pin.IN, Pin.PULL_UP)
        self.position = 0
        # attach interrupts
        self.pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
                       handler=self._callback)
        self.pin_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
                       handler=self._callback)

    def _callback(self, pin):
        # simple state machine -- do the minimal work here
        a = self.pin_a.value()
        b = self.pin_b.value()
        if a == b:
            self.position += 1
        else:
            self.position -= 1

    def get_position(self):
        return self.position

# Example usage:
# enc = QuadratureEncoder(2,3)
# pos = enc.get_position()
