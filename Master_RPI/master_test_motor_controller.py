"""
Test script for Motor Controller
Tests motor control functionality in simulation mode
"""

import time
import math
from master_motor_controller import MotorController, MotorDirection
from master_command_processor import CommandProcessor
from master_config import NUM_MOTORS


def test_motor_controller():
    """Test basic motor controller functionality"""
    print("Testing Motor Controller...")

    # Create motor controller (simulation mode)
    controller = MotorController()

    # Test hardware initialization (should fail gracefully in simulation)
    success = controller.initialize_hardware()
    print(f"Hardware initialization: {'Success' if success else 'Failed (expected in simulation)'}")

    # Test motor speed setting
    print("\nTesting motor speed control...")
    for motor_id in range(NUM_MOTORS):
        controller.set_motor_speed(motor_id, 0.5, MotorDirection.FORWARD)
        print(f"Set motor {motor_id} to 50% speed, FORWARD")

    # Test direction commands, covering both legacy and new messages
    print("\nTesting direction commands...")
    test_angles = [0, math.pi/4, math.pi/2, math.pi, 3*math.pi/2]
    test_speeds = [0.2, 0.5, 0.8]
    for angle in test_angles:
        for speed in test_speeds:
            print(f"Legacy: angle {math.degrees(angle):.1f}°, speed {speed}")
            controller.process_direction_command(angle, speed)
            time.sleep(0.05)
    # new cardinal commands
    cardinal = ['forward', 'left', 'right', 'up', 'down', 'backward']
    for d in cardinal:
        for speed in test_speeds:
            forward = 1.0 - speed if d != 'forward' else 1.0
            print(f"New: dir {d}, speed {speed}, forward {forward}")
            controller.process_direction_command(d, speed, forward)
            time.sleep(0.05)

    # Test encoder reading (simulation)
    print("\nTesting encoder reading...")
    encoders = controller.read_encoders()
    print(f"Encoder values: {encoders}")

    # Test limit switch reading (simulation)
    print("\nTesting limit switch reading...")
    switches = controller.read_limit_switches()
    print(f"Limit switches: {switches}")

    # Test emergency stop
    print("\nTesting emergency stop...")
    controller.emergency_stop()

    # Get status
    print("\nFinal status:")
    status = controller.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("Motor Controller test completed!")


def test_command_processor():
    """Test command processor parsing"""
    print("\nTesting Command Processor...")

    from master_command_processor import CommandProcessor

    # Create command processor
    processor = CommandProcessor()

    # Test command parsing
    test_commands = [
        # legacy
        "ANGLE:0.00,SPEED:0.50",
        "ANGLE:1.57,SPEED:0.80",  # π/2
        "ANGLE:-1.57,SPEED:0.30", # -π/2
        # new
        "DIR:FORWARD,SPEED:0.20,FWD:1.00",
        "DIR:LEFT,SPEED:0.70,FWD:0.30",
        "DIR:DOWN,SPEED:0.40,FWD:0.60",
        "CAPTURE",
        "INVALID:COMMAND"
    ]

    for cmd in test_commands:
        print(f"Processing command: {cmd}")
        processor._process_command(cmd)
        time.sleep(0.1)

    print("Command Processor test completed!")


def interactive_test():
    """Interactive testing mode"""
    print("\nInteractive Test Mode")
    print("Commands:")
    print("  angle <degrees> <speed>  - Test direction command")
    print("  capture                  - Test capture command")
    print("  status                  - Show system status")
    print("  stop                    - Emergency stop")
    print("  quit                    - Exit test")

    controller = MotorController()
    processor = CommandProcessor()

    while True:
        try:
            cmd = input("Command: ").strip().lower()

            if cmd == "quit":
                break
            elif cmd == "status":
                status = controller.get_status()
                print("Motor Status:")
                for key, value in status.items():
                    print(f"  {key}: {value}")
            elif cmd == "stop":
                controller.emergency_stop()
                print("Emergency stop activated")
            elif cmd.startswith("angle"):
                parts = cmd.split()
                if len(parts) == 3:
                    degrees = float(parts[1])
                    speed = float(parts[2])
                    angle_rad = math.radians(degrees)
                    controller.process_direction_command(angle_rad, speed)
                    print(f"Set direction: {degrees}°, speed: {speed}")
                else:
                    print("Usage: angle <degrees> <speed>")
            elif cmd == "capture":
                processor._process_capture_command()
                print("Capture command sent")
            elif cmd.startswith("capture"):
                print("Usage: capture (no parameters needed)")
            else:
                print("Unknown command")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    controller.emergency_stop()
    print("Interactive test ended")


if __name__ == "__main__":
    print("Robotic Arm Motor Control Test Suite")
    print("=" * 40)

    # Run basic tests
    test_motor_controller()
    test_command_processor()

    # Interactive test
    interactive_test()