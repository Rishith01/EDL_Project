"""
UART Handler for Robotic Arm Control
Handles communication with RPi over UART in a thread-safe manner
"""

import serial
import threading
from PyQt5.QtCore import QObject, pyqtSignal


class UartHandler(QObject):
    """Handles UART serial communication with RPi in a separate thread"""
    connection_status = pyqtSignal(bool)  # Signal: True=connected, False=disconnected
    
    def __init__(self, port='COM3', baudrate=9600):
        """
        Initialize UART handler
        
        Args:
            port (str): Serial port name (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate (int): Baud rate for serial communication (default: 9600)
        """
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.is_connected = False
        self.lock = threading.Lock()
    
    def connect(self):
        """
        Open UART serial connection to RPi
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1.0,
                write_timeout=1.0
            )
            self.is_connected = True
            self.connection_status.emit(True)
            print(f"[UART] Connected to RPi on {self.port} at {self.baudrate} baud")
            return True
        except Exception as e:
            print(f"[UART] Connection failed: {e}")
            self.is_connected = False
            self.connection_status.emit(False)
            return False
    
    def send_command(self, angle, speed):
        """
        Send arm direction command to RPi
        Format: ANGLE:<angle>,SPEED:<speed>
        
        Args:
            angle (float): Direction angle in radians
            speed (float): Speed magnitude (0.0 to 1.0)
        """
        if not self.is_connected or self.serial is None:
            return
        
        try:
            with self.lock:
                message = f"ANGLE:{angle:.2f},SPEED:{speed:.2f}\n"
                self.serial.write(message.encode())
        except Exception as e:
            print(f"[UART] Send command failed: {e}")
            self.is_connected = False
            self.connection_status.emit(False)
    
    def send_capture(self, x, y):
        """
        Send capture command with position to RPi
        Format: CAPTURE:<x>,<y>
        
        Args:
            x (int): X coordinate in frame
            y (int): Y coordinate in frame
        """
        if not self.is_connected or self.serial is None:
            return
        
        try:
            with self.lock:
                message = f"CAPTURE:{x},{y}\n"
                self.serial.write(message.encode())
                print(f"[UART] Capture command sent: ({x}, {y})")
        except Exception as e:
            print(f"[UART] Send capture failed: {e}")
            self.is_connected = False
            self.connection_status.emit(False)
    
    def disconnect(self):
        """Close serial connection"""
        if self.serial:
            try:
                if self.serial.is_open:
                    self.serial.close()
                print("[UART] Disconnected")
            except:
                pass
            self.socket = None
            self.is_connected = False
