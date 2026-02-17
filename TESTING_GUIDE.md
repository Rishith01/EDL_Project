# Testing Guide - Independent Subtask Testing

This guide explains how to test each component independently to verify functionality.

## File Structure

```
EDL_Project/
├── Main Application Files:
│   ├── uart_handler.py       # UART communication (renamed from socket_handler.py)
│   ├── camera_gui.py         # Main GUI with camera
│   ├── main.py               # Entry point
│   └── arm_gui.py            # Alternative entry point
│
├── Independent Test Files:
│   ├── test_uart_handler.py  # Test UART communication
│   ├── test_camera.py        # Test camera detection and capture
│   ├── test_direction.py     # Test direction/speed calculation
│   ├── test_gui.py           # Test GUI components
│   └── run_tests.py          # Run all tests together
│
└── README.md                 # Original project documentation
```

## Quick Start

### Run All Tests
```bash
python run_tests.py
```

### Run Individual Tests

#### 1. Test UART Communication (Without Camera or GUI)
```bash
python test_uart_handler.py
```

**What it tests:**
- ✓ UART handler initialization
- ✓ Connection to serial port
- ✓ Sending direction commands (ANGLE, SPEED)
- ✓ Sending capture commands (CAPTURE X,Y)
- ✓ Message format validation
- ✓ Disconnect cleanup

**Expected output:**
```
[Test 1] Creating UART handler...
✓ Handler created successfully

[Test 2] Testing UART connection...
✗ Connection failed (expected if RPi not connected)  ← This is OK if RPi not plugged in

[Test 5] Testing message formats...
✓ Command format correct: ANGLE:0.45,SPEED:0.60
✓ Capture format correct: CAPTURE:100,200
```

---

#### 2. Test Camera Detection & Capture (Without UART or GUI)
```bash
python test_camera.py
```

**What it tests:**
- ✓ Camera detection (finds which cameras are available)
- ✓ Camera properties (resolution, FPS, brightness, contrast)
- ✓ Frame capture from camera
- ✓ Frame rate measurement (actual FPS)
- ✓ Color format conversion (BGR → RGB)
- ✓ Region of Interest (ROI) extraction
- ✓ Multiple camera switching

**Expected output:**
```
[Test 1] Detecting available cameras...
✓ Camera 0 available
Found 1 camera(s): [0]

[Test 3] Capturing frame...
✓ Frame captured:
  - Shape: 640x480x3
  - Data type: uint8

[Test 4] Measuring frame rate (30 frames)...
✓ Actual FPS: 29.5
```

---

#### 3. Test Direction & Speed Calculation (Pure Math - No Hardware)
```bash
python test_direction.py
```

**What it tests:**
- ✓ Mouse at center = zero speed
- ✓ Direction calculation to different angles
- ✓ Speed increases with distance from center
- ✓ Speed capped at 1.0
- ✓ All four quadrants (up, down, left, right)
- ✓ Diagonal directions
- ✓ UART message format generation

**Expected output:**
```
[Test 1] Mouse at center position...
  Position: (320, 240)
  Angle: 0.0000 rad (0.00°)
  Speed: 0.0000
✓ Center position test passed

[Test 2] Mouse to the right...
  Angle: 0.0000 rad (0.00°)
  Speed: 0.3300
✓ Right direction test passed

[Test 6] Speed capped at maximum (1.0)...
  Speed: 1.0000
✓ Speed capping test passed
```

**Use this to verify:**
- Mouse click at screen center → speed should be 0
- Mouse click to right → angle ≈ 0°
- Mouse click up → angle ≈ 90°
- Speed increases as you move further from center
- Far click beyond screen → speed ≈ 1.0

---

#### 4. Test GUI Components (Window, Layout, Interactions)
```bash
python test_gui.py
```

**What it tests:**
- ✓ GUI window creation
- ✓ Camera detection integration
- ✓ Widget layout (labels, dropdowns)
- ✓ Direction computation
- ✓ ROI calculation
- ✓ Frame update timer
- ✓ Optional: Live display for 5 seconds

