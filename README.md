# Robotic Arm Control Interface

A real-time GUI application for controlling a robotic arm using a connected camera (USB or webcam) and mouse input.

## Project Structure

```
EDL_Project/
├── socket_handler.py      # TCP socket communication with RPi
├── camera_gui.py          # Main GUI and camera components
├── arm_gui.py            # Alternative entry point (imports from camera_gui)
├── main.py               # Primary entry point for the application
├── test_socket_handler.py # Unit test for socket module
├── test_camera.py        # Unit test for camera detection
├── test_gui.py           # Unit test for GUI components
└── README.md             # This file
```

## Module Descriptions

### `socket_handler.py`
Handles TCP socket communication with the Raspberry Pi server.

**Key Classes:**
- `SocketHandler`: Manages socket connections, sends commands to RPi

**Features:**
- Thread-safe socket operations with locking
- PyQt5 signals for connection status updates
- Message formats:
  - `ANGLE:<angle>,SPEED:<speed>\n` - Continuous arm direction
  - `CAPTURE:<x>,<y>\n` - Object capture at coordinates

**Usage:**
```python
from socket_handler import SocketHandler

handler = SocketHandler(host='192.168.1.100', port=5000)
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

gui = CameraGUI(rpi_host='192.168.1.100', rpi_port=5000)
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

### Test Socket Handler
```bash
python test_socket_handler.py
```
Tests socket initialization, connection attempts, and message sending (without requiring a running RPi server).

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

Edit the RPi connection settings in `main.py` or `arm_gui.py`:

```python
RPi_HOST = '192.168.1.100'  # Your RPi IP address
RPi_PORT = 5000              # Your RPi server port
```

## Requirements

```
PyQt5
opencv-python (cv2)
numpy
```

Install with:
```bash
pip install PyQt5 opencv-python numpy
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

Your Raspberry Pi server should:
1. Listen on TCP port 5000 (or configured port)
2. Accept messages in format: `ANGLE:<float>,SPEED:<float>\n`
3. Accept commands in format: `CAPTURE:<int>,<int>\n`

Example Python RPi server:
```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000))
server.listen(1)
conn, addr = server.accept()

while True:
    msg = conn.recv(1024).decode()
    print(f"Received: {msg}")
    # Process motor commands here
```

## Troubleshooting

### No cameras detected
- Check USB camera connection
- Try different camera indices (modify `detect_cameras()` range)
- Test with: `python test_camera.py`

### Socket connection fails
- Verify RPi is running and server is listening
- Check RPi IP address (modify `RPi_HOST` in main.py)
- Verify network connectivity
- Test with: `python test_socket_handler.py`

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
