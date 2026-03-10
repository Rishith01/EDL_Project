"""
High‑level abstraction for limit switch logic.  The physical switches may be
wired directly to GPIOs or accessed via the SPI expander; this module hides
that detail and implements the mapping rules defined in config.py.
"""
from config import NUM_LIMIT_SWITCHES
from spi_expander import read_register

# if direct pins are used, import them here and populate `switch_pins` list
# switch_pins = [Pin(x, Pin.IN, Pin.PULL_UP) for x in DIRECT_PINS]


def read_all():
    """Return a list of boolean states for every limit switch."""
    # placeholder when using expander; assume registers 0x00..0x01 contain
    # the 16-bit input state.
    low = read_register(0x00)
    high = read_register(0x01)
    bits = (high << 8) | low
    return [bool(bits & (1 << i)) for i in range(NUM_LIMIT_SWITCHES)]


def is_blocked(motor_id, direction, mapping):
    """Utility: given DIRECTIONAL_LIMIT_SWITCHES mapping return (blocked,list)"""
    key = (motor_id, direction)
    if key not in mapping:
        return False, []
    states = read_all()
    blocked = []
    for idx in mapping[key]:
        if states[idx]:
            blocked.append(idx)
    return bool(blocked), blocked
