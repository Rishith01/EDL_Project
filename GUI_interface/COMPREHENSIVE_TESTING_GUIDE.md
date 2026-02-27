# Comprehensive Testing Guide

Complete reference for testing all components individually and together.

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Component Tests (Individual)](#component-tests-individual)
4. [Integration Testing](#integration-testing)
5. [Troubleshooting & Diagnosis](#troubleshooting--diagnosis)
6. [Common Issues & Fixes](#common-issues--fixes)

---

## Quick Start

### Run All Tests at Once
```bash
python run_tests.py
```

### Quick Troubleshooting Checklist
```bash
# Does the math work? (no hardware needed)
python test_direction.py

# Is the camera working?
python test_camera.py

# Is UART communication working?
python test_uart_handler.py

# Is the GUI working?
python test_gui.py
```

---

## Architecture Overview

### File Organization
```
EDL_Project/
├─ Core Application Files:
│  ├─ main.py                  # Entry point with UART settings
│  ├─ arm_gui.py               # Alternative entry point
│  ├─ camera_gui.py            # Main GUI + camera + UART integration
│  └─ uart_handler.py          # UART communication handler
│
├─ Independent Component Tests:
│  ├─ test_direction.py        # Pure math: angle/speed calculation
│  ├─ test_camera.py           # USB camera: detection, capture, properties
│  ├─ test_uart_handler.py     # Serial: UART connection & messaging
│  ├─ test_gui.py              # Window: GUI components & integration
│  └─ run_tests.py             # Master test runner
│
└─ Documentation:
   └─ COMPREHENSIVE_TESTING_GUIDE.md  # This file
```

### Component Dependencies
```
Direction Math (test_direction.py)
    ↓
Camera I/O (test_camera.py)
    ↓
GUI Component (test_gui.py) ← depends on above + UART
    ↓
UART Comms (test_uart_handler.py) ← independent
    ↓
Main Application (main.py, camera_gui.py)
```

**Key Principle:** Each component can be tested in isolation without dependent services present.

---

## Component Tests (Individual)

### TEST 1: Direction Calculation (`test_direction.py`)

**Dependencies:** None (pure Python math)  
**Hardware Required:** None  
**Run Time:** ~1 second

#### Command
```bash
python test_direction.py
```

#### What It Tests
| Test | Purpose | Expected Result |
|------|---------|-----------------|
| Center position | Mouse at screen center | Speed = 0.0 |
| Cardinal directions | Up/Down/Left/Right | Angles: 90°, -90°, 180°, 0° |
| Diagonal directions | 45° angles | Speed increases, angles correct |
| Speed scaling | Distance increases speed | speed(200px) > speed(50px) |
| Speed capping | Max speed is 1.0 | Far distances → 1.0 |
| All quadrants | All 4 screen regions work | Consistent angles and speeds |
| Message format | UART message structure | `ANGLE:X.XX,SPEED:Y.YY\n` |

#### Expected Output
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
```

#### Validation Criteria
- ✓ All tests pass without assertion errors
- ✓ Speed is always 0.0–1.0 range
- ✓ Angles increase with mouse movement
- ✓ Message format shows `ANGLE:` and `SPEED:` fields

---

### TEST 2: Camera Interface (`test_camera.py`)

**Dependencies:** OpenCV (`cv2`)  
**Hardware Required:** USB camera (or built-in webcam)  
**Run Time:** ~5–10 seconds

#### Command
```bash
python test_camera.py
```

#### What It Tests
| Test | Purpose | Success Criteria |
|------|---------|-----------------|
| Detection | Find available cameras | At least 1 camera found |
| Properties | Get hardware specs | Resolution, FPS, brightness |
| Frame capture | Read single frame | Frame shape and data type correct |
| Frame rate | Measure actual FPS | Close to declared FPS setting |
| Color conversion | BGR → RGB | Converted frame shape matches |
| ROI extraction | Crop region from frame | ROI coordinates within bounds |
| Multi-camera | Switch between cameras | Can access multiple indices |

#### Expected Output
```
[Test 1] Detecting available cameras...
  ✓ Camera 0 available
  Found 2 camera(s): [0, 1]

[Test 3] Capturing frame...
  ✓ Frame captured:
    - Shape: 640x480x3
    - Data type: uint8
    - Pixel value range: 10-245 (mean: 128.5)

[Test 4] Measuring frame rate (30 frames)...
  ✓ Actual FPS: 29.5
```

#### Validation Criteria
- ✓ At least 1 camera detected
- ✓ Frame resolution is reasonable (e.g., 640×480)
- ✓ Measured FPS > 20 (reasonable for USB)
- ✓ Frame pixel values in 0–255 range
- ✓ Color conversion preserves shape

#### Notes
- **Camera 0 vs Camera 1:** Often Camera 0 = built-in laptop webcam, Camera 1 = USB webcam (but not guaranteed; OS assigns indices)
- **Multiple Cameras:** If 2 cameras found, tests now run for both (as per your earlier update)
- **Errors like `Camera index out of range`:** Normal during detection probing; not a failure

---

### TEST 3: UART Handler (`test_uart_handler.py`)

**Dependencies:** `pyserial`  
**Hardware Required:** Optional—RPi with UART, USB-Serial adapter, or any device on a COM port  
**Run Time:** ~2 seconds

#### Command
```bash
python test_uart_handler.py
```

#### What It Tests
| Test | Purpose | Expected Result |
|------|---------|-----------------|
| Initialization | Create UartHandler object | Handler object created |
| Connection | Open serial connection | Connected if device present, or graceful fail |
| Send command | Send direction message | `ANGLE:X,SPEED:Y\n` format |
| Send capture | Send capture message | `CAPTURE:X,Y\n` format |
| Message formats | Validate structure | Correct delimiters and types |
| Disconnect | Close connection cleanly | Serial port closed |

#### Expected Output
```
[Test 1] Creating UART handler...
✓ Handler created successfully

[Test 2] Testing UART connection...
✗ Connection failed: [Windows Error]  ← OK if RPi not connected

[Test 5] Testing message formats...
✓ Command format correct: ANGLE:0.45,SPEED:0.60
✓ Capture format correct: CAPTURE:100,200
```

#### Validation Criteria
- ✓ Handler object created without errors
- ✓ Message formats are valid (even if connection fails)
- ✓ No exceptions thrown during send operations (silent fail is expected when disconnected)
- ✓ Connection fails gracefully if no device present

#### Important Notes
- **Expected Failure:** `Connection failed: module 'serial' has no attribute 'Serial'` means `pyserial` is not installed correctly
  ```bash
  pip uninstall pyserial -y
  pip install pyserial
  ```
- **Graceful Disconnect:** If RPi not connected, tests skip the connection test—this is normal
- **COM Port:** Default is `COM3`; change in `test_uart_handler.py` line if using different port

---

### TEST 4: GUI Components (`test_gui.py`)

**Dependencies:** PyQt5, OpenCV, camera available  
**Hardware Required:** USB camera; optional: display for visual test  
**Run Time:** ~3 seconds (or ~8 seconds with display test)

#### Command
```bash
python test_gui.py
```

#### What It Tests
| Test | Purpose | Success Criteria |
|------|---------|-----------------|
| Label creation | CameraLabel widget | Widget created, mouse tracking enabled |
| GUI initialization | CameraGUI window | Window created with correct title and size |
| Camera detection | Integration with camera test | Detected cameras listed in dropdown |
| Component properties | Widget visibility and setup | All components initialized |
| Direction computation | Math integrated in GUI | Angle and speed calculated correctly |
| ROI calculation | Capture region mapped | Coordinates within frame bounds |
| Optional display | Visual verification | Window displays, closes after 5s |

#### Expected Output
```
[Test 1] Creating CameraLabel...
  ✓ CameraLabel created
    - Focus policy: Strong
    - Mouse tracking: Enabled

[Test 2] Initializing CameraGUI...
✓ GUI instance created
    - Title: Robotic Arm Control Interface
    - Size: 1000x750

[Test 3] Checking camera detection...
  ✓ Camera detection results:
    - Cameras found: [0, 1]
    - Dropdown items: 2
    - Item 0: Camera 0
    - Item 1: Camera 1
```

#### Validation Criteria
- ✓ GUI window created with expected title
- ✓ All detected cameras shown in dropdown (2 items if 2 cameras)
- ✓ Direction computation produces valid angles and speeds
- ✓ ROI coordinates within frame bounds

#### Display Test (Optional)
When prompted:
```
Run GUI display test? (y/n, default=n): y
```
This opens a GUI window for 5 seconds. Visually verify:
- Camera feed displays live
- Crosshair (red lines) follows your mouse
- Direction vector (line from center to mouse) appears
- Window closes cleanly

---

## Integration Testing

### Scenario 1: Complete Hardware Setup Verification

**Goal:** Verify all systems work together before running main application  
**Hardware Needed:** USB camera + RPi/UART device

#### Step 1: Verify Math Foundation
```bash
python test_direction.py
```
**Expected:** All tests pass ✓

#### Step 2: Verify Camera Input
```bash
python test_camera.py
```
**Expected:** At least 1 camera detected, frames captured at >20 FPS ✓

#### Step 3: Verify UART Output
```bash
python test_uart_handler.py
```
**Expected:** Connection succeeds + message formats valid ✓ (OK if connection fails)

#### Step 4: Verify GUI Integration
```bash
python test_gui.py
```
**Expected:** All components initialized, camera shown in dropdown ✓

#### Step 5: Run All Tests Together
```bash
python run_tests.py
```
**Expected Summary:**
```
======================================================================
Running all component tests...
======================================================================

[Test 1/4] Direction Calculation (test_direction.py)
✓ PASSED

[Test 2/4] Camera Interface (test_camera.py)
✓ PASSED

[Test 3/4] UART Handler (test_uart_handler.py)
⚠ SKIPPED or ✓ PASSED (depends on hardware)

[Test 4/4] GUI Components (test_gui.py)
✓ PASSED

======================================================================
Summary: 3–4 tests passed, ready to launch main application
======================================================================
```

#### Step 6: Launch Main Application
```bash
python main.py
```
or
```bash
python arm_gui.py
```

---

### Scenario 2: Diagnose a Broken Component

**When:** Something doesn't work in main application  
**Process:** Binary search using tests

#### Is the math wrong?
```bash
python test_direction.py
```
- ⚠ FAIL → Bug in angle/speed calculation logic
- ✓ PASS → Math is fine, issue elsewhere

#### Is the camera not working?
```bash
python test_camera.py
```
- ⚠ FAIL → Camera not detected, driver issue, or USB not connected
- ✓ PASS → Camera is fine, issue elsewhere

#### Is UART communication broken?
```bash
python test_uart_handler.py
```
- ⚠ FAIL → Serial port issue, RPi not connected, or COM port wrong
- ✓ PASS → UART is fine, issue elsewhere

#### Is the GUI not displaying?
```bash
python test_gui.py
```
- ⚠ FAIL → PyQt5 issue, or integration problem
- ✓ PASS → GUI is fine, issue in main loop

---

### Scenario 3: Multi-Camera Testing

**Goal:** Verify system works with multiple cameras

#### Test Each Camera Separately
The updated `test_camera.py` now:
1. Detects all cameras (e.g., [0, 1])
2. Runs all tests for Camera 0
3. Runs all tests for Camera 1
4. Tests switching between cameras

```bash
python test_camera.py
```

**Expected Output:**
```
[Test 1] Detecting available cameras...
  ✓ Camera 0 available
  ✓ Camera 1 available
  Found 2 camera(s): [0, 1]

[Running tests for camera 0]
  ...test output...

[Running tests for camera 1]
  ...test output...

[Test 7] Testing camera switching (2 cameras)...
  ✓ Camera 0: ✓
  ✓ Camera 1: ✓
```

#### Verify GUI Works with Both Cameras
```bash
python test_gui.py
```
Look for output:
```
✓ Camera detection results:
  - Cameras found: [0, 1]
  - Dropdown items: 2
  - Item 0: Camera 0
  - Item 1: Camera 1
```

---

## Troubleshooting & Diagnosis

### Test Execution Matrix

| Issue | Test to Run | Command | What to Look For |
|-------|------------|---------|-----------------|
| Math wrong | Direction | `python test_direction.py` | Angle/speed values incorrect |
| No camera | Camera | `python test_camera.py` | "No cameras detected" |
| Camera slow | Camera | `python test_camera.py` | FPS < 20 |
| Bad colors | Camera | `python test_camera.py` | "Conversion test failed" |
| No UART | UART | `python test_uart_handler.py` | "Connection failed" |
| GUI broken | GUI | `python test_gui.py` | Window not created |
| Nothing works | All | `python run_tests.py` | Most tests fail |

### Reading Test Output

#### ✓ Symbols Indicate Success
```
✓ Frame captured      ← Test passed
⚠ Connection failed   ← Expected failure (no device)
✗ Failed to open      ← Actual failure
```

#### Common Harmless Warnings
```
[WARN:0@0.016] global cap_ffmpeg_impl.hpp:1217 open VIDEOIO/FFMPEG: Failed list devices
  → OpenCV falling back to other backends; not a problem

[ERROR:0@2.595] global obsensor_uvc_stream_channel.cpp:163 cv::obsensor::getStreamChannelGroup
  → OpenCV probing indices 1–4; they don't exist; this is normal

[UART] Connection failed: module 'serial' has no attribute 'Serial'
  → pyserial not installed correctly; NOT normal, needs fixing
```

---

## Common Issues & Fixes

### 1. UART: "module 'serial' has no attribute 'Serial'"

**Problem:** `pyserial` module installed incorrectly  
**Fix:**
```bash
pip uninstall serial pyserial -y
pip install pyserial
```

### 2. Camera: "No cameras detected!"

**Problem:** USB camera not connected or driver missing  
**Diagnosis:**
```powershell
# Check Device Manager → Imaging devices
Get-PnpDevice -Class Camera | Format-Table -AutoSize
```
**Fix:**
- Plug in USB camera
- Install/update camera drivers from manufacturer
- Try different USB port
- Restart computer

### 3. Camera: "Module 'cv2' has no attribute 'VideoCapture'"

**Problem:** OpenCV not installed  
**Fix:**
```bash
pip install opencv-python
```

### 4. GUI: No window appears

**Problem:** PyQt5 not installed or display server issue  
**Fix:**
```bash
pip install --upgrade PyQt5
```

### 5. Direction: "Assertion errors" in test output

**Problem:** Math in `compute_direction()` incorrect  
**Diagnosis:** Check output to see which test failed:
```bash
python test_direction.py 2>&1 | grep -A5 "AssertionError"
```
**Fix:** Review angle/speed calculations in `camera_gui.py`

### 6. Slow FPS in `test_camera.py` (<20 FPS)

**Problem:** USB bandwidth, CPU load, or old camera  
**Diagnosis:**
- Check if other USB devices are running
- Check System Monitor for CPU usage
- Try reducing resolution in camera settings
**Fix:**
```python
# In camera_gui.py, after opening camera:
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
```

### 7. UART: "Connection failed: Port 'COM3' not found"

**Problem:** Wrong COM port or RPi not connected  
**Diagnosis:**
```powershell
# List all COM ports
Get-CimInstance Win32_SerialPort | Select-Object DeviceID
```
**Fix:** Update port in `main.py` or `camera_gui.py`:
```python
RPi_PORT = 'COM3'  # ← Change to your actual port
```

---

## Configuration Reference

### UART Settings
**File:** `main.py`, `arm_gui.py`, `camera_gui.py`
```python
RPi_PORT = 'COM3'          # Serial port name (Windows)
RPi_BAUDRATE = 9600        # Match your RPi baud rate
```

### Camera Settings
**File:** `camera_gui.py`
```python
detect_cameras() range(5)  # Checks indices 0–4
# Default resolution: 640×480 (OpenCV auto-selects)
```

### Direction Calculation
**File:** `camera_gui.py`, `test_direction.py`
```python
ROI_SIZE = 60              # Pixels around capture point
SPEED_MAX = 1.0            # Speed always capped
```

---

## Message Reference

### Direction Command (Laptop → RPi)
```
ANGLE:0.45,SPEED:0.75\n
```
- Sent continuously as mouse moves
- Angle in radians (−π to π)
- Speed in 0.0–1.0 range
- Newline-terminated

### Capture Command (Laptop → RPi)
```
CAPTURE:320,240\n
```
- Sent when K key pressed
- X, Y pixel coordinates in frame
- Newline-terminated

---

## Quick Reference: Test Commands

```bash
# Single component tests
python test_direction.py      # Math only
python test_camera.py         # Camera only
python test_uart_handler.py   # Serial only
python test_gui.py            # GUI only

# All tests
python run_tests.py

# Main application
python main.py
python arm_gui.py
```

---

## Summary: When to Use Each Test

| You Want To | Run | Time | Hardware |
|-------------|-----|------|----------|
| Verify math works | `test_direction.py` | 1s | None |
| Check camera connection | `test_camera.py` | 5–10s | USB camera |
| Verify UART setup | `test_uart_handler.py` | 2s | Optional |
| Test GUI layout | `test_gui.py` | 3–8s | Camera + display |
| Verify everything | `run_tests.py` | 10–20s | All of above |
| Run application | `main.py` | ∞ | All of above |

