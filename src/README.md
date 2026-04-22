# Continuum Robot Control System

## Overview
A distributed control system for a tendon-driven continuum robot:
- **Laptop (Host)**: planning, UI, safety decisions
- **Master Pico**: real-time control, safety arbitration
- **Slave Pico**: high-speed encoder processing

---

## System Architecture
```mermaid
flowchart LR
    %% ===== USER & HOST =====
    U[User] --> H[Laptop Host]

    %% ===== COMMAND PATH =====
    H -->|USB Serial Commands| M[Master Pico]

    %% ===== ACTUATION PATH =====
    M -->|I2C Control| D[PCA9685 Drivers]
    D -->|PWM Signals| MOT[DC Motors]

    %% ===== FEEDBACK LOOP =====
    MOT -->|Quadrature Signals| ENC[Encoders]
    ENC -->|GPIO| S[Slave Pico]
    S -->|I2C Telemetry| M

    %% ===== LIMIT SAFETY LOOP =====
    LS[Limit Switches] -->|Digital Signals| MCP[MCP23S17 Port Expanders]
    MCP -->|SPI| M

    %% ===== STATUS BACK TO HOST =====
    M -->|LIMIT / TIMEOUT Events| H
```

---

## Data Flow
```mermaid
sequenceDiagram
    participant U as User
    participant H as Laptop
    participant M as Master
    participant S as Slave

    U->>H: Input (click/keys)
    H->>M: START / GRIP
    M->>S: Reset encoder
    S-->>M: Encoder ticks
    M-->>H: LIMIT / TIMEOUT
```

---

## Project Structure
```
/Project-Root
├── src/
│   ├── Python_VSCode/
│   │   └── Teleop/
│   └── Micropython_Thonny/
│       ├── Master_RPi/
│       └── Slave_RPi/
```
## Step-by-step Execution Flow
- Load master code and Slave code to 2 different Rasberry Picos.
- Make the connections as given in the pcb section ( refer to the schematic and the guideline in PCB README.md ).
- Connect main Rasberry Pico to Laptop and run the main.py on master RPI.
- Run the code ( see the COM port connections for USB and Endoscope Camera ).
- Done! Now see Teleop README.md to find the commands.

## Platform and Specifications
- Thonny used for flashing code on Rasberry Pico
- Micropython used for master and slave RPi code ( Version MicroPython v1.25.0 )
- Python3 used for code for Teleop
- Communication protocols used : SPI , I2C and USB Serial ( UART over USB )
