# Robotic Arm Control System

This repository contains a distributed robotic arm control system with the following components:

## 📁 Project Structure

```
EDL_Project/
├── GUI_interface/           # 🖥️  LAPTOP - GUI Application
│   ├── arm_gui.py          # Main GUI launcher
│   ├── camera_gui.py       # Camera control and user interface
│   ├── uart_handler.py     # UART communication with Master RPi
│   ├── test_uart_handler.py # UART handler tests
│   ├── run_tests.py        # Test runner
│   ├── test_*.py           # Various test files
│   └── main.py             # Alternative entry point
│
├── Master_RPI/         # 🔧 MASTER RPi - Motor Control (single source of truth)
│   ├── master_command_processor.py    # UART command processing
│   ├── master_motor_controller.py     # Motor control logic
│   ├── master_config.py              # Master RPi configuration
│   ├── master_test_motor_controller.py # Master tests
│   └── MASTER_README.md              # Master documentation
│
└── Slave_RPI/              # 📡 SLAVE RPi - Encoder Interface
    ├── slave_encoder_interface.py   # Encoder reading and I2C
    └── README.md                    # Slave documentation
```

## 🖥️ GUI_interface (Laptop)

**Purpose:** User interface for camera control and direction commands

**Key Files:**
- `camera_gui.py` - Main GUI with camera feed and mouse control
- `uart_handler.py` - Sends commands to Master RPi via UART
- `arm_gui.py` - GUI application launcher

**Communication:**
- Sends direction commands: `ANGLE:<angle>,SPEED:<speed>`
- Sends capture commands: `CAPTURE`

## 🔧 Master_RPI (Master RPi)

**Purpose:** Main motor control system coordinating all slave devices

**Key Files:**
- `master_command_processor.py` - Receives GUI commands via UART
- `master_motor_controller.py` - Controls motors via PWM and GPIO
- `master_config.py` - I2C addresses and system configuration

**Slave Communication:**
- PWM Generator (PCA9685) - Motor speed control
- GPIO Expander 1 (MCP23017) - Motor direction control
- GPIO Expander 2 (MCP23017) - Limit switch monitoring
- Slave RPi - Encoder feedback

## 📡 Slave_RPI (Slave RPi)

**Purpose:** Encoder data acquisition and feedback

**Key Files:**
- `slave_encoder_interface.py` - Quadrature encoder reading and I2C responses

**Hardware:**
- 8 quadrature encoders for motor position feedback
- I2C communication with Master RPi

## 🚀 Deployment

### Laptop Setup
```bash
# Install dependencies
pip install PyQt5 opencv-python pyserial

# Run GUI
cd GUI_interface
python arm_gui.py
```

### Master RPi Setup
```bash
# Install dependencies
pip install smbus

# Run motor control
cd Master_RPI
python master_command_processor.py
```

### Slave RPi Setup
```bash
# Install dependencies
pip install RPi.GPIO smbus

# Run encoder interface
cd Slave_RPI
python slave_encoder_interface.py
```

## 🔌 Hardware Connections

### Master RPi I2C Devices
- PWM Generator: 0x40
- GPIO Expander 1: 0x20 (motor directions)
- GPIO Expander 2: 0x21 (limit switches)
- Slave RPi: 0x50

### Slave RPi Encoder Pins (BCM)
See `Slave_RPI/README.md` for encoder pin assignments.

## 📋 Communication Flow

1. **Laptop GUI** → UART → **Master RPi**
2. **Master RPi** → I2C → **Slave Devices** (PWM, GPIO, Slave RPi)
3. **Slave RPi** → I2C → **Master RPi** (encoder feedback)

## 🧪 Testing

Each component has independent tests:
- Laptop: `GUI_interface/test_*.py`
- Master: `Master_RPI/master_test_motor_controller.py`
- Slave: Run with simulation mode (no hardware required)

## ⚙️ Configuration

- Master RPi: `Master_RPI/master_config.py`
- Adjust I2C addresses and pin assignments for your hardware
- Encoder pins in `Slave_RPI/slave_encoder_interface.py`