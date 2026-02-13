"""
TCP Socket Handler for Robotic Arm Control
Handles communication with RPi over sockets in a thread-safe manner
"""

import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal


class SocketHandler(QObject):
    """Handles TCP socket communication with RPi in a separate thread"""
    connection_status = pyqtSignal(bool)  # Signal: True=connected, False=disconnected
    
    def __init__(self, host='192.168.1.100', port=5000):
        """
        Initialize socket handler
        
        Args:
            host (str): RPi IP address
            port (int): RPi server port
        """
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None
        self.is_connected = False
        self.lock = threading.Lock()
    
    def connect(self):
        """
        Connect to RPi server
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            self.connection_status.emit(True)
            print(f"[Socket] Connected to RPi at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"[Socket] Connection failed: {e}")
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
        if not self.is_connected or self.socket is None:
            return
        
        try:
            with self.lock:
                message = f"ANGLE:{angle:.2f},SPEED:{speed:.2f}\n"
                self.socket.sendall(message.encode())
        except Exception as e:
            print(f"[Socket] Send command failed: {e}")
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
        if not self.is_connected or self.socket is None:
            return
        
        try:
            with self.lock:
                message = f"CAPTURE:{x},{y}\n"
                self.socket.sendall(message.encode())
                print(f"[Socket] Capture command sent: ({x}, {y})")
        except Exception as e:
            print(f"[Socket] Send capture failed: {e}")
            self.is_connected = False
            self.connection_status.emit(False)
    
    def disconnect(self):
        """Close socket connection"""
        if self.socket:
            try:
                self.socket.close()
                print("[Socket] Disconnected")
            except:
                pass
            self.socket = None
            self.is_connected = False
