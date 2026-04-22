#  3D Models Overview

This directory contains all mechanical design files used in the Tentacle Arm End Effector project. The designs follow a **modular architecture**, enabling independent development, testing, and iteration of each subsystem.

---

##  Design Philosophy
- **Modularity** – Each subsystem (tentacle, continuum links, base, etc.) is designed independently for ease of iteration and replacement  
- **Tendon-driven actuation** – Motion is achieved through routed tendons enabling flexible bending  
- **Iterative prototyping** – Multiple versions were developed to resolve tolerance, routing, and mechanical constraints  
- **Ease of fabrication** – Designs are optimized for rapid prototyping using accessible manufacturing methods  

---

##  Manufacturing Methods
- **3D Printing ** – Used for all structural components (STL files)
- **Laser Cutting** – Used for enclosure panels (DXF files)  

---

##  Materials Used
- **PLA (Primary Material)**  
  - Chosen for its balance between rigidity, printability, and cost  
  - Provides sufficient structural strength while allowing minor compliance  

- **TPU (Tested)**  
  - Too flexible for structural components  

- **Resin (Tested)**  
  - High precision but expensive and limited in build volume  

- **Acrylic (6mm)**  
  - Used for enclosure panels via laser cutting  

---

##  Design Considerations
- **Tolerance management** was critical across all components  
- Minor post-processing (filing/drilling) was required in tight-fit regions  
- **Tendon routing** and **vinyl tubing guidance** were key constraints  
- Structural strength balanced with flexibility for continuum motion  

---

##  System Integration
The mechanical assembly follows this structure:
entacle → Continuum Links (×4) → Base Plate → Lead Screw → Enclosure


- The **tentacle** performs grasping  
- The **continuum links** enable flexible motion  
- The **base plate** houses motors and routing  
- The **lead screw** enables linear extension  
- The **enclosure** houses the entire system  

---

## Folder Structure
```plaintext
.
├── enclosure/     # Laser-cut enclosure designs (DXF)
├── base_plate/    # Base plate designs and iterations
├── spools/        # Tendon winding mechanisms
├── continuum/     # Continuum link structures
└── tentacle/      # Gripper/tentacle designs
```


Each folder contains design files along with images and detailed README documentation.

## Assembly Instructions

The assembly of the Tentacle Arm End Effector is carried out in stages, starting from the continuum structure to the final enclosure integration.

---

### 1. Continuum Link Assembly

- Attach the continuum link segments along a central **hot glue stick backbone**, maintaining uniform spacing  
- For each link:
  - Tie **four fishing lines** at 90° intervals around the link  
  - Ensure consistent positioning for symmetric actuation  

---

### 2. Tendon Routing

- Route each fishing line through the **vinyl tubing guides**  
- This ensures:
  - Reduced friction  
  - Controlled motion  
  - Proper alignment between links  

- Repeat this process for all continuum links and route all tendons down to the base plate  

---

### 3. Base Plate and Motor Assembly

- Mount all motors securely onto the **base plate** using appropriate screws  
- Route the fishing lines through designated holes in the base plate  
- Wind each tendon onto its respective **spool mechanism**  
- Attach the spools firmly onto the **motor D-shafts**

---

### 4. Lead Screw Integration

- Connect the **base plate** to the lead screw mechanism  
- Attach the lead screw to the motor using a **shaft coupler**  
- Mount the lead screw motor onto the **motor mount**

---

### 5. Enclosure Integration

- Fix the motor mount and lead screw assembly inside the **enclosure**  
- Ensure alignment of the continuum structure with the enclosure exit opening  

- For additional stability:
  - Support the lead screw using **pillow bearings**  
  - Secure them to the enclosure structure  

---

### 6. Final Checks

- Verify all tendons are properly tensioned  
- Ensure smooth rotation of motors and spools  
- Check for:
  - No tendon overlap  
  - No obstruction in tubing  
  - Free movement of continuum links 
- Can check for each motor's working and mechanical issues by running individual commands on Thonny for each motor. 

---

### Notes

- Minor adjustments (tightening, re-routing, or trimming) may be required due to tolerance variations  
- Proper tendon tension is critical for accurate motion and control  