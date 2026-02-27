# Component Testing Guide

This document describes step-by-step procedures to test each part of the robotic arm
system: GUI (laptop), Master RPi code, and Slave RPi encoder interface.  Use this
before deploying to hardware or when verifying functionality after changes.

---

## 1. GUI Interface (Laptop)

1. **Prepare environment**
   ```bash
   cd GUI_interface
   pip install PyQt5 opencv-python pyserial
   ```

2. **Run unit tests**
   ```bash
   python run_tests.py
   ```
   - Verifies `uart_handler`, camera feed simulation, and GUI logic.

3. **Manual exercise**
   - Launch application:
     ```bash
     python arm_gui.py
     ```
   - Move the mouse over the video feed. Observe printed direction/forward
     messages in the terminal (about 30 FPS).
   - Click in the centre box (50 % area) – should print `forward` commands.
   - Click outside – cardinal directions should appear.
   - Press **K** to send a `CAPTURE` command and verify it is printed.
   - If an RPi is connected on the configured COM port, the messages will be
     sent over UART; open a serial monitor to inspect them.

4. **Inspect UART output**
   - Use a USB‑TTL adapter or a loop‑back to confirm that `DIR:` messages are
     sent correctly.

---

## 2. Master RPi Code

1. **Prepare environment**
   ```bash
   cd Master_RPI
   pip install smbus pyserial
   ```

2. **Run motor controller tests**
   ```bash
   python master_test_motor_controller.py
   ```
   - Runs in simulation mode (smbus unavailable) and prints results for every
     motor command, including legacy and new message formats, capture replay,
     encoder/limit‑switch reads, and emergency stop.

3. **Inspect behavior manually**
   - Start the command processor:
     ```bash
     python master_command_processor.py
     ```
   - Connect to it via UART (match port/baud in `master_config.py`).
   - Send test strings manually, e.g. via `echo "DIR:LEFT,SPEED:0.5,FWD:0.5" > /dev/ttyUSB0`.
   - Observe printed motor‑controller debug output.
   - Issue `CAPTURE` and check that `retrace_forward_history()` message appears.
   - Verify `get_status()` reports sensible values (forward_history, speeds, etc.)
     using the interactive test mode or by calling it from Python.
   - **Limit switch check:** adjust `LIMIT_SWITCH_TO_MOTORS` in
     `master_config.py` and trigger one of the dummy switches; commands for the
     corresponding motor(s) should be blocked and a warning printed.

4. **Hardware integration**
   - With I2C devices connected, run the processor and ensure no initialization
     errors are printed.
   - Trigger limit switches or rotate encoders to see values change.
   - Use the PWM/GPIO I2C addresses in `master_config.py` to map to your
     actual hardware; adjust as needed.

---

## 3. Slave RPi Interface

1. **Prepare environment**
   ```bash
   cd Slave_RPI
   pip install RPi.GPIO smbus
   ```

2. **Review `slave_encoder_interface.py` for pin assignments**
   - Map each encoder channel (A/B) to the correct BCM GPIO pins.

3. **Run in simulation mode**
   - If you lack hardware, the script should fallback gracefully or be stubbed.
   - Execute it and ensure it exposes an I2C address (0x50 by default).

4. **Hardware test**
   - Power the encoders and run the script on the slave Pi.
   - On the master Pi execute a small snippet:
     ```python
     import smbus
     bus = smbus.SMBus(1)
     data = [bus.read_byte_data(0x50, i) for i in range(16)]
     print(data)
     ```
   - Rotate each encoder; values should change accordingly.

5. **Integration check**
   - Start both master and slave Raspberry Pis.
   - Command the master to move the motors and verify that the slave reports
     sensible encoder values when read by the master’s control loop.

---

## 4. End-to-end test (all components together)

1. Start the slave interface on its Pi.
2. Start the master command processor on the master Pi.
3. Run the GUI on a laptop connected to the master via UART.
4. Move the mouse/click to send commands; observe the master log and ensure the
   lead‑screw and continuum motors receive correct signals.
5. Use `CAPTURE` to force the arm to retract; watch the master’s forward
   history and replay behaviour.

---

## Notes

- Adjust serial port names and I2C addresses to match your setup.
- For hardware-less testing, run the master and GUI simultaneously and use a
  virtual serial port pair (e.g. `com0com` on Windows) to link them.
- This testing guide is kept independent of particular OSs; adapt commands as
  necessary for Linux-based RPis.

Happy testing!  Ensure each step passes before moving to the next layer.