# Master RPi Robotic Arm Motor Control System

This folder contains the motor control system for the Master Raspberry Pi, handling communication with slave devices and motor coordination.

## Architecture

The software is split between two Raspberry Pis:

- **Controlling (Master) RPi** – this repository path; it runs the command
  processor and motor controller code.  It receives high‑level movement
  messages from the GUI over UART, computes appropriate motor outputs, and
  forwards encoder requests to the slave.

- **Slave RPi** – a lightweight helper (not shown here) connected to the motor
  encoders.  It reads the encoder values and provides them over I2C to the
  master RPi.

The system consists of the following modules:

1. **Command Processor** (`master_command_processor.py`): Receives commands from
   GUI via UART and translates them to motor control commands
2. **Motor Controller** (`master_motor_controller.py`): Handles low-level motor
   control and communication with slave devices
3. **Configuration** (`master_config.py`): System configuration and I2C addresses

## Hardware Setup

The system communicates with the following slave devices via I2C:

- **PWM Generator** (PCA9685): Controls motor speeds (8 channels)
- **GPIO Expander 1** (MCP23017): Controls motor directions (8 outputs)
- **GPIO Expander 2** (MCP23017): Reads limit switches (16 inputs)
- **Slave RPi**: Provides encoder feedback (8 encoders)

## Motor Mapping

- **Motor 0**: Lead‑screw drive for whole‑arm forward/backward movement
- **Motors 1-6**: Continuum robot joints (three modules with two motors each)
- **Motors 7-8**: Tentacle end effector

> Note: GUI central box now covers roughly 50% of the display – clicking inside
> means a pure forward command; outside triggers a lateral direction.

## Usage

### Running the Motor Control System

```bash
python command_processor.py
```

### Testing Individual Components

```bash
python test_motor_controller.py
```

## Configuration

Edit `master_config.py` to adjust I2C addresses and other settings for your specific hardware setup.

## Communication Protocol

The GUI now sends a higher‑level movement message describing a cardinal
direction plus a forward component.  Supported messages (all terminated by
newline) are:

```
DIR:<direction>,SPEED:<speed>,FWD:<forward>
CAPTURE
```

* `<direction>` is one of `FORWARD`, `BACKWARD`, `LEFT`, `RIGHT`, `UP`, `DOWN`
* `<speed>` is the lateral magnitude (0.0–1.0) used to drive the continuum
  motors
* `<forward>` is the forward/backward magnitude (0.0–1.0) used to drive the
  lead‑screw; the master records this history so the arm can retrace its
  path after a capture

For backwards compatibility the old `ANGLE:<angle>,SPEED:<speed>` messages
are still recognised; they are converted internally into the new format.

`CAPTURE` remains the same and will trigger the arm to return to its starting
position by replaying the stored forward history.

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