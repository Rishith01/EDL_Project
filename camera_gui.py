"""
Camera GUI Module for Robotic Arm Control
Handles video capture, display, and user input
"""

import cv2
import math
import threading
from PyQt5.QtWidgets import (
    QLabel, QMainWindow, QComboBox, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen

from uart_handler import UartHandler


class CameraLabel(QLabel):
    """Custom QLabel that captures keyboard events and mouse tracking"""
    keyPressed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
    
    def keyPressEvent(self, event):
        """Emit signal on key press"""
        if not event.isAutoRepeat():  # Ignore auto-repeat
            self.keyPressed.emit(event.key())


class CameraGUI(QMainWindow):
    """Main GUI window for arm control with camera feed"""
    
    def __init__(self, rpi_port='COM3', rpi_baudrate=9600):
        super().__init__()
        self.setWindowTitle("Robotic Arm Control Interface")
        self.resize(1000, 750)

        # Camera properties
        self.cap = None
        self.frame = None
        self.available_cameras = []
        self.current_camera_index = 0

        # Mouse tracking
        self.mouse_x = 0
        self.mouse_y = 0
        self.label_width = 0
        self.label_height = 0

        # Capture region
        self.captured_roi = None

        # UART communication
        self.uart_handler = UartHandler(rpi_port, rpi_baudrate)
        self.uart_handler.connection_status.connect(self.on_connection_status)
        
        # Start UART connection in background thread
        self.uart_thread = threading.Thread(target=self.uart_handler.connect, daemon=True)
        self.uart_thread.start()

        # UI Setup
        self._setup_ui()

        # Timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # ~30 FPS (1000ms / 30)

        # Detect and initialize camera
        self.detect_cameras()
        if self.available_cameras:
            self.cap = cv2.VideoCapture(self.available_cameras[0])

    def _setup_ui(self):
        """Setup user interface components"""
        # Camera feed display
        self.image_label = CameraLabel(self)
        self.image_label.keyPressed.connect(self.on_key_pressed)

        # Camera selector
        self.camera_selector = QComboBox()
        self.camera_selector.currentIndexChanged.connect(self.on_camera_changed)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label, 1)
        layout.addWidget(self.camera_selector)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def detect_cameras(self):
        """Detect available cameras connected to system"""
        self.available_cameras = []
        for i in range(5):  # Check cameras 0-4
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.available_cameras.append(i)
                cap.release()
        
        if not self.available_cameras:
            QMessageBox.warning(self, "Error", "No cameras detected!")
            return
        
        # Populate combobox
        camera_names = [f"Camera {i}" for i in self.available_cameras]
        self.camera_selector.blockSignals(True)
        self.camera_selector.addItems(camera_names)
        self.camera_selector.blockSignals(False)
        
        print(f"[Camera] Detected cameras: {self.available_cameras}")

    def on_camera_changed(self, index):
        """Handle camera selection change"""
        if index < 0 or index >= len(self.available_cameras):
            return
        
        self.change_camera(self.available_cameras[index])

    def change_camera(self, camera_index):
        """Switch to a different camera"""
        try:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                raise Exception("Camera failed to open")
            self.current_camera_index = camera_index
            print(f"[Camera] Switched to Camera {camera_index}")
        except Exception as e:
            print(f"[Camera] Error: {e}")
            QMessageBox.critical(self, "Camera Error", f"Failed to open camera: {e}")

    def on_connection_status(self, connected):
        """Handle RPi UART connection status updates"""
        status = "🟢 Connected" if connected else "🔴 Disconnected"
        print(f"[Connection] RPi UART: {status}")

    def on_key_pressed(self, key):
        """Handle keyboard input events"""
        if key == Qt.Key_K:
            self.capture_object()
        elif key == Qt.Key_Escape:
            self.close()

    def capture_object(self):
        """Capture object at current mouse position"""
        if self.frame is None:
            print("[Capture] No frame available")
            return
        
        h, w = self.frame.shape[:2]
        
        # Map label coordinates to frame coordinates
        frame_x = int(self.mouse_x * w / self.label_width) if self.label_width > 0 else w // 2
        frame_y = int(self.mouse_y * h / self.label_height) if self.label_height > 0 else h // 2
        
        # Clamp to frame bounds
        frame_x = max(0, min(frame_x, w - 1))
        frame_y = max(0, min(frame_y, h - 1))

        size = 60
        x1 = max(0, frame_x - size)
        y1 = max(0, frame_y - size)
        x2 = min(w, frame_x + size)
        y2 = min(h, frame_y + size)

        self.captured_roi = self.frame[y1:y2, x1:x2].copy()
        print(f"[Capture] Object captured at ({frame_x}, {frame_y})")
        
        # Send capture command to RPi
        self.uart_handler.send_capture(frame_x, frame_y)

    def compute_direction(self, w, h):
        """
        Calculate arm direction based on mouse position
        
        Returns:
            tuple: (angle in radians, speed magnitude 0.0-1.0)
        """
        # Center of display
        label_cx = self.label_width // 2
        label_cy = self.label_height // 2
        
        # Vector from center to mouse
        dx = self.mouse_x - label_cx
        dy = label_cy - self.mouse_y  # Invert Y for correct coordinate system

        angle = math.atan2(dy, dx)
        magnitude = math.sqrt(dx*dx + dy*dy)
        max_dist = math.sqrt(label_cx*label_cx + label_cy*label_cy)
        speed = min(magnitude / max_dist, 1.0) if max_dist > 0 else 0.0

        return angle, speed

    def mouseMoveEvent(self, event):
        """Track global mouse movement within application"""
        # Get label position relative to screen
        label_global_x = self.image_label.mapToGlobal(0, 0).x()
        label_global_y = self.image_label.mapToGlobal(0, 0).y()
        
        global_x = event.globalX()
        global_y = event.globalY()
        
        # Convert to label-relative coordinates
        self.mouse_x = global_x - label_global_x
        self.mouse_y = global_y - label_global_y
        
        # Clamp to label bounds
        self.mouse_x = max(0, min(self.mouse_x, self.label_width))
        self.mouse_y = max(0, min(self.mouse_y, self.label_height))

    def update_frame(self):
        """Update camera frame and display with overlay"""
        if self.cap is None or not self.cap.isOpened():
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return

        self.frame = frame.copy()
        frame_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w = frame_display.shape[:2]

        # Create QImage from frame
        bytes_per_line = 3 * w
        qimg = QImage(frame_display.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Scale pixmap to fit label while maintaining aspect ratio
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label.height(), Qt.SmoothTransformation)
        
        # Draw overlay graphics
        painter = QPainter(scaled_pixmap)
        pen = QPen(Qt.red, 2)
        painter.setPen(pen)

        # Crosshair at mouse position
        crosshair_size = 15
        painter.drawLine(self.mouse_x - crosshair_size, self.mouse_y, 
                        self.mouse_x + crosshair_size, self.mouse_y)
        painter.drawLine(self.mouse_x, self.mouse_y - crosshair_size, 
                        self.mouse_x, self.mouse_y + crosshair_size)

        # Direction vector from center to mouse
        label_cx = scaled_pixmap.width() // 2
        label_cy = scaled_pixmap.height() // 2
        painter.drawLine(label_cx, label_cy, self.mouse_x, self.mouse_y)

        painter.end()

        self.image_label.setPixmap(scaled_pixmap)
        self.label_width = scaled_pixmap.width()
        self.label_height = scaled_pixmap.height()

        # Compute and send direction to RPi
        angle, speed = self.compute_direction(w, h)
        self.uart_handler.send_command(angle, speed)

    def closeEvent(self, event):
        """Cleanup resources on window close"""
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.uart_handler.disconnect()
        event.accept()
