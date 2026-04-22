# Continuum Link Design and Development

## Purpose
Continuum links serve as the primary structural and functional units of the robot, designed to provide **flexible, multi-directional motion**. Unlike traditional rigid-body joints, these links allow the robot to achieve smooth curvature, enabling it to navigate through highly constrained or irregular environments.

---

## Technical Structure and Components
Each link is a precision-engineered manifold designed to manage structural support, sensing, and actuation routing. 
* **Actuation Channels:** Four dedicated tendon pathways arranged at 90-degree intervals.
* **Spring Mounting Interface:** Four mounting points for springs that provide the restorative force necessary to return the link to a neutral position.
* **Obstacle Avoidance System:** Four limit switches are integrated at 90-degree intervals, positioned strategically between the springs and the tendons to detect external contact.
* **Internal Manifolds:** Specialized internal paths are provided specifically for the routing of limit switch wiring to ensure it does not interfere with moving parts.
* **Vinyl Tubing Guides:** Vertical guides house vinyl tubing, which is critical for independent link control. By fixing the relative motion of the link below, the tubing ensures that a tendon passing through it can directly actuate the current link without being affected by the movement of previous segments.

---

## Working Principle
The links operate on a tendon-driven continuum mechanics principle:
* **Antagonistic Pairs:** Tendons are arranged in opposing pairs; pulling one side creates a compressive force that results in a controlled bend in that direction.
* **Individual Link Control:** The use of tubing allows the system to isolate forces, enabling the differential actuation of specific links to achieve complex shapes rather than a simple uniform curve.
* **Central Backbone:** A central core (utilizing a glue-stick material) provides high compressive strength to withstand tendon tension while maintaining the lateral flexibility required for bending.

---

## Iterative Refinement
The design progressed through approximately three major iterations, focusing on structural durability and routing efficiency:
* **Structural Reinforcement:** Early versions suffered from mechanical failure where the pulling force on the vinyl tubing caused the link structure to break. Later iterations improved the housing geometry to better distribute these localized stresses.
* **Pathing Integrity:** Internal routing was refined to accommodate the limit switch wiring and tendons simultaneously without entanglement or signal interference.
* **Anchor Point Optimization:** The holes for tendon anchoring were adjusted to ensure they could withstand the high tension required for maximum deflection.

---

## Current Constraints and Design Considerations
While the current link configuration is highly functional, specific mechanical trade-offs were identified:

* **Backbone Hysteresis and Droop:** The use of glue gun sticks as a central backbone introduces significant stability issues. After bending, the backbone often fails to return to a perfectly linear state. This residual bending results in twists within the gaps between links, causing the robot to "droop" toward one side in its relaxed position. To maintain a consistent neutral axis, it is necessary to fix the backbone position at specific intermediate points—specifically at the start and end of each link segment.

* **Spring-Based Support:** The current use of springs for support provides the required restorative force and allows for bending, but it was primarily implemented as a baseline support mechanism. A more specialized structural alternative could potentially offer better uniform resistance and stability.

---

This design represents a robust solution for independent link control and 360-degree obstacle detection within the 30-degree limit. Future developments may explore more rigid intermediate backbone constraints or alternative support structures to achieve even greater curvature and stability.