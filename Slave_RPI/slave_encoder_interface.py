"""
Slave RPi Encoder Interface and Communication
Handles encoder reading and I2C communication with Master RPi
"""

import time
import threading
import RPi.GPIO as GPIO
from smbus import SMBus


class EncoderReader:
    """Handles quadrature encoder reading for multiple motors"""

    def __init__(self, encoder_pins):
        """
        Initialize encoder reader

        Args:
            encoder_pins: List of (pinA, pinB) tuples for each encoder
        """
        self.encoder_pins = encoder_pins
        self.num_encoders = len(encoder_pins)
        self.encoder_counts = [0] * self.num_encoders
        self.encoder_states = [0] * self.num_encoders
        self.lock = threading.Lock()

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for i, (pinA, pinB) in enumerate(encoder_pins):
            GPIO.setup(pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Read initial state
            stateA = GPIO.input(pinA)
            stateB = GPIO.input(pinB)
            self.encoder_states[i] = (stateA << 1) | stateB

            # Setup interrupts
            GPIO.add_event_detect(pinA, GPIO.BOTH, callback=lambda channel, enc=i: self._encoder_callback(channel, enc, True))
            GPIO.add_event_detect(pinB, GPIO.BOTH, callback=lambda channel, enc=i: self._encoder_callback(channel, enc, False))

    def _encoder_callback(self, channel, encoder_id, is_pinA):
        """Handle encoder pin change interrupts"""
        pinA, pinB = self.encoder_pins[encoder_id]

        # Read current states
        stateA = GPIO.input(pinA)
        stateB = GPIO.input(pinB)
        new_state = (stateA << 1) | stateB

        # Determine direction and update count
        old_state = self.encoder_states[encoder_id]

        # Quadrature encoding state transitions
        # Clockwise: 00->01->11->10->00
        # Counter-clockwise: 00->10->11->01->00

        with self.lock:
            if old_state == 0:  # 00
                if new_state == 1:  # 01 - clockwise
                    self.encoder_counts[encoder_id] += 1
                elif new_state == 2:  # 10 - counter-clockwise
                    self.encoder_counts[encoder_id] -= 1
            elif old_state == 1:  # 01
                if new_state == 3:  # 11 - clockwise
                    self.encoder_counts[encoder_id] += 1
                elif new_state == 0:  # 00 - counter-clockwise
                    self.encoder_counts[encoder_id] -= 1
            elif old_state == 2:  # 10
                if new_state == 0:  # 00 - clockwise
                    self.encoder_counts[encoder_id] += 1
                elif new_state == 3:  # 11 - counter-clockwise
                    self.encoder_counts[encoder_id] -= 1
            elif old_state == 3:  # 11
                if new_state == 2:  # 10 - clockwise
                    self.encoder_counts[encoder_id] += 1
                elif new_state == 1:  # 01 - counter-clockwise
                    self.encoder_counts[encoder_id] -= 1

            self.encoder_states[encoder_id] = new_state

    def get_counts(self):
        """Get current encoder counts"""
        with self.lock:
            return self.encoder_counts.copy()

    def reset_counts(self, encoder_id=None):
        """Reset encoder counts"""
        with self.lock:
            if encoder_id is None:
                self.encoder_counts = [0] * self.num_encoders
            else:
                self.encoder_counts[encoder_id] = 0

    def cleanup(self):
        """Cleanup GPIO"""
        GPIO.cleanup()


class SlaveRPi:
    """Main slave RPi controller"""

    def __init__(self, i2c_address=0x50, encoder_pins=None):
        """
        Initialize slave RPi

        Args:
            i2c_address: I2C address for master communication
            encoder_pins: List of (pinA, pinB) tuples for encoders
        """
        self.i2c_address = i2c_address

        # Default encoder pins (BCM numbering) - adjust for your setup
        if encoder_pins is None:
            # 8 encoders: ENC0-ENC7
            self.encoder_pins = [
                (17, 18),   # Encoder 0
                (22, 23),   # Encoder 1
                (24, 25),   # Encoder 2
                (5, 6),     # Encoder 3
                (12, 13),   # Encoder 4
                (19, 20),   # Encoder 5
                (16, 26),   # Encoder 6
                (21, 27)    # Encoder 7
            ]

        self.encoder_reader = EncoderReader(self.encoder_pins)

        # I2C bus for communication with master
        self.i2c_bus = SMBus(1)  # I2C bus 1 on RPi

        # Control flags
        self.running = False
        self.update_thread = None

        print(f"[SlaveRPi] Initialized with I2C address 0x{i2c_address:02X}")

    def start(self):
        """Start the slave RPi services"""
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        print("[SlaveRPi] Started encoder monitoring")

    def stop(self):
        """Stop the slave RPi services"""
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=1.0)
        self.encoder_reader.cleanup()
        print("[SlaveRPi] Stopped")

    def _update_loop(self):
        """Main update loop for encoder monitoring"""
        while self.running:
            try:
                # Encoder data is read on-demand via I2C requests from master
                time.sleep(0.01)  # 100Hz base loop
            except Exception as e:
                print(f"[SlaveRPi] Update loop error: {e}")
                time.sleep(1.0)

    def get_encoder_data(self):
        """Get encoder data as 16-bit values"""
        counts = self.encoder_reader.get_counts()
        # Convert to 16-bit signed integers
        data = []
        for count in counts:
            # Clamp to 16-bit range
            clamped = max(-32768, min(32767, count))
            # Convert to unsigned 16-bit for I2C transmission
            if clamped < 0:
                data.append(65536 + clamped)
            else:
                data.append(clamped)
        return data

    def handle_i2c_request(self):
        """Handle I2C read requests from master"""
        encoder_data = self.get_encoder_data()

        # Return data as bytes (16 bytes total: 2 bytes per encoder)
        response = bytearray()
        for value in encoder_data:
            response.append(value >> 8)    # High byte
            response.append(value & 0xFF)  # Low byte

        return response


def main():
    """Main entry point for slave RPi"""
    print("Slave RPi Encoder Interface Starting...")

    # Create slave RPi instance
    slave = SlaveRPi(i2c_address=0x50)  # Match master config

    try:
        slave.start()

        # Keep running
        while True:
            time.sleep(1.0)
            # Print encoder status every 10 seconds
            if int(time.time()) % 10 == 0:
                counts = slave.encoder_reader.get_counts()
                print(f"[SlaveRPi] Encoder counts: {counts}")

    except KeyboardInterrupt:
        print("\n[SlaveRPi] Shutdown requested")
    except Exception as e:
        print(f"[SlaveRPi] Fatal error: {e}")
    finally:
        slave.stop()


if __name__ == "__main__":
    main()