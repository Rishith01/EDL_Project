"""
UART Handler for Robotic Arm Control
Handles communication with RPi over UART in a thread-safe manner
"""

import serial
import threading
from PyQt5.QtCore import QObject, pyqtSignal


class UARTHandler(QObject):
    """Handles UART serial communication with RPi in a separate thread"""
    connection_status = pyqtSignal(bool)  # Signal: True=connected, False=disconnected
    
    def __init__(self, port='COM5', baudrate=9600):
        """
        Initialize UART handler
        
        Args:
            port (str): Serial port name (e.g., 'COM5' on Windows, '/dev/ttyUSB0' on Linux)
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
        Legacy command sender. Still available for backward compatibility.
        Format: ANGLE:<angle>,SPEED:<speed>\n
        Args:
            angle (float): Direction angle in radians
            speed (float): Speed magnitude (0.0 to 1.0)
        """
        if not self.is_connected or self.serial is None or not self.serial.is_open:
            return

        try:
            with self.lock:
                message = f"ANGLE:{angle:.2f},SPEED:{speed:.2f}\n"
                self.serial.write(message.encode())
        except Exception as e:
            print(f"[UART] Send command failed: {e}")
            self.is_connected = False
            self.connection_status.emit(False)

    def send_movement(self, direction, speed, forward):
        """
        Send high‑level movement command to RPi.
        Format: DIR:<direction>,SPEED:<speed>,FWD:<forward>\n
        Args:
            direction (str): one of 'forward','backward','left','right','up','down'
            speed (float): lateral magnitude (0.0-1.0)
            forward (float): forward/backward component (0.0-1.0)
        """
        if not self.is_connected or self.serial is None or not self.serial.is_open:
            return

        try:
            with self.lock:
                # ensure values are in range
                s = max(0.0, min(speed, 1.0))
                f = max(0.0, min(forward, 1.0))
                message = f"DIR:{direction.upper()},SPEED:{s:.2f},FWD:{f:.2f}\n"
                self.serial.write(message.encode())
        except Exception as e:
            print(f"[UART] Send movement failed: {e}")
            self.is_connected = False
            self.connection_status.emit(False)
    
    def send_capture(self):
        """
        Send capture command to RPi
        Format: CAPTURE
        
        """
        if not self.is_connected or self.serial is None or not self.serial.is_open:
            return
        
        try:
            with self.lock:
                message = "CAPTURE\n"
                self.serial.write(message.encode())
                print("[UART] Capture command sent")
        except Exception as e:
            print(f"[UART] Send capture failed: {e}")
            self.is_connected = False
            self.connection_status.emit(False)
        
    def disconnect(self):
        """Close serial connection"""
        with self.lock:
            if self.serial:
                try:
                    if self.serial.is_open:
                        self.serial.close()
                    print("[UART] Disconnected")
                except Exception as e:
                    print(f"[UART] Disconnect error: {e}")

                self.serial = None
                self.is_connected = False
                self.connection_status.emit(False)
