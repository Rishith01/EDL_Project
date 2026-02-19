# Master RPi Robotic Arm Motor Control System

This folder contains the motor control system for the Master Raspberry Pi, handling communication with slave devices and motor coordination.

## Architecture

The system consists of:

1. **Command Processor** (`master_command_processor.py`): Receives commands from GUI via UART and translates them to motor control commands
2. **Motor Controller** (`master_motor_controller.py`): Handles low-level motor control and communication with slave devices
3. **Configuration** (`master_config.py`): System configuration and I2C addresses

## Hardware Setup

The system communicates with the following slave devices via I2C:

- **PWM Generator** (PCA9685): Controls motor speeds (8 channels)
- **GPIO Expander 1** (MCP23017): Controls motor directions (8 outputs)
- **GPIO Expander 2** (MCP23017): Reads limit switches (16 inputs)
- **Slave RPi**: Provides encoder feedback (8 encoders)

## Motor Mapping

- **Motors 0-1**: Tentacle end effector
- **Motors 2-7**: Continuum robot joints

## Usage

### Running the Motor Control System

```bash
python master_command_processor.py
```

### Testing Individual Components

```bash
python master_test_motor_controller.py
```

## Configuration

Edit `master_config.py` to adjust I2C addresses and other settings for your specific hardware setup.

## Communication Protocol

The system receives commands from the GUI via UART with the following format:

- Direction commands: `ANGLE:<angle>,SPEED:<speed>`
- Capture commands: `CAPTURE`

Where:
- `angle`: Direction in radians (-π to π)
- `speed`: Magnitude (0.0 to 1.0)
- `x`, `y`: Camera coordinates for object capture

## Safety Features

- Emergency stop functionality
- Limit switch monitoring
- Encoder feedback for position control
- Dead zone handling for small movements

## Dependencies

- `smbus` (for I2C communication on Raspberry Pi)
- `serial` (for UART communication)
- `threading` (for concurrent operations)

## Notes

- The system can run in simulation mode if hardware is not available
- Motor mapping and kinematics are simplified - adjust based on your robot's specific requirements
- Encoder and limit switch mappings need to be configured for your hardware setup