# PCB information and Post-Fabrication Modifications

This PCB was designed using **Autodesk Fusion 360 (Fusion Electronics)**. It consists of 2 RPIs(both communicate over I2C, one is connected to the laptop[master] and the other is the slave). Slave RPI collects encoder information and relays it to the main RPI. We did this because we were worried about the computing capability of a single RPI. The master RPI also controls 2 GPIO port expanders[MCP23S17](over SPI), which provide a means to get feedback using the limit switches. This RPI also controls the Adafruit Featherwing motor drivers(via I2C), 3 of the drivers are stacked on top of each other using stackable header pins. It also contains an AMS1117 3.3V LDO to power the logic using a 12V input. More information about the schematic is available in the image below.

<img width="1550" height="1316" alt="image" src="https://github.com/user-attachments/assets/94ba14d2-cec5-4ff9-b2b4-5dc721d8ac28" />

Following fabrication, a few manual trace modifications (often referred to as "micro-surgeries" or bodge wires) are required on the physical board to correct an inconsistency with the SPI bus routing.

## Layout issue
### SPI issue
In the initial PCB design, the pin assignments for the **MCP23S17** (specifically the one closest to the Raspberry Pi) were mistakenly split across two different SPI buses. The original, incorrect routing was as follows:

* **`GP6`** (Pin 9, SPI0 SCK) -> MCP23S17 SPI SCK
* **`GP7`** (Pin 10, SPI0 TX) -> MCP23S17 SPI TX
* **`GP8`** (Pin 11, SPI1 RX) -> MCP23S17 SPI RX
* **`GP9`** (Pin 12, SPI0 CS) -> MCP23S17 SPI CS

### RPI VBUS issue
Main RPI's VSYS pin(Pin 39) was connected to the 3.3V power rail on the PCB. The issue was that the main RPI had to be connected to the laptop via a USB cable while operating the robot which caused the VSYS pin to output 5V as it was connected to the power line of the USB. This forced the bus to go to 5V and fried our LDO(AMS 1117).

## Fixes 
### Microsurgery
To maintain SPI consistency and ensure the interface operates on a unified bus, the SPI TX and SCK lines for this MCP23S17 must be manually reassigned. The following corrections were made on the fabricated board:

* **MCP23S17 SPI TX** (Pin 8) -> Reroute to **`GP14`** (Pin 19)
* **MCP23S17 SPI SCK** (Pin 9) -> Reroute to **`GP15`** (Pin 20)
  
### Cutting pin headers 
Originally, the 3.3V bus going towards the main RPI was cut, but then we realised that it provided power to the slave RPI and encoders down the line, so we had to solder the cut trace and cut the pin headers for VSYS and VBUS of the main RPI using flush cutters so that 5V and 3.3V are not shorted.

Here is the pico pinout for easy reference.

![pico-pinout](https://github.com/user-attachments/assets/23b73b6d-2a5e-4de8-abea-e4847d5206c8)

## Purpose of PCB
- Wiring Mangement
- Keeping the electronics in one compartment
- Connecting all power sources needed to one main power port
- Fixing Wire ends for N20 motor connectors ( There were too many motors, needed a way to sort and compile all motor connections ) 
