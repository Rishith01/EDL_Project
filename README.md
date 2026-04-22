<!-- Do Not Change the below line. It will affect your workflow badge -->
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/9lqHKop1)

![Docs Added](https://github.com/edl-iitb/edl-26-project-submission-edl26_tue16/actions/workflows/classroom.yml/badge.svg)

<!-- ADD YOUR CHANGES AFTER THIS LINE -->

# SACE(Secure Adaptive Continuum Explorer)
**Team TUE-16 | Indian Institute of Technology Bombay**

---

## Team Members
* **Arijit Paul** (23B1219)
* **Arshit Singh** (23B1275)
* **Prithvi Sangam** (23B1292)
* **Rishith Gupta** (23B1234)
* **Veeresh S K** (23B1309)

---

## Project Abstract
This project investigates the practical implementation of **soft robotics** through the development of a modular, tentacle-based end effector on a continuum backbone. The system is engineered to navigate highly constrained environments and perform adaptive grasping of irregular objects. 

The architecture consists of a **continuum robotic arm featuring four flexible segments** capable of extending from a compact enclosure. By integrating 10 degrees of freedom (DOF), tendon-driven actuation, and real-time visual feedback, the robot demonstrates the capability of compliant structures to achieve dexterity and safety in applications where traditional rigid-link manipulators are insufficient.

---

## Key Technical Features
* **Deployable Mechanism:** Engineered for high spatial efficiency, allowing the arm to extend from a compact housing for maximum reach-to-storage ratio.
* **Continuum Kinematics:** A multi-link flexible structure that facilitates smooth, non-discrete bending for complex maneuvering in tight spaces.
* **Adaptive Morphology:** The tentacle-inspired design conforms naturally to the geometry of target objects, ensuring secure grasping through compliant contact.
* **Teleoperated Control:** Real-time operation via a gaming controller/click based interface, mapping user input directly to multi-segment motion.
* **Integrated Vision System:** An endoscope camera provides a live stream to the operator for precise navigation and targeting.
* **Active Safety Array:** Integrated limit switches detect external obstacles and mechanical limits to prevent system damage and ensure safe motion.
* **Modularity:** The system is partitioned into independent subsystems, allowing for streamlined repair, scaling, and iterative refinement.

---

## System Overview

### Hardware Architecture
* **Controller Architecture:** Dual Raspberry Pi Pico microcontrollers configured in a Master–Slave hierarchy to distribute real-time processing loads.
* **Motor Control:** Three Adafruit FeatherWing Motor Drivers, selected for their high-density power management and compact footprint.
* **Actuation:** 11 N20 micro-gear motors dedicated to tendon-driven link manipulation through specialized differential spools.
* **Sensing Array:** 16 Limit Switches (distributed as 4 per continuum segment) for obstacle detection and motion constraint.
* **Vision:** A high-resolution endoscope camera module for front-facing orientation and feedback with 60 degree field of view.
* **Electronics:** A custom-designed PCB for efficient power distribution and signal routing, including 12V to 3.3V power conversion.

### Software Architecture
* **Workstation Logic:** Python-based control scripts on the laptop for signal processing, controller mapping, and user interface management.
* **Embedded Firmware:** MicroPython-based scripts running on the Raspberry Pi Pico for low-level hardware control and motor actuation.
* **Visual Pipeline:** Python-based live feed processing for real-time operator guidance.
The flowcharts and execution logic are present in the folder READMEs. Refer to particular folder for more details.
---

## Working Principle
1.  **Input Acquisition:** The operator provides motion commands through a gaming controller/click and keyboard interface.
2.  **Signal Processing:** The laptop-based Python environment translates given commands into specific link-actuation commands and calculates which link is to move how much using our control algorithm.
3.  **Command Dispatch:** Control signals are transmitted to the Master Raspberry Pi Pico.
4.  **Distributed Execution:** The Master Pico coordinates with the Slave Pico and the motor driver array to execute precise motor rotations.
5.  **Actuation:** N20 motors rotate the differential spools, pulling tendons to induce controlled bending in the continuum segments.
6.  **Feedback Loop:** Real-time visual data from the camera and tactile data from the limit switches are monitored to guide navigation and prevent collisions.

---

## Final Deliverables

The project delivers a fully functional soft robotic system with the following capabilities:

- **Continuum Robotic Arm System**
  - A four-segment tendon-driven continuum arm capable of smooth, multi-directional bending  
  - Designed to navigate constrained environments with high flexibility  

- **Tentacle-Based End Effector**
  - A compliant gripper capable of adaptive grasping of irregular objects  
  - Independently actuated for controlled gripping  

- **Teleoperation Interface**
  - Real-time control using keyboard, mouse, and gaming controller  
  - Supports intuitive interaction through a camera-based interface  

- **Vision-Guided Operation**
  - Integrated endoscope camera providing live visual feedback  
  - Enables precise navigation and targeting  

- **Safety Mechanism**
  - Limit switch array for obstacle detection and motion constraint  
  - Automatic escape responses to prevent system damage  

- **Custom Embedded Control System**
  - Dual Raspberry Pi Pico architecture (Master–Slave)  
  - Distributed control for motor actuation and hardware interfacing  

- **Mechanical and Electronic Integration**
  - Fully assembled system including:
    - Custom PCB  
    - Motor driver integration  
    - Tendon-driven actuation system  

- **User Interface and Control Software**
  - Python-based host system for trajectory planning and control  
  - MicroPython firmware for real-time embedded execution  

---

## Repository Structure

```plaintext
├── src/                # Source code (MicroPython + Python)
├── pcb/                # PCB designs and schematics
│   └── PCB1/
│       ├── design.brd
│       ├── schematic.src
│       └── pictures/   # Fabricated PCB and Fusion 360 layouts
├── 3d_models/          # CAD models (Fusion 360)
│   ├── tentacle/
│   ├── continuum/
│   ├── base_plate/
|   ├── enclosure/
│   ├── spool/
|   └── motor_mount/
├── reports/            # Project Milestone Documentation
│   ├── milestone0/
│   ├── milestone1/
│   ├── milestone2/
|   ├── milestone3/
│   └── milestone4/
├── others/
│   ├── user_manual/    # Operational instructions
│   ├── presentation/   # System demonstration
|       ├── slides/
│       └── video/    
|   ├── images/         # Images of final setup
|   ├── extras/         # Extra images and videos
|   └── diagrams/       # Relevant diagrams
├── bom.xls             # Detailed Bill of Materials
└── README.md
```

## Repository Walkthrough

### src/
Contains all source code for the system, including:
- MicroPython code for the Raspberry Pi Pico, master and slave RPi (motor control, hardware interfacing)
- Python-based host code for user interaction, trajectory planning, and communication  

Each subfolder is organized based on the execution platform and includes relevant README files describing usage and setup.

---

### pcb/
Includes all PCB-related design files and documentation:
- Schematic and layout files for the custom PCB  
- Fabrication outputs and board design files  
- Images of the fabricated PCB and assembled boards  

The PCB integrates motor drivers, power distribution, and control interfaces required for system operation.

---

### 3d_models/
Contains all mechanical CAD designs used in the project.  
The models are organized into subsystem-level folders:
- **tentacle and top_link/** – End-effector for gripping and top link continuum link
- **continuum/** – Flexible links enabling motion  
- **base_plate/** – Structural base and motor mounting  
- **enclosure/** – Outer housing (laser-cut design)  
- **spools/** – Tendon winding mechanisms  
- **Motor Mount/** – Motor holding structures  

Each folder includes design files, images, and descriptions of functionality and assembly.

---

### reports/
Contains all milestone reports documenting the project lifecycle:
- Concept development  
- Design iterations  
- Implementation progress  
- Final system evaluation  

All reports are provided in PDF format.

---

### others/
Contains supporting materials required for understanding and operating the system:
- **user_manual/** – Step-by-step instructions for setup and operation  
- **presentation/** – Slides and demonstration video  
- **images/** – Photographs of the final assembled system  
- **diagrams/** – Wiring diagrams and system-level representations
- **extras/** - Extra images and videos during testing and prototyping

---

### bom.xls
A detailed Bill of Materials listing all components used in the project, including:
- Electronic components  
- Mechanical parts  
- Consumables and fabrication materials  

Each entry includes quantity, description, and source information.

---

### README.md
The root documentation file providing:
- Project overview and objectives  
- System description  
- Repository structure  
- Key features and functionality  
---

## Technical Constraints and Operational Limits
The current design represents a balance between mechanical performance and the physical limitations of the materials and space.

1. **Bending Threshold**: Empirical testing established a stable operational limit of approximately 30° per link. Beyond this angle, mechanical stress increases significantly, contributing to tendon slack issues within the actuation system.

2. **Control Paradigm**: Currently restricted to manual teleoperation; autonomous path planning and inverse kinematics are not yet implemented.

3. **Backbone Hysteresis and Droop**: The use of glue gun sticks as a central backbone introduces stability issues. After bending, the backbone may fail to return to a perfectly linear state, causing the robot to droop. Ensuring the backbone is fixed at the start and end of each link segment is critical for maintaining a consistent neutral axis.

4. **Tendon Dynamics**: Issues regarding tendon slack and potential thread interference in the shared spool design persist during extreme ranges of motion.

---


## Course Reflection and Learnings

### Technical Learnings

This project provided hands-on experience across multiple domains:

- **Mechanical Design**
  - Designing for tolerances and iterative prototyping  
  - Understanding trade-offs between flexibility and structural strength  
  - Challenges in tendon-driven systems such as slack and routing  

- **Embedded Systems**
  - Working with dual microcontroller architecture (Master–Slave)  
  - Interfacing peripherals such as motor drivers, encoders, and port expanders  
  - Handling real-time constraints in MicroPython  

- **Control Systems**
  - Implementing coordinated multi-link motion  
  - Understanding limitations of open-loop control  
  - Practical challenges in achieving smooth motion  

- **PCB Design**
  - Designing and debugging custom PCBs  
  - Managing power distribution and signal routing  
  - Handling hardware failures and component sensitivity  

- **System Integration**
  - Combining mechanical, electrical, and software subsystems  
  - Debugging issues arising only during full system integration  

---

### Team Challenges and Adaptation

- **Subsystem Isolation and Testing**
  - Each subsystem (mechanical, electronics, software) was tested independently before integration  
  - This helped in identifying issues early and reducing debugging complexity  

- **Iterative Prototyping**
  - Multiple iterations were required, especially for:
    - Spool design  
    - Tentacle structure  
    - Continuum links  
  - Rapid prototyping enabled quick validation and refinement  

- **Cross-Domain Collaboration**
  - Team members developed working knowledge of other subsystems  
  - Ensured continuity when specific members were unavailable  

- **Integration Challenges**
  - Most issues arose during integration rather than individual subsystem development  
  - Required coordinated debugging sessions and time alignment among team members  

---

### Honest Reflection

- While the final system achieves the intended functionality, a significant portion of the effort was spent resolving **practical engineering challenges** rather than implementing advanced features  

- Mechanical reliability (tolerances, tendon routing, slack management) proved to be more critical and time-consuming than initially anticipated  

- Hardware failures (motor drivers, microcontrollers) highlighted the importance of robust electrical design and protection  

- The control system works effectively for manual operation, but lacks higher-level intelligence and automation  

- Overall, the project demonstrates a **working proof-of-concept**, but not a fully optimized or production-ready system  

---

### Incomplete Features and Limitations

The following aspects remain incomplete:

- **Autonomous Control**
  - No implementation of inverse kinematics or automated path planning  
  - Reason: Complexity of modeling continuum kinematics and time constraints  

- **Closed-Loop Feedback**
  - Limited use of encoder data for precise control  
  - Reason: Integration complexity and prioritization of basic functionality  

- **Robust Tendon Management**
  - Issues with slack, overlap, and spool behavior at extreme motions  
  - Reason: Mechanical design constraints and limited iteration time  

- **System Stability**
  - Vibrations and minor inaccuracies in motion  
  - Reason: Structural limitations and compact design constraints  

---

### Future Work 

- **Inverse Kinematics for Continuum Arms**
  - Develop simplified models for controlled positioning  

- **Improved Tendon Mechanism**
  - Dedicated spool designs with better separation and tension control  

- **Enhanced Feedback Control**
  - Utilize encoder data for closed-loop control  
  - Implement PID-based corrections  

- **Structural Improvements**
  - Replace glue stick backbone with engineered compliant structures  

- **Miniaturization**
  - Redesign base plate and enclosure for reduced footprint  

- **System Robustness**
  - Add electrical protection (snubbers, proper grounding, shielding)  

---

## Acknowledgements
We extend our sincere gratitude to Prof. Siddharth Tallur, Prof. Himanshu Bahirat, and Prof. P. C. Pandey for their continuous guidance and valuable insights throughout this project. We also acknowledge the support of Ankur, Maheshwar, the WEL RAs and TAs for their technical assistance during the development and debugging phases.

## Inspiration 
The inspiration for the tentacle end effector came from this youtube video of the spirobs bot: https://m.youtube.com/watch?v=Q2yYclPaEV0

Inspiration for the continuum arm came from this video from continnum robotics lab of university of toronto. https://m.youtube.com/watch?v=MxBeUQay8YM
