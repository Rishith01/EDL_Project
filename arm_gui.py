"""
Alternative entry point for Robotic Arm Control Application
This file can be used to launch the GUI directly or run tests
"""

import sys
from PyQt5.QtWidgets import QApplication
from camera_gui import CameraGUI


def run_gui(rpi_port='COM3', rpi_baudrate=9600):
    """
    Launch the GUI application
    
    Args:
        rpi_port (str): Serial port name (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
        rpi_baudrate (int): Baud rate for UART communication
    """
    app = QApplication(sys.argv)
    window = CameraGUI(rpi_port=rpi_port, rpi_baudrate=rpi_baudrate)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Configure RPi UART connection details
    RPi_PORT = 'COM5'      # Change to your serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
    RPi_BAUDRATE = 9600    # Change to your RPi UART baud rate
    
    run_gui(rpi_port=RPi_PORT, rpi_baudrate=RPi_BAUDRATE)
