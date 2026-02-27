"""
Test module for GUI - INDEPENDENT GUI TEST
Tests GUI initialization, layout, and interaction independently
Usage: python test_gui.py
"""

import sys
import cv2
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from camera_gui import CameraGUI, CameraLabel


def test_camera_label_creation():
    """Test 1: CameraLabel widget creation"""
    print("\n[Test 1] Creating CameraLabel...")
    app = QApplication.instance() or QApplication(sys.argv)
    
    label = CameraLabel()
    print(f"  ✓ CameraLabel created")
    print(f"    - Focus policy: Strong")
    print(f"    - Mouse tracking: Enabled")
    assert label.hasMouseTracking(), "Mouse tracking should be enabled"


def test_gui_initialization():
    """Test 2: GUI instance creation"""
    print("\n[Test 2] Initializing CameraGUI...")
    app = QApplication.instance() or QApplication(sys.argv)
    
    # Note: UART connection will fail (expected with dummy port)
    gui = CameraGUI(rpi_port='COM5', rpi_baudrate=9600)
    print(f"  ✓ GUI instance created")
    print(f"    - Title: {gui.windowTitle()}")
    print(f"    - Size: {gui.width()}x{gui.height()}")
    gui.close()


def test_gui_camera_detection():
    """Test 3: Camera detection in GUI"""
    print("\n[Test 3] Checking camera detection...")
    app = QApplication.instance() or QApplication(sys.argv)
    
    gui = CameraGUI(rpi_port='COM5', rpi_baudrate=9600)
    gui.close()
    print(f"  ✓ Camera detection results:")
    print(f"    - Cameras found: {gui.available_cameras}")
    print(f"    - Dropdown items: {gui.camera_selector.count()}")
    
    # Check if cameras are listed in dropdown
    for i in range(gui.camera_selector.count()):
        item_text = gui.camera_selector.itemText(i)
        print(f"    - Item {i}: {item_text}")


def test_gui_properties():
    """Test 4: GUI component properties"""
    print("\n[Test 4] Checking GUI properties...")
    app = QApplication.instance() or QApplication(sys.argv)
    
    gui = CameraGUI(rpi_port='COM5', rpi_baudrate=9600)
    print(f"  ✓ Component properties:")
    print(f"    - Image label visible: {gui.image_label.isVisible()}")
    print(f"    - Camera selector visible: {gui.camera_selector.isVisible()}")
    print(f"    - Timer active: {gui.timer.isActive()}")
    print(f"    - Initial mouse position: ({gui.mouse_x}, {gui.mouse_y})")
    gui.close()


def test_direction_computation():
    """Test 5: Direction computation"""
    print("\n[Test 5] Testing direction computation...")
    app = QApplication.instance() or QApplication(sys.argv)
    
    gui = CameraGUI(rpi_port='COM5', rpi_baudrate=9600)
    gui.close()
    # Setup test conditions
    gui.label_width = 800
    gui.label_height = 600
    frame_width = 640
    frame_height = 480
    
    test_cases = [
        ("Center", 400, 300, "Small speed"),
        ("Far right", 750, 300, "Higher speed to right"),
        ("Up", 400, 100, "Higher speed upward"),
        ("Diagonal", 750, 100, "Diagonal direction"),
    ]
    
    for name, mouse_x, mouse_y, desc in test_cases:
        gui.on_mouse_moved(mouse_x, mouse_y)
        angle, speed = gui.compute_direction()
        print(f"    - {name}: angle={angle:.2f}rad, speed={speed:.2f} ({desc})")


def test_capture_roi_calculation():
    """Test 6: ROI (Region of Interest) calculation"""
    print("\n[Test 6] Testing ROI calculation...")
    app = QApplication.instance() or QApplication(sys.argv)
    
    gui = CameraGUI(rpi_port='COM5', rpi_baudrate=9600)
    gui.close()
    
    gui.mouse_x = 320
    gui.mouse_y = 240
    gui.label_width = 800
    gui.label_height = 600
    
    # Simulate capture coordinates
    h, w = 480, 640
    frame_x = int(gui.mouse_x * w / gui.label_width)
    frame_y = int(gui.mouse_y * h / gui.label_height)
    
    size = 60
    x1 = max(0, frame_x - size)
    y1 = max(0, frame_y - size)
    x2 = min(w, frame_x + size)
    y2 = min(h, frame_y + size)
    
    print(f"  ✓ ROI calculation:")
    print(f"    - Mouse position: ({gui.mouse_x}, {gui.mouse_y})")
    print(f"    - Frame coordinates: ({frame_x}, {frame_y})")
    print(f"    - ROI bounds: ({x1},{y1}) to ({x2},{y2})")
    

def test_gui_with_display(duration_seconds=10):
    """Test 7: GUI display and event loop"""
    print(f"\n[Test 7] Running GUI with display ({duration_seconds} seconds)...")
    app = QApplication.instance() or QApplication(sys.argv)
    
    gui = CameraGUI(rpi_port='COM5', rpi_baudrate=9600)
    gui.close()
    gui.show()
    print(f"  ✓ GUI window displayed")
    print(f"    - Frame update timer running")
    print(f"    - Running event loop...")
    
    # Close after specified duration
    QTimer.singleShot(duration_seconds * 1000, app.quit)
    app.exec_()
    gui.close()
    
    print(f"  ✓ Event loop completed after {duration_seconds} seconds")


if __name__ == "__main__":
    print("=" * 70)
    print("GUI Independent Tests")
    print("Tests GUI initialization, components, and display")
    print("=" * 70)
    
    try:
        test_camera_label_creation()
        test_gui_initialization()
        test_gui_camera_detection()
        test_gui_properties()
        test_direction_computation()
        test_capture_roi_calculation()
        
        # Optional: test with display (comment out if you don't want GUI window)
        # response = input("\nRun GUI display test? (y/n, default=n): ").strip().lower()
        # if response == 'y':
        test_gui_with_display(duration_seconds=10)
        # else:
        #     print("  - Skipping display test")
        
        print("\n" + "=" * 70)
        print("✓ All GUI tests completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
