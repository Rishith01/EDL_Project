"""
Wrapper around the Adafruit MotorKit (PCA9685) driver.
This example assumes the `adafruit_motor` and related libraries have been
ported/installed in the Pico filesystem.
"""
from adafruit_motorkit import MotorKit
from i2c_bus import i2c

kit = MotorKit(i2c=i2c)


def set_speed(motor_num, speed):
    """Set motor number (0..n) to speed in range -1.0..1.0."""
    if speed > 1:
        speed = 1
    if speed < -1:
        speed = -1
    # MotorKit uses attributes motor1..motor4, change as needed.
    motor = getattr(kit, f"motor{motor_num+1}", None)
    if motor is None:
        raise ValueError("invalid motor index")
    if speed >= 0:
        motor.throttle = speed
    else:
        motor.throttle = -speed


def stop_all():
    for i in range(1, 5):
        getattr(kit, f"motor{i}").throttle = 0

# If the driver has a "brake" pin or addressable register you may expose
# an interrupt-safe emergency_stop() as well.

def emergency_stop():
    stop_all()
