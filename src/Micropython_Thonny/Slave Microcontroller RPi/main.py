"""
=====================================================================================
This script configures the slave RPi Pico to act as a dedicated, 
high-speed hardware encoder coprocessor. It operating strictly as an I2C Peripheral to the master RPi. 
It handles the computationally expensive task of tracking thousands of motor pulses per second across 8 DC motors.

Instead of relying on standard CPU interrupts (which can drop ticks at high speeds),
we leverage the RP2040's PIO state machines. 
The PIO blocks count quadrature encoder pulses in the background with zero CPU overhead. 

Core Responsibilities:
1. High-Speed Pulse Counting : Manages 8 PIO state machines to track link motors.
2. Target Zeroing            : Listens for command from the Master to instantly 
                               reset a specific encoder's tick count to 0 before a move.
3. Telemetry Streaming       : Packages all 8 encoder counts into a continuous 16-byte 
                               Little-Endian payload upon Master request.

Software Dependencies:
1. i2c_responder.py 
=====================================================================================
"""

import rp2
import machine
import time
from i2c_responder import I2CResponder 

# For convenient visual confirmation that the slave is ON, we turn on the LED.
led = machine.Pin("LED", machine.Pin.OUT)
led.value(1)

# ==========================================
# 1. PIO ENCODER CLASS (For the 8 Links)
# ==========================================
# This assembly runs directly on the PIO hardware block, not the main CPU.
# It waits for Pin A to change, reads both A and B, and pushes the binary 
# state into a hardware queue (RX FIFO) for the Python CPU to evaluate later.
@rp2.asm_pio()
def quadrature_encoder():
    wrap_target()
    wait(1, pin, 0)      # Block and wait for Pin A to go HIGH
    in_(pins, 2)         # Read the state of Pin A and Pin B (2 bits)
    push(noblock)        # Push that 2-bit state into the hardware FIFO
    wait(0, pin, 0)      # Block and wait for Pin A to go LOW
    wrap()

class PIOEncoder:
    def __init__(self, sm_id, pin_a, pin_b):
        # Bind the assembly code to a specific State Machine and GPIO pair
        self.sm = rp2.StateMachine(sm_id, quadrature_encoder, in_base=pin_a)
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.ticks = 0
        self.sm.active(1) # Start the hardware state machine

    def read(self):
        # Drain the hardware queue. Evaluate the 2-bit state to determine direction.
        while self.sm.rx_fifo():
            state = self.sm.get() & 0x03 # State is either 01 or 11
            
            # Quadrature Logic: If A leads B, it's state 1. If B leads A, it's state 3.
            if state == 1:       
                self.ticks += 1  # Forward tick
            elif state == 3:     
                self.ticks -= 1  # Backward tick
                
        return abs(self.ticks) # PC Controller only cares about absolute distance traveled
        
    def reset(self):
        # Clear any leftover data in the queue and zero out the counter
        while self.sm.rx_fifo():
            self.sm.get()
        self.ticks = 0

# ==========================================
# 2. SYSTEM SETUP
# ==========================================
NUM_MOTORS = 8 # Tracking the 8 Continuum Links

print("Initializing Encoders (8 PIO)...")
# Map the 8 State Machines to their physical GPIO pin pairs
encoders = [
    PIOEncoder(0, machine.Pin(0), machine.Pin(1)),
    PIOEncoder(1, machine.Pin(2), machine.Pin(3)),
    PIOEncoder(2, machine.Pin(8), machine.Pin(9)),
    PIOEncoder(3, machine.Pin(10), machine.Pin(11)),
    PIOEncoder(4, machine.Pin(12), machine.Pin(13)),
    PIOEncoder(5, machine.Pin(14), machine.Pin(15)),
    PIOEncoder(6, machine.Pin(22), machine.Pin(26)),
    PIOEncoder(7, machine.Pin(20), machine.Pin(21))
]

# Initialize the RPi Pico as an I2C Peripheral (Slave) on Address 0x50
i2c_target = I2CResponder(i2c_device_id=0, sda_gpio=4, scl_gpio=5, responder_address=0x50)
print("SLAVE READY. Tracking 8 Encoders.")

incoming_buffer = []

while True:
    # --- TASK 1. DRAIN FIFOS / UPDATE TICKS ---
    # The PIO hardware is counting infinitely fast. We just empty the queue 
    # every loop to update our Python variable.
    for m in range(NUM_MOTORS):
        encoders[m].read()

    # --- TASK 2. HANDLE MASTER COMMANDS (WRITES) ---
    # If the Master Pico sends data, we parse it. 
    # Expected format: [Command_Byte, Motor_ID_Byte]
    if i2c_target.write_data_is_available():
        incoming_buffer.extend(i2c_target.get_write_data(max_size=2))
        
    if len(incoming_buffer) >= 2:
        cmd = incoming_buffer[0]
        m = incoming_buffer[1]
        
        # 0x01 is the "reset encoder" command.
        if cmd == 0x01 and 0 <= m < NUM_MOTORS:
            encoders[m].reset() # sets encoder ticks to 0, to start counting from 0
            
        incoming_buffer = incoming_buffer[2:] # Clear processed bytes from buffer

    # --- TASK 3. SEND TELEMETRY PACKET (READS) ---
    # If the Master Pico requests data, we package all 8 encoders into 16 bytes
    if i2c_target.read_is_pending():
        data_packet = bytearray(16) # 8 motors * 2 bytes each = 16 bytes
        
        for m in range(NUM_MOTORS):
            current_ticks = abs(encoders[m].ticks)
            
            # Little-Endian Formatting: 
            # Slice the 16-bit integer into two 8-bit bytes for I2C transmission
            data_packet[(m*2)] = current_ticks & 0xFF        # Low Byte
            data_packet[1 + (m*2)] = (current_ticks >> 8) & 0xFF  # High Byte
            
        # Push the bytes into the hardware output buffer for the Master to clock out
        for byte in data_packet:
            i2c_target.put_read_data(byte)
