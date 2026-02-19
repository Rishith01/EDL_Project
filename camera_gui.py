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
    keyPressed = pyqtSignal(int)
    mouseMoved = pyqtSignal(int, int)
    mouseClicked = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
    
    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            self.keyPressed.emit(event.key())

    def mouseMoveEvent(self, event):
        self.mouseMoved.emit(event.x(), event.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseClicked.emit(event.x(), event.y())
class CameraGUI(QMainWindow):
    """Main GUI window for arm control with camera feed"""
    
    def __init__(self, rpi_port='COM3', rpi_baudrate=9600):
        super().__init__()
        self.setWindowTitle("Robotic Arm Camera Control")
        self.setMinimumSize(800, 600)
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
        
        self.image_label.mouseMoved.connect(self.on_mouse_moved)
        self.image_label.mouseClicked.connect(self.on_mouse_clicked)

        # Timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # ~30 FPS (1000ms / 30)

        # Detect and initialize camera
        self.detect_cameras()
        if self.available_cameras:
            self.cap = cv2.VideoCapture(self.available_cameras[0], cv2.CAP_DSHOW)
            self.current_camera_index = self.available_cameras[0]

    def on_mouse_moved(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
        
    def on_mouse_clicked(self, x, y):
        """Handle mouse click to determine section"""
        if self.label_width == 0 or self.label_height == 0:
            return
        
        # Center of display
        cx = self.label_width // 2
        cy = self.label_height // 2
        
        # Vector from center to click
        dx = x - cx
        dy = cy - y  # Invert Y
        
        if dx == 0 and dy == 0:
            section = "center"
        else:
            angle = math.degrees(math.atan2(dy, dx))
            if angle < 0:
                angle += 360
            
            # Determine section
            if 0 <= angle < 22.5 or 337.5 <= angle < 360:
                section = "right"
            elif 22.5 <= angle < 67.5:
                section = "up-right"
            elif 67.5 <= angle < 112.5:
                section = "up"
            elif 112.5 <= angle < 157.5:
                section = "up-left"
            elif 157.5 <= angle < 202.5:
                section = "left"
            elif 202.5 <= angle < 247.5:
                section = "down-left"
            elif 247.5 <= angle < 292.5:
                section = "down"
            elif 292.5 <= angle < 337.5:
                section = "down-right"
        
        print(f"[Click] Section: {section} (angle: {angle:.1f}°)")
        
    def _setup_ui(self):
        """Setup user interface components"""
        # Title label
        title_label = QLabel("Robotic Arm Camera Control")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin: 10px;
                padding: 5px;
            }
        """)

        # Camera feed display
        self.image_label = CameraLabel(self)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: black;
            }
        """)
        self.image_label.keyPressed.connect(self.on_key_pressed)

        # Camera selector
        self.camera_selector = QComboBox()
        self.camera_selector.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #34495e;
                margin-right: 10px;
            }
        """)
        self.camera_selector.currentIndexChanged.connect(self.on_camera_changed)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.image_label, 1)
        layout.addWidget(self.camera_selector, 0, Qt.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
            }
        """)
        self.setCentralWidget(container)

    def detect_cameras(self):
        """Detect available cameras connected to system"""
        self.available_cameras = []
        for i in range(2):  # Check cameras 0-1
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
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
            self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
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

    def compute_direction(self):
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

    def update_frame(self):
        """Update camera frame and display with overlay"""
        if self.cap is None or not self.cap.isOpened():
            return
        
        ret, frame = self.cap.read()
        if not ret:
            print("[Camera] Failed to read frame")
            return

        self.frame = frame.copy()
        frame_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w = frame_display.shape[:2]

        # Create QImage from frame
        bytes_per_line = 3 * w
        qimg = QImage(frame_display.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Scale pixmap to fit label while maintaining aspect ratio
        pixmap = QPixmap.fromImage(qimg)
        if self.image_label.width() == 0 or self.image_label.height() == 0:
            return

        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
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

        painter.end()

        self.image_label.setPixmap(scaled_pixmap)
        self.label_width = scaled_pixmap.width()
        self.label_height = scaled_pixmap.height()

        # Compute and send direction to RPi
        angle, speed = self.compute_direction()
        self.uart_handler.send_command(angle, speed)

    def resizeEvent(self, event):
        """Handle window resize to update display immediately"""
        super().resizeEvent(event)
        # Force an immediate frame update when resized
        if self.cap and self.cap.isOpened():
            self.update_frame()

    def closeEvent(self, event):
        """Cleanup resources on window close"""
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.uart_handler.disconnect()
        event.accept()
