# ⚙️ Slave Encoder Coprocessor

## 📌 Overview
High-speed encoder tracking using PIO.

---

## 🧠 Architecture
```mermaid
flowchart LR
    E[Encoders] --> P[PIO]
    P --> S[Slave]
    S -->|I2C| M[Master]
```

---

# 🔁 **2. Slave Algorithm Flowchart**

```mermaid
flowchart LR

    %% ===== INIT =====
    A[Start] --> B[Initialize System]
    B --> C[Setup PIO and I2C]
    C --> D[Main Loop]

    %% ===== CORE =====
    D --> E[Update Encoder Counts]

    %% ===== SPLIT =====
    E --> F{Event Check}

    %% LEFT COLUMN (COMMAND PATH)
    F -->|Command| G[Read Command]
    G --> H{Reset Command}
    H -->|Yes| I[Reset Encoder]
    H -->|No| J[Ignore Command]

    %% RIGHT COLUMN (DATA PATH)
    F -->|Read Request| K[Prepare Encoder Data]
    K --> L[Send Data to Master]

    %% CENTER (NO EVENT)
    F -->|No Event| M[Continue]

    %% ===== MERGE =====
    I --> N[Loop Back]
    J --> N
    L --> N
    M --> N

    %% ===== LOOP =====
    N --> D
```

## ⚙️ Features
- 8 encoders
- PIO-based counting
- I2C streaming

---

## ▶️ Run
- Flash MicroPython
- Upload files
- Run main.py

---

## 📂 Source Files & Structure
```plaintext
/src/slave
├── main.py              # Core loop (PIO + I2C handling)
├── i2c_responder.py     # Low-level I2C peripheral implementation
```

## Platform and Specifications
- Thonny used for flashing code on Rasberry Pico
- Micropython used for master and slave RPi code ( Version MicroPython v1.25.0 )
- Python3 used for code for Teleop
- Communication protocols used : SPI , I2C and USB Serial ( UART over USB )