**Expected output:**
```
[Test 1] Creating CameraLabel...
✓ CameraLabel created

[Test 2] Initializing CameraGUI...
✓ GUI instance created
  - Title: Robotic Arm Control Interface
  - Size: 1000x750

[Test 3] Checking camera detection...
✓ Camera detection results:
  - Cameras found: [0]
```

**When prompted for display test (optional):**
```
Run GUI display test? (y/n, default=n): y
[Test 7] Running GUI with display (5 seconds)...
✓ GUI window displayed
```
This will open the GUI window for 5 seconds so you can verify:
- Camera feed displays
- Crosshair follows your mouse
- Dropdown menu works
- Window closes properly

---

## Troubleshooting & Common Issues

### UART Test Fails: "Connection failed"
**Cause:** RPi not connected or COM port wrong
```bash
# Check what COM ports are available (Windows):
# Device Manager → Ports (COM & LPT)

# Update in main.py:
RPi_PORT = 'COM3'  # ← Change to your actual port
```

### Camera Test Fails: "No cameras detected!"
**Cause:** USB camera not connected or driver issue
```bash
# On Windows, check:
# Device Manager → Imaging devices

# Try different indices (some systems use 1 instead of 0):
# Edit test_camera.py line: for i in range(5):  # Tries 0,1,2,3,4
```

### Direction Test Fails: Assertion errors
**Cause:** Math calculations incorrect
```bash
# Check the actual vs expected values in output
# If speeds don't increment properly, review the distance calculation
# If angles are off, check the coordinate system (Y is inverted)
```

### GUI Test Fails: "GUI instance creation failed"
**Cause:** PyQt5 not installed or broken
```bash
# Reinstall PyQt5:
pip install --upgrade PyQt5
```

---

## Test Execution Workflow

### Scenario 1: Verify Each Component is Working
1. Start with **test_direction.py** (no hardware needed)
   - Confirms math calculations are correct
2. Run **test_camera.py** (camera needed)
   - Confirms USB camera works
3. Run **test_uart_handler.py** (UART/RPi needed)
   - Confirms serial communication works
4. Run **test_gui.py** (all above needed)
   - Confirms everything works together

### Scenario 2: Diagnose Communication Problems
```bash
# Is the math wrong?
python test_direction.py

# Is the camera not working?
python test_camera.py

# Is UART communication failing?
python test_uart_handler.py

# If UART fails, check:
# - USB cable connected
# - COM port in Device Manager
# - Correct port number in config
# - RPi powered on and UART enabled
# - Matching baud rate (9600)
```

### Scenario 3: Before Running Main Application
```bash
# Quick verification of all systems:
python run_tests.py

# All tests should show:
# - Direction: ✓ PASSED
# - Camera: ✓ PASSED (or skip if urgent)
# - UART: ✗ FAILED is OK if RPi not connected
# - GUI: ✓ PASSED
```

---

## Message Formats (For Debugging)

### Direction Command
```
ANGLE:0.45,SPEED:0.75\n
```
Sent continuously as mouse moves. Angle in radians, speed 0.0-1.0

### Capture Command
```
CAPTURE:320,240\n
```
Sent when K key pressed. X,Y are pixel coordinates in the frame

---

## Modular Code Structure

Key principle: **Each component can be tested independently**

```
UART ← Sends commands → RPi UART Module
↑
Camera GUI ← Gets frame → USB Camera
↑
Direction ← Calculates angle/speed ← Mouse Position
```

### Pure Functions (No External Dependencies)
- `compute_direction()` - Math only, no hardware needed
- `UartHandler.send_command()` - Just formatting, tests message format

### Hardware-Dependent
- `test_camera.py` - Needs USB camera
- `test_uart_handler.py` - Needs UART device/RPi
- `test_gui.py` - Needs display server

### Integrations
- `camera_gui.py` - Combines GUI + Camera + UART

---

## Summary

Use this testing approach to:
1. ✓ Verify each subtask independently
2. ✓ Identify exactly where problems occur
3. ✓ Test without requiring all hardware
4. ✓ Debug mathematical calculations
5. ✓ Validate message formats
6. ✓ Confirm hardware connections

**Start with:** `python test_direction.py` → `python test_camera.py` → `python test_uart_handler.py` → `python test_gui.py`
