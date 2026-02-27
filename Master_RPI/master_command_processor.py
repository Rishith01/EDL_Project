"""
Command Processor for Robotic Arm Control
Receives commands from GUI via UART and controls motors
"""

import serial
import threading
import time
import re
from master_motor_controller import MotorController
from master_config import *


class CommandProcessor:
    """Processes commands from GUI and controls motor system"""

    def __init__(self, uart_port=UART_PORT, uart_baudrate=UART_BAUDRATE,
                 pwm_addr=PWM_GENERATOR_ADDRESS, gpio1_addr=GPIO_EXPANDER_1_ADDRESS,
                 gpio2_addr=GPIO_EXPANDER_2_ADDRESS, slave_rpi_addr=SLAVE_RPI_ADDRESS):
        """
        Initialize command processor

        Args:
            uart_port: UART port for GUI communication
            uart_baudrate: UART baud rate
            pwm_addr: PWM generator I2C address
            gpio1_addr: GPIO expander 1 I2C address
            gpio2_addr: GPIO expander 2 I2C address
            slave_rpi_addr: Slave RPi I2C address
        """
        self.uart_port = uart_port
        self.uart_baudrate = uart_baudrate

        # Initialize motor controller
        self.motor_controller = MotorController(
            pwm_address=pwm_addr,
            gpio_expander_1_address=gpio1_addr,
            gpio_expander_2_address=gpio2_addr,
            slave_rpi_address=slave_rpi_addr
        )

        # UART communication
        self.serial = None
        self.uart_thread = None
        self.running = False

        # Command patterns
        self.angle_speed_pattern = re.compile(r'ANGLE:(-?\d+\.?\d*),SPEED:(\d+\.?\d*)')
        # new cardinal format
        self.dir_pattern = re.compile(r'DIR:([A-Z]+),SPEED:(\d+\.?\d*),FWD:(\d+\.?\d*)')
        self.capture_pattern = re.compile(r'CAPTURE$')

    def start(self):
        """Start the command processor"""
        print("[CommandProcessor] Starting...")

        # Initialize motor controller hardware
        if not self.motor_controller.initialize_hardware():
            print("[CommandProcessor] Hardware initialization failed - running in simulation mode")

        # Start motor control loop
        self.motor_controller.start_control_loop()

        # Start UART communication
        self.running = True
        self.uart_thread = threading.Thread(target=self._uart_listener, daemon=True)
        self.uart_thread.start()

        print("[CommandProcessor] Started successfully")

    def stop(self):
        """Stop the command processor"""
        print("[CommandProcessor] Stopping...")

        self.running = False

        # Stop motor control
        self.motor_controller.stop_control_loop()
        self.motor_controller.emergency_stop()

        # Close UART
        if self.serial and self.serial.is_open:
            self.serial.close()

        if self.uart_thread:
            self.uart_thread.join(timeout=1.0)

        print("[CommandProcessor] Stopped")

    def _uart_listener(self):
        """Listen for UART commands from GUI"""
        while self.running:
            try:
                # Open serial connection if not already open
                if not self.serial or not self.serial.is_open:
                    self.serial = serial.Serial(
                        port=self.uart_port,
                        baudrate=self.uart_baudrate,
                        timeout=1.0
                    )
                    print(f"[CommandProcessor] UART connected on {self.uart_port}")

                # Read line from UART
                if self.serial.in_waiting > 0:
                    line = self.serial.readline().decode().strip()
                    if line:
                        self._process_command(line)

            except serial.SerialException as e:
                print(f"[CommandProcessor] UART error: {e}")
                if self.serial:
                    self.serial.close()
                time.sleep(1.0)  # Wait before retry

            except Exception as e:
                print(f"[CommandProcessor] Unexpected error: {e}")
                time.sleep(0.1)

    def _process_command(self, command):
        """Process incoming command from GUI"""
        print(f"[CommandProcessor] Received: {command}")

        # first try new DIR style commands
        dir_match = self.dir_pattern.search(command)
        if dir_match:
            dir_str, speed_str, fwd_str = dir_match.groups()
            try:
                direction = dir_str.lower()
                speed = float(speed_str)
                forward = float(fwd_str)
                if not (0 <= speed <= 1.0) or not (0 <= forward <= 1.0):
                    print(f"[CommandProcessor] Invalid magnitudes speed={speed}, forward={forward}")
                    return
                self.motor_controller.process_direction_command(direction, speed, forward)
            except ValueError as e:
                print(f"[CommandProcessor] Invalid direction command values: {e}")
            return

        # Parse angle and speed command
        angle_speed_match = self.angle_speed_pattern.search(command)
        if angle_speed_match:
            angle_str, speed_str = angle_speed_match.groups()
            try:
                angle = float(angle_str)
                speed = float(speed_str)

                # Validate ranges
                if not (0 <= speed <= 1.0):
                    print(f"[CommandProcessor] Invalid speed: {speed}")
                    return

                # Process direction command
                self.motor_controller.process_direction_command(angle, speed)

            except ValueError as e:
                print(f"[CommandProcessor] Invalid angle/speed values: {e}")
            return

        # Parse capture command
        capture_match = self.capture_pattern.search(command)
        if capture_match:
            self._process_capture_command()
            return

        # Unknown command
        print(f"[CommandProcessor] Unknown command: {command}")

    def _process_capture_command(self):
        """Process capture command (object detection/targeting)"""
        print("[CommandProcessor] Processing capture command")

        # after capture we want the arm to return along the same forward trajectory
        self.motor_controller.retrace_forward_history()

        # additional capture handling could go here (e.g. operate tentacle motors)

    def get_status(self):
        """Get system status"""
        return {
            'uart_connected': self.serial and self.serial.is_open,
            'motor_controller': self.motor_controller.get_status(),
            'running': self.running
        }

    def send_response(self, message):
        """Send response back to GUI (if needed)"""
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(f"{message}\n".encode())
            except Exception as e:
                print(f"[CommandProcessor] Send response failed: {e}")


def main():
    """Main entry point for command processor"""
    # Default configuration - adjust for your setup
    processor = CommandProcessor(
        uart_port=UART_PORT,
        uart_baudrate=UART_BAUDRATE,
        pwm_addr=PWM_GENERATOR_ADDRESS,
        gpio1_addr=GPIO_EXPANDER_1_ADDRESS,
        gpio2_addr=GPIO_EXPANDER_2_ADDRESS,
        slave_rpi_addr=SLAVE_RPI_ADDRESS
    )

    try:
        processor.start()

        # Keep running until interrupted
        while True:
            time.sleep(1.0)

            # Print status every 10 seconds
            status = processor.get_status()
            if status['running']:
                print("[CommandProcessor] System running - UART:", "Connected" if status['uart_connected'] else "Disconnected")

    except KeyboardInterrupt:
        print("\n[CommandProcessor] Shutdown requested")
    except Exception as e:
        print(f"[CommandProcessor] Fatal error: {e}")
    finally:
        processor.stop()


if __name__ == "__main__":
    main()