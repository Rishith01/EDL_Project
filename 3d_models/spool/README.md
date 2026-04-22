# Spool Design and Development

## Purpose
The spool assembly is the primary mechanical interface responsible for **tendon actuation**. It converts the rotational motion of the motors into controlled linear displacement, which pulls the tendons to actuate the continuum robotic links.

### Operational Logic
* **Dual-Tendon Control:** Each individual spool manages two tendons.
* **Differential Winding:** The spool utilizes a differential winding configuration. As the motor rotates, one tendon is wound (pulled) while the opposing tendon is unwound (released), enabling precise bidirectional control of the robot's bending.

---

## Iterative Development Process
The spool underwent approximately five iterations to move from a basic cylinder to a specialized mechanical component. This evolution was driven by the need to solve common failures in tendon-driven systems.

### Initial Design Failures
The earliest prototypes lacked internal constraints, leading to several issues:
* **Tendon Overlap:** Without dedicated paths, tendons would wind over themselves, changing the effective radius of the spool and causing inconsistent actuation.
* **Tendon Tangling:** The absence of separators allowed opposing tendons to interfere with each other, leading to mechanical jams.

### Design Refinements
To resolve these failures, the following features were integrated into subsequent iterations:
* **Wedge-Based Separators:** Internal dividers were added to create independent channels for each tendon, ensuring zero interference.
* **Tilted Routing Paths:** Angled internal geometry guides the tendon naturally during the winding process, preventing the thread from stacking on itself.
* **Chamfered Edges:** All contact surfaces are chamfered to reduce friction and minimize abrasive wear on the tendons during high-tension cycles.
* **Shaft-Compatible Mounting:** The core is designed with a "D-profile" to match the motor shaft, ensuring direct torque transfer.

---

## Technical Challenges and Constraints

The current design represents a balance between mechanical performance and the physical limitations of the materials and space.

### 1. Mechanical Limits and Slack Formation
A persistent challenge is the formation of tendon slack during extreme motion. Empirical testing reveals that when the continuum link is actuated beyond a **30-degree bending angle**, the mechanical limit of the link is reached. At this threshold, the tendon displacement ratio becomes non-linear, causing the opposing tendon to lose tension and develop slack.

### 2. Geometry Trade-offs
There is a direct trade-off regarding the height of the internal separators:
* **Separation vs. Size:** While taller separators provide better tendon isolation, they increase the overall spool height.
* **Cascading Footprint:** A taller spool necessitates a larger **base plate** and a taller **protective cap**. To maintain a compact robotic base, the separator height must be kept at a functional minimum.

### 3. D-Shaft Wear and Friction
Under high-torque conditions, the interface between the motor and the spool is a point of failure:
* **Material Fatigue:** Friction and high pressure cause the "D" shaped profile of the motor shaft to gradually wear down the internal profile of the spool.
* **Torque Slippage:** As this profile rounds off, it leads to backlash or total slippage, where the motor shaft rotates but fails to turn the spool effectively.

---
While this design represents the most effective solution developed within our current constraints, it is not necessarily the absolute optimal configuration, and future iterations may explore new geometries to facilitate greater bending angles.