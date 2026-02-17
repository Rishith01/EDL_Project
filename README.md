# Robotic Arm Control Interface

A real-time GUI application for controlling a robotic arm using a connected camera (USB or webcam) and mouse input.

## Project Structure

```
EDL_Project/
├── uart_handler.py        # UART communication with RPi
├── camera_gui.py          # Main GUI and camera components
├── arm_gui.py            # Alternative entry point (imports from camera_gui)
├── main.py               # Primary entry point for the application
├── test_uart_handler.py   # Unit test for UART module
├── test_camera.py        # Unit test for camera detection
├── test_direction.py     # Unit test for direction calculation
├── test_gui.py           # Unit test for GUI components
├── run_tests.py          # Master test runner for all tests
├── TESTING_GUIDE.md      # Comprehensive testing documentation
└── README.md             # This file
```

## Module Descriptions

### `uart_handler.py`
Handles UART serial communication with the Raspberry Pi server.

**Key Classes:**
- `UartHandler`: Manages UART connections, sends commands to RPi

**Features:**
- Thread-safe serial operations with locking
- PyQt5 signals for connection status updates
- Message formats:
  - `ANGLE:<angle>,SPEED:<speed>\n` - Continuous arm direction
  - `CAPTURE:<x>,<y>\n` - Object capture at coordinates

**Usage:**
```python
from uart_handler import UartHandler

handler = UartHandler(port='COM3', baudrate=9600)
handler.connect()
handler.send_command(angle=1.57, speed=0.5)
handler.send_capture(x=320, y=240)
handler.disconnect()
```

### `camera_gui.py`
Main GUI implementation with camera feed display and control handling.

**Key Classes:**
- `CameraLabel`: Custom QLabel that captures keyboard events
- `CameraGUI`: Main application window

**Features:**
- Real-time camera feed (USB or webcam)
- Auto-detection of available cameras
- Mouse-based arm direction control
- Keyboard shortcuts (K for capture, ESC to exit)
- Overlay graphics (crosshair, direction vector)
- Camera selection dropdown
- Integrated socket communication

**Usage:**
```python
from camera_gui import CameraGUI

gui = CameraGUI(rpi_port='COM3', rpi_baudrate=9600)
gui.show()
```

### `main.py`
Primary entry point for the application.

**Usage:**
```bash
python main.py
```

### `arm_gui.py`
Alternative entry point with function wrapper for programmatic use.

**Usage:**
```bash
python arm_gui.py
```

## Testing Individual Modules

For comprehensive testing documentation with independent tests for each component, see [TESTING_GUIDE.md](TESTING_GUIDE.md).

### Test UART Handler
```bash
python test_uart_handler.py
```
Tests UART initialization, connection attempts, and message sending (without requiring a connected RPi).

### Test Direction Calculation
```bash
python test_direction.py
```
Tests mouse position to angle/speed conversion (pure math, no hardware needed).

### Run All Tests
```bash
python run_tests.py
```
Runs all independent tests and provides a summary report.

### Test Camera
```bash
python test_camera.py
```
Tests camera detection, frame capture, and FPS measurement.

### Test GUI
```bash
python test_gui.py
```
Tests GUI initialization and functionality (opens window for 10 seconds).

## Configuration

Edit the RPi UART connection settings in `main.py` or `arm_gui.py`:

```python
RPi_PORT = 'COM3'      # Your serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
RPi_BAUDRATE = 9600    # Your UART baud rate
```

## Requirements

```
PyQt5
opencv-python (cv2)
numpy
pyserial
```

Install with:
```bash
pip install PyQt5 opencv-python numpy pyserial
```

## Usage Controls

| Control | Action |
|---------|--------|
| **Mouse movement** | Control arm direction from center of screen |
| **K key** | Capture object at mouse position and send to RPi |
| **ESC key** | Exit application |
| **Dropdown** | Select camera source |

## How It Works

1. **Camera Feed**: Captures real-time video from selected camera
2. **Mouse Tracking**: Calculates angle and speed from mouse position relative to screen center
3. **Overlays**: Displays crosshair at mouse position and direction vector from center
4. **Communication**: Sends angle/speed continuously and capture commands on demand to RPi
5. **Modular Design**: Each component can be tested independently

## RPi Server Expected Format

Your Raspberry Pi UART server should:
1. Listen on UART serial port (typically `/dev/ttyAMA0` or `/dev/ttyUSB0`)
2. Use matching baud rate (default: 9600)
3. Accept messages in format: `ANGLE:<float>,SPEED:<float>\n`
4. Accept commands in format: `CAPTURE:<int>,<int>\n`

Example Python RPi UART server:
```python
import serial

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

while True:
    if ser.in_waiting:
        msg = ser.readline().decode().strip()
        print(f"Received: {msg}")
        # Process motor commands here
```

## Troubleshooting

### No cameras detected
- Check USB camera connection
- Try different camera indices (modify `detect_cameras()` range)
- Test with: `python test_camera.py`

### UART connection fails
- Verify RPi is running and UART is available
- Check serial port name (modify `RPi_PORT` in main.py)
- Verify baud rate matches RPi configuration (modify `RPi_BAUDRATE` in main.py)
- Ensure USB UART adapter is properly connected (if using USB-to-UART)
- Test with: `python test_uart_handler.py`
- On Windows, check Device Manager for COM port assignment
- On Linux, use `ls -la /dev/tty*` to verify port availability
- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed troubleshooting

### GUI window doesn't appear
- Check PyQt5 installation
- Test GUI with: `python test_gui.py`
- Ensure display server is available

## Future Enhancements

- [ ] Add frame recording capability
- [ ] Add object detection/tracking
- [ ] Add gesture recognition for commands
- [ ] Add UDP option for faster communication
- [ ] Add configuration file support
- [ ] Add logging system
- [ ] Add calibration interface
