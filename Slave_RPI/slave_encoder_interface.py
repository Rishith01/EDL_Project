"""
Slave RPi Encoder Interface and Communication
Handles encoder reading and I2C communication with Master RPi
"""

import time
import threading
import RPi.GPIO as GPIO
import serial

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
            GPIO.add_event_detect(pinA, GPIO.BOTH, callback=lambda channel, enc=i: self._encoder_callback(enc))
            GPIO.add_event_detect(pinB, GPIO.BOTH, callback=lambda channel, enc=i: self._encoder_callback(enc))

    def _encoder_callback(self, encoder_id):
        """Handle encoder pin change interrupts"""
        pinA, pinB = self.encoder_pins[encoder_id]

        # Read current states
        stateA = GPIO.input(pinA)
        stateB = GPIO.input(pinB)
        new_state = (stateA << 1) | stateB

        # Determine direction and update count
        
        # Quadrature encoding state transitions
        # Clockwise: 00->01->11->10->00
        # Counter-clockwise: 00->10->11->01->00

        with self.lock:
            old_state = self.encoder_states[encoder_id]
            if (old_state == 0 and new_state == 1) or \
               (old_state == 1 and new_state == 3) or \
               (old_state == 3 and new_state == 2) or \
               (old_state == 2 and new_state == 0):
                self.encoder_counts[encoder_id] += 1

            elif (old_state == 0 and new_state == 2) or \
                 (old_state == 2 and new_state == 3) or \
                 (old_state == 3 and new_state == 1) or \
                 (old_state == 1 and new_state == 0):
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
    """Main slave RPi controller using UART"""

    def __init__(self, encoder_pins=None, uart_port='/dev/serial0', baudrate=115200):

        if encoder_pins is None:
            self.encoder_pins = [
                (17, 18),
                (22, 23),
                (24, 25),
                (5, 6),
                (12, 13),
                (19, 20),
                (16, 26),
                (21, 27)
            ]
        else:
            self.encoder_pins = encoder_pins

        self.encoder_reader = EncoderReader(self.encoder_pins)

        self.serial = serial.Serial(
            port=uart_port,
            baudrate=baudrate,
            timeout=0.1
        )

        self.running = False
        self.thread = None

        print(f"[SlaveRPi] UART initialized on {uart_port} @ {baudrate} baud")

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._uart_loop, daemon=True)
        self.thread.start()
        print("[SlaveRPi] Started UART command loop")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.encoder_reader.cleanup()
        self.serial.close()
        print("[SlaveRPi] Stopped cleanly")

    def _uart_loop(self):
        while self.running:
            try:
                if self.serial.in_waiting > 0:
                    command = self.serial.readline().decode().strip()

                    if command == "GET":
                        counts = self.encoder_reader.get_counts()
                        response = ",".join(str(c) for c in counts)
                        self.serial.write((response + "\n").encode())

                    elif command == "RESET":
                        self.encoder_reader.reset_counts()
                        self.serial.write(b"OK\n")

            except Exception as e:
                print(f"[SlaveRPi] UART error: {e}")
                time.sleep(1)


def main():
    print("Slave RPi Encoder UART Interface Starting...")

    slave = SlaveRPi()

    try:
        slave.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[SlaveRPi] Shutdown requested")
    except Exception as e:
        print(f"[SlaveRPi] Fatal error: {e}")
    finally:
        slave.stop()

if __name__ == "__main__":
    main()