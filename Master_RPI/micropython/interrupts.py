"""
Central interrupt registration and scheduling helpers.
MicroPython ISRs must be short; use micropython.schedule to defer work.
"""
import micropython

handlers = {}


def register(pin, trigger, handler, arg=None):
    """Attach an irq to a Pin and remember the handler for scheduling."""
    def _irq(p):
        # schedule the real handler with optional arg
        if arg is not None:
            micropython.schedule(handler, arg)
        else:
            micropython.schedule(handler, p)
    pin.irq(trigger=trigger, handler=_irq)
    handlers[pin] = handler


# Example of a scheduled callback signature
# def my_handler(arg_or_pin):
#     # called outside interrupt context
#     pass
