🔹 diagrams/

This folder includes technical diagrams that describe the system design and operation:
```
Hardware interconnection diagrams

PCB wiring diagram
```
These help in understanding how different subsystems interact.


# Wiring and Electrical Connections

## Overview

The wiring of the system primarily consists of:
- Power distribution (12V and ground)
- Motor and encoder connections
- Limit switch interfacing
- Communication between modules (PCB, Raspberry Pi Pico, motor drivers)

The design emphasizes modularity, ease of debugging, and safe operation.

---

## Power Distribution

- A **12V SMPS** is used as the main power source  
- Power is supplied to the PCB through **screw terminals**

### Wiring Convention
- **Red** → +12V (VCC)  
- **Black** → Ground (GND)  
- Other colors → Signal lines (motors, encoders, limit switches)

### Notes
- Ensure tight screw terminal connections to avoid voltage drops  
- Ground is shared across all modules (common ground reference)

---

## Motor and Encoder Connections

- N20 motors are connected to the PCB via **motor driver outputs (Adafruit FeatherWing)**  
- Each motor is paired with an **encoder**, which relays feedback to the **Slave Raspberry Pi Pico**

### Mapping
- Motors are indexed from **0 to 10**
- Direction control:
  - Achieved in software  
  - Can be reversed by swapping motor polarity if required  

### Encoder Interface
- Encoder signals are routed to the **Slave Pico**
- Used for:
  - Motion tracking  
  - Basic feedback  

---

## Limit Switch Connections

- A total of ~16 limit switches are used  
- Distributed across continuum links for collision detection and motion limits  

### Electrical Configuration
- Each switch is connected as a **digital input**
- Typical wiring:
  - One terminal → GND  
  - Other terminal → GPIO (via port expander)  

- Operates in **pull-up configuration**:
  - Default state → HIGH  
  - Triggered (pressed) → LOW  

---

## Port Expander Interface

- Limit switches are connected via **GPIO port expanders (MCP23S17 over SPI)**

### Function
- Expands available input pins  
- Reduces load on the Raspberry Pi Pico  

### Mapping
- Mapping of:
  - Expander ID (`mcp_id`)
  - Pin number  

is handled in software and can be modified without hardware changes  

---

## Motor Driver Connections

- **Adafruit FeatherWing motor drivers** are used for motor control  
- Controlled via I2C from the Master Pico  

### Features
- Compact integration of multiple motor channels  
- Simplifies wiring and reduces PCB complexity  

---

## Connector Types

The system uses the following connectors:

- **Screw Terminals**
  - For power input (12V, GND)
  - Provides secure and reliable connections  

- **Pin Headers / JST Connectors (as applicable)**
  - For:
    - Motor connections  
    - Encoder signals  
    - Limit switches  

- **Motor Leads**
  - Pre-attached wires from motors used for:
    - Motor power  
    - Encoder output  

---

## Intermodule Connections

### 1. Laptop ↔ Master Pico
- USB Serial communication  
- Used for command transmission and feedback  

---

### 2. Master Pico ↔ Motor Drivers
- I2C communication  
- Controls motor speed and direction  

---

### 3. Master Pico ↔ Port Expanders
- SPI communication  
- Reads limit switch states  

---

### 4. Slave Pico ↔ Encoders
- Direct GPIO connections  
- Handles encoder signal processing  

---

### 5. PCB ↔ Mechanical System
- Motors mounted on base plate  
- Wiring routed through structured paths to avoid interference  

---

## Design Considerations

- Modular wiring enables easy debugging and replacement  
- Color-coded wiring improves readability and maintenance  
- Separation of power and signal lines reduces noise  
- Port expanders simplify large-scale input handling  

---

## Notes

- Ensure all grounds are common across modules  
- Use masking tape to avoid shorting as done in our figures
- Check polarity before powering the system  
- Loose wiring may result in:
  - False limit switch triggers  
  - Unstable motor behavior  

- All connections should be verified before operation for safe functioning of the system
=======
