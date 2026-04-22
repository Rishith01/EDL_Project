# 🧠 Master Controller (RPi Pico)

## 📌 Overview
Real-time execution + safety.

---

## 🧠 Architecture
```mermaid
flowchart TD
    H[Host] --> M[Master]
    M --> D[Motor Drivers]
    M --> S[Slave]
    M --> L[Limit Switches]
```

## Flowchart
```mermaid
flowchart TD

    %% ===== INIT =====
    A[Start] --> B[Initialize Hardware]
    B --> C[Brake All Motors]
    C --> D[Enter Main Loop]

    %% ===== MAIN LOOP =====
    D --> E{Check Limit Switches}

    %% ===== LIMIT HANDLING =====
    E -->|Triggered| F[Stop All Motors]
    F --> G[Send LIMIT to Host]
    G --> D

    E -->|No Trigger| H{Check Serial Input}

    %% ===== SERIAL COMMANDS =====
    H -->|Command Available| I{Command Type}

    I -->|START| J[Parse Motor ID, Direction, Angle, PWM]
    J --> K{Motor Type?}

    K -->|Lead Screw| L[Start Motor + Start Timer]
    L --> D

    K -->|Link Motor| M[Convert Angle to Encoder Ticks]
    M --> N[Reset Encoder via Slave]
    N --> O[Start Motor + Set Target]
    O --> D

    I -->|GRIP| P[Control Gripper Motor]
    P --> D

    I -->|STOP| Q[Brake All Motors]
    Q --> D

    H -->|No Input| R{Any Motor Active?}

    %% ===== FEEDBACK LOOP =====
    R -->|Yes| S[Read Encoder Data from Slave]

    S --> T{Target Reached?}
    T -->|Yes| U[Brake Motor]
    U --> D

    T -->|No| V{Timeout > 2s?}
    V -->|Yes| W[Brake Motor + Send TIMEOUT]
    W --> D

    V -->|No| D

    R -->|No| D
```
## File Interaction

```mermaid
flowchart LR
    MAIN[main.py] --> FD[feather_driver.py]
    MAIN --> MCP[mcp23s17.py]
    FD --> PCA[pca9685.py]
```

---

## ⚙️ Responsibilities
- Serial commands
- PWM motor control
- Encoder feedback loop
- Limit detection

---

## ▶️ Run
- Flash MicroPython
- Upload files
- Run main.py

---

## 📁 File Structure
```plaintext
/src/master
├── main.py            # Core control loop (scheduler + logic)
├── feather_driver.py  # Motor driver abstraction (PCA9685 control)
├── mcp23s17.py        # SPI driver for limit switch expanders
└── pca9685.py         # Low-level PWM driver
```

## Platform and Specifications
- Thonny used for flashing code on Rasberry Pico
- Micropython used for master and slave RPi code ( Version MicroPython v1.25.0 )
- Python3 used for code for Teleop
- Communication protocols used : SPI , I2C and USB Serial ( UART over USB )
