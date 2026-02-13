"""
Alternative entry point for Robotic Arm Control Application
This file can be used to launch the GUI directly or run tests
"""

import sys
from PyQt5.QtWidgets import QApplication
from camera_gui import CameraGUI


def run_gui(rpi_host='192.168.1.100', rpi_port=5000):
    """
    Launch the GUI application
    
    Args:
        rpi_host (str): RPi IP address
        rpi_port (int): RPi server port
    """
    app = QApplication(sys.argv)
    window = CameraGUI(rpi_host=rpi_host, rpi_port=rpi_port)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Configure RPi connection details
    RPi_HOST = '192.168.1.100'  # Change to your RPi IP address
    RPi_PORT = 5000              # Change to your RPi server port
    
    run_gui(rpi_host=RPi_HOST, rpi_port=RPi_PORT)
