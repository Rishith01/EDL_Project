"""
Main entry point for Robotic Arm Control Application
Initializes PyQt5 application and launches the GUI
"""

import sys
from PyQt5.QtWidgets import QApplication
from camera_gui import CameraGUI


def main():
    """
    Initialize and run the application
    
    Configuration:
    - UART Port and baud rate can be modified here
    """
    app = QApplication(sys.argv)
    
    # Configure RPi UART connection details
    RPi_PORT = 'COM3'      # Change to your serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
    RPi_BAUDRATE = 9600    # Change to your RPi UART baud rate
    
    # Create and show main window
    window = CameraGUI(rpi_port=RPi_PORT, rpi_baudrate=RPi_BAUDRATE)
    window.show()
    
    print("[App] Robotic Arm Control Interface started")
    print(f"[App] RPi UART connection configured: {RPi_PORT} at {RPi_BAUDRATE} baud")
    print("[App] Controls:")
    print("  - Mouse: Move pointer to control arm direction")
    print("  - K key: Capture object at mouse position")
    print("  - ESC key: Exit application")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
