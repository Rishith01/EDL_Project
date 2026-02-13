"""
Test module for GUI Components
Tests GUI without network communication
"""

import sys
import cv2
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from camera_gui import CameraGUI, CameraLabel


def test_camera_gui():
    """Test GUI components and functionality"""
    print("=" * 60)
    print("Camera GUI Test")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    
    # Test 1: Create GUI instance
    print("\n[Test 1] Creating CameraGUI instance...")
    # Using localhost - this will fail to connect to RPi (expected)
    gui = CameraGUI(rpi_host='127.0.0.1', rpi_port=5000)
    print("  ✓ GUI instance created successfully")
    
    # Test 2: Check GUI properties
    print("\n[Test 2] Checking GUI properties...")
    print(f"  - Window title: {gui.windowTitle()}")
    print(f"  - Window size: {gui.width()}x{gui.height()}")
    print(f"  - Available cameras: {gui.available_cameras}")
    print(f"  - Camera selector items: {[gui.camera_selector.itemText(i) for i in range(gui.camera_selector.count())]}")
    
    # Test 3: Test mouse position calculation
    print("\n[Test 3] Testing mouse position tracking...")
    gui.mouse_x = 100
    gui.mouse_y = 100
    gui.label_width = 800
    gui.label_height = 600
    angle, speed = gui.compute_direction(640, 480)
    print(f"  - Mouse position: ({gui.mouse_x}, {gui.mouse_y})")
    print(f"  - Label size: {gui.label_width}x{gui.label_height}")
    print(f"  - Computed angle: {angle:.2f} rad")
    print(f"  - Computed speed: {speed:.2f}")
    
    # Test 4: Test keyboard label
    print("\n[Test 4] Testing CameraLabel...")
    label = CameraLabel(gui)
    print(f"  - Focus policy: {label.focusPolicy()}")
    print(f"  - Mouse tracking: {label.hasMouseTracking()}")
    
    # Test 5: Show window briefly
    print("\n[Test 5] Displaying GUI window (10 seconds)...")
    gui.show()
    print("  ✓ GUI window opened")
    print("  - Testing frame update for 10 seconds...")
    
    # Run event loop for 10 seconds
    QTimer.singleShot(10000, app.quit)
    app.exec_()
    
    print("  ✓ Event loop completed")
    
    print("\n" + "=" * 60)
    print("Camera GUI Test Completed")
    print("=" * 60)


if __name__ == "__main__":
    test_camera_gui()
