# Slave RPi Encoder Interface

This folder contains code for the Slave Raspberry Pi that handles encoder reading and communication with the Master RPi.

## Files

- `slave_encoder_interface.py` - Main encoder interface and I2C communication code

## Hardware Setup

### Encoder Connections
The code expects 8 quadrature encoders connected to the following GPIO pins (BCM numbering):

| Encoder | Pin A | Pin B |
|---------|-------|-------|
| 0       | 17    | 18    |
| 1       | 22    | 23    |
| 2       | 24    | 25    |
| 3       | 5     | 6     |
| 4       | 12    | 13    |
| 5       | 19    | 20    |
| 6       | 16    | 26    |
| 7       | 21    | 27    |

### I2C Communication
- I2C Address: 0x50 (configurable)
- Communicates with Master RPi for encoder data requests

## Usage

```bash
python slave_encoder_interface.py
```

## Dependencies

- `RPi.GPIO` - For GPIO access
- `smbus` - For I2C communication

## Encoder Data Format

Encoder counts are sent as 16-bit signed integers:
- 2 bytes per encoder (high byte first)
- Total: 16 bytes for 8 encoders
- Range: -32768 to +32767

## Notes

- Adjust encoder pin assignments in the code for your specific hardware setup
- Ensure proper pull-up resistors on encoder lines
- The slave responds to I2C read requests from the master