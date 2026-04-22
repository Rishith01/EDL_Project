"""
=====================================================================================
This module provides a lightweight, high-speed MicroPython SPI driver for the 
Microchip MCP23S17 16-Bit I/O Expander.

Core Responsibilities:
1. HAEN Bootstrapping : 
   By default, the MCP23S17 boots up with Hardware Address Enable (HAEN) turned off, 
   meaning it ignores its physical address pins (A0, A1, A2) and only responds to 
   address 0. This driver intelligently broadcasts the HAEN-enable command to 
   address 0 first, then seamlessly shifts to the user-defined physical address.
   
2. Default Input Configuration : 
   Configures all 16 pins across 
   Port A and Port B as digital inputs upon initialization.
   
3. Internal Pull-Up Activation : 
   Enables the chip's internal 100kΩ pull-up 
   resistors on all 16 pins.
   
4. 16-Bit Aggregation : 
   Provides a `read_all()` method that fetches both 8-bit 
   ports and bit-shifts them into a single 16-bit integer. 
=====================================================================================
"""

import machine

class MCP23S17:
    def __init__(self, spi, cs, address=1):
        self.spi = spi
        self.cs = cs
        self.cs.value(1) # Ensure chip is deselected to start

        # --------- HAEN Bootstrapping ----------- 
        # 1. Start with Address 000 (0x40) because HAEN is off by default
        self.opcode = 0x40   
        
        # 2. Send the HAEN enable command to Address 000
        # IOCON register = 0x0A (Enable Hardware Addressing)
        self.write_reg(0x0A, 0x08)  
        
        # 3. NOW shift to your actual physical wired address (e.g., 001)
        # Shift the 3-bit address into the correct position (Bits 1, 2, 3)
        self.opcode = 0x40 | (address << 1)  
        # Now the address is correctly fixed
      
        # -------- INITIALIZATION --------
        # CONFIGURE BOTH PORTS AS INPUTS (0xFF = 11111111)
        self.write_reg(0x00, 0xFF)  # IODIRA 
        self.write_reg(0x01, 0xFF)  # IODIRB 

        # ENABLE INTERNAL PULL-UPS ON BOTH PORTS
        self.write_reg(0x0C, 0xFF)  # GPPUA
        self.write_reg(0x0D, 0xFF)  # GPPUB

    # ---------- LOW LEVEL ----------
    def write_reg(self, reg, val):
        self.cs.value(0)
        # Send 3 bytes: Write Opcode, Register Address, Data Value
        self.spi.write(bytearray([self.opcode, reg, val]))
        self.cs.value(1)

    def read_reg(self, reg):
        self.cs.value(0)
        # Send 2 bytes: Read Opcode (opcode | 1), Register Address
        self.spi.write(bytearray([self.opcode | 1, reg]))
        # Read the 1 byte response
        result = self.spi.read(1)
        self.cs.value(1)
        return result[0]

    # ---------- READ FUNCTIONS ----------
    def read_gpioa(self):
        return self.read_reg(0x12)

    def read_gpiob(self):
        return self.read_reg(0x13)

    def read_all(self):
        """Returns a single 16-bit integer representing all 16 pins"""
        a = self.read_gpioa()
        b = self.read_gpiob()
        # Shift Port B left by 8 bits, and combine with Port A
        return (b << 8) | a
