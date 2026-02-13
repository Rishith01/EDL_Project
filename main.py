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
    - RPi IP address and port can be modified here
    """
    app = QApplication(sys.argv)
    
    # Configure RPi connection details
    RPi_HOST = '192.168.1.100'  # Change to your RPi IP address
    RPi_PORT = 5000              # Change to your RPi server port
    
    # Create and show main window
    window = CameraGUI(rpi_host=RPi_HOST, rpi_port=RPi_PORT)
    window.show()
    
    print("[App] Robotic Arm Control Interface started")
    print(f"[App] RPi connection configured: {RPi_HOST}:{RPi_PORT}")
    print("[App] Controls:")
    print("  - Mouse: Move pointer to control arm direction")
    print("  - K key: Capture object at mouse position")
    print("  - ESC key: Exit application")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
