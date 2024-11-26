# Detailed Design
## Function of the Subsystem


The navigation and master control subsystem utilizes a Jetson Nano as the core of the robot's systems. It takes data from the various sensor subsystems such as the LiDAR and ODOS sensors to determine its position and rotation on an internal grid, takes data from the camera subsystem to place the astral material on that grid, and then outputs high-level serial commands to the microcontroller associated with the motor control subsystem. Additionally, with the assistance of the Sensors and Object Detection subsystems, respectively, this subsystem will handle localization of the robot (i.e. its position on an internal map of the game board) and the placement of the astral material on the robot's internal map. It will manage all of this using a state machine that transitions its states based on the time remaining and feedback from the positional sensors.

## Specifications and Constraints

### Specifications:
1.  The Robot shall act autonomously (Specification 1 [1]). This is necessary for compliance with Game Manual 1
2.  The Robot shall be able to navigate to and position itself for the following tasks (Specification 2 [1]). This is necessary to maximize potential points.
	i. Navigate out of Landing Pad (i)
	ii.  Navigate within 3 seconds of Start LED (ii)
	iii.  Navigating into the cave (iii)
	iv.  Navigate to correct shipping pad (v)
	v.  Navigate to and allow for placement of team beacon (ix)
3.  The Robot shall account for background interference (Specification 11 [1]). This is to help reduce potential failure points.
### Constraints:
1.  The Robot shall stay on the game field (Specification 5 [1]). This is necessary for the safety of the team and all IEEE SECON staff members.
2.  The Robot shall cease all operation after 3 minute timer is done (Specification 10 [1]). This is necessary for the safety of the team and all IEEE SECON staff members.
3. The Robot shall immediately cease operations upon the usage of the emergency stop button (Specification 7 [1]). This is necessary for the safety of the team and all IEEE SECON staff members.

## Overview of Proposed Solution


The proposed solution centers around a hybrid navigation system combining preprogrammed paths with dynamic pathfinding for specific tasks. The system relies on a state machine and an event queue to coordinate high-level navigation with the microcontroller associated with the motor subsystem. Sensor feedback from LiDAR and odometry ensures real-time localization and adaptive positioning.

### **Core Components and Operation**

1.  **State Machine**  
    The majority of the robot's navigation tasks, such as moving between predefined locations like the landing pad, cave, and shipping pad, are handled via preprogrammed paths defined in a state machine. A state machine is a way of organizing potential states that, in this case, the robot can be in, and the transitions between these states. The routes these states mean algorithmic pathfinding can be avoided, reducing the need for heavy computation during a match.
    
   2.  **Event Queue**  
The event queue serves as a decoupling mechanism, separating the state machine and high-level logic from time-sensitive tasks [2]. Once a desired position or action is determined by the state machine, it is added to the event queue. The queue then processes these events sequentially, sending high-level commands—such as the required rotation and distance—to the microcontroller, which handles motor control. After the Arduino sends a command saying it's processed the current event or a period of time without movement, the next event is sent. This design allows the Jetson Nano to continue processing other high-level tasks, such as processing sensor data or computing navigation algorithms. 

2.  **A\* Pathfinding**  
    The A* algorithm is employed for states that involve picking up astral material. The way that A* works is as a form of Dijstrika's algorithm (an algorithm that explores each node in order of its distance from the starting node) [3]. In essence, A* is used as a way to balance finding the shortest path along with a given heuristic (in this case, proximity of the path to the nearest material) [4].  The state machine chooses the furthest astral material. A* plots a path to this material. The heuristic function in the A* algorithm heavily prioritizes paths  with astral material. If any astral material remain after reaching the destination, this process is repeated until either all astral material are gathered or the time allotted runs out. This approach balances optimal pathfinding with the competition's time constraints, allowing the robot to maximize points.


4. **Sensor-Driven Feedback Loop**  
    Positional data from LiDAR and odometry sensors provide continuous updates on the robot's location. This feedback ensures that the robot can accurately determine its current position and orientation, enabling adjustments when moving toward desired positions.
   
    

### **Specification Compliance**

1.  **Autonomous Operation (Specification 1)**  
    The integration of a state machine, event queue, and sensor feedback ensures that the robot operates autonomously, meeting the competition’s requirements for compliance with Game Manual 1.
    
2.  **Navigation (Specification 2)**
    
    -   Preprogrammed paths handle transitions between key locations (e.g., landing pad, cave, shipping pad).
    -   The A* algorithm dynamically optimizes the collection of astral materials by balancing path length and material prioritization.
3.  **Background Interference Tolerance (Specification 3)**  
    The feedback loop continuously corrects the robot's position using real-time sensor data from multiple sensors, mitigating the effects of environmental interference such as noise.

### **Constraints Compliance**    

4.  **Staying on the Game Field (Constraint 1)**  
    Predefined paths and real-time sensor feedback ensure the robot stays within boundaries, maintaining safety for participants and compliance with rules.
    
5.  **Ceasing Operation (Constraint 2)**  
    The state machine halts all operations when the timer reaches the three-minute limit. This is currently enforced programmatically as a high-level if statement inside of the main loop of the program.
    
6.  **Emergency Stop (Constraint 3)**  
    The emergency stop button overrides all active processes, immediately issuing a stop-motors command to the Arduino, ensuring compliance with safety requirements.
## Interface with Other Subsystems

#### Inputs:
-   **LiDAR Data**: Provides distance measurements to surrounding objects for real-time localization and obstacle detection.
    -   _Input Type_: Distance
    -   _Method_: I2C
-   **Odometry (OTOS) Data**: Applies Kalman filter to IMU, and optical sensor
    -   _Input Type_: Positional
    -   _Method_: I2C
  #### Outputs:
 -  ** Arduino Commands **
	 - _Output Type_: High-Level Commands
	 -  _Method_: Serial
## Godot Simulation
As a proof of concept for the overarching software architecture, a simulation in Godot was created. Godot was chosen for two main reasons: ease of prototyping, and the similarity of GDScript (Godot engine's inbuilt programming language) to Python. Additionally, closure (the ability for a function to retain memory outside of its enclosing scope [5]) makes the connection between state machine and event queue easier. At time of writing, this simulation is not fully operable but development is ongoing and the most up to date version (and source code) can be found at the following link. Note that support for operating systems other than Windows is not supported at this moment.

https://github.com/ACruz-42/F24-Team1-Capstone-Simulation

The state machine is only about half-way complete, but the relationship between main loop, state machine, and event queue are functional and proofs of the effectiveness of the design. Additionally, the A* algorithm works but is not interconnected with the other subsystems at this moment. 
## Buildable Schematic

![GPIO Pinout for Jetson Nano](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/Navigation-and-Master-Control-Detailed-Design/Documentation/Images/NavigationAndMasterControl/JetsonNanoConnections.png?raw=true)
![Jetson Nano USB Connections](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/Navigation-and-Master-Control-Detailed-Design/Documentation/Images/NavigationAndMasterControl/USBConnections.png?raw=true)
## Operational Flowchart

![Operational Flow](https://raw.githubusercontent.com/ACruz-42/F24_Team1_CapstoneDemo/22eb8c53bf35084e8dbe66c7c78e3c61e33c7ab1/Documentation/Images/NavigationAndMasterControl/MasterControlFlowChart.svg)

## BOM

|Item|Manufacturer|Part Number| Distributor|Distributor Part Number|Quantity|Price
| :- | :- | :- | :- | :- | :- | :- |
|Jetson Nano|Nvidia|#945-13450-0000-100|Amazon|B0B8DMPWJL|1|$215
|Total||||||$215|

Jetson Nano purchasing link: https://www.amazon.com/onboard-Robotics-Machine-Learning-Version/dp/B0B8DMPWJL

## Analysis

-   **Program Structure: State Machine, Event Queue, and Main Loop**  
    The decision to structure the software into a state machine, event queue, and main loop provides several advantages in maintainability and efficiency.
    
    -   The  state machine dictates the robot's high-level behavior, handling navigation between predefined locations and managing of transitions predictably and reliably. Additionally, clear delineations between states allow for easy debugging and experimentation
    -   The event queue serves as a time-independent intermediary, decoupling the state machine from real-time motor control. By abstracting motor commands to the Arduino, the event queue allows the Jetson Nano to continue executing high-level tasks without being constrained by execution delays.
    -   The main loop integrates the state machine and event queue together, ensuring continuous processing of sensor data and high-level commands. This structure ensures the robot can react dynamically to new information without compromising ongoing tasks, such as the operation of the emergency off-button or the detection of astral material. This design has already shown promise in the Godot simulation, where the interdependencies between these components have been successfully implemented, even if partially.
-   **Choice of Godot for Simulation**  
    Godot was selected as the simulation platform for its ease of prototyping and its GDScript language, which closely resembles Python—the programming language used on the Jetson Nano. This similarity allows for a smoother transition from simulated logic to real-world implementation.
    
    -   **Prototyping**: Godot’s user-friendly interface and node-based structure made it possible to iterate on designs quickly, enabling fast debugging and validation of core concepts such as the interaction between the state machine and event queue.
    -   **Code Translation**: GDScript’s support for closure simplifies the connection between the state machine and event queue. Python is similar in both its indent-based code, and closure-enabled programming. This structural alignment ensures the simulation’s code can be easily transferred to the actual robot.
    -   **Progress**: While the simulation is not fully operational, its current development demonstrates the effectiveness of the chosen structure. The integration of A* for astral material collection and the foundational elements of the state machine are already functional, further validating this choice.
    
    The simulation also provides a controlled environment to test edge cases and refine the robot’s behavior before physical implementation, significantly reducing development risks.
    
-   **Jetson Nano Over Raspberry Pi 5**  
    The Jetson Nano was selected over the Raspberry Pi 5 due to its superior compatibility with AI and machine vision tasks and its lower power consumption.
    
    -   **Processing Capabilities**: The Jetson Nano’s GPU is optimized for deep learning and computer vision tasks, enabling efficient real-time processing of sensor data (particularly the camera) and the A* algorithm. This capability directly supports the subsystem’s need for parallel computational power, particularly for tasks like localization and navigation.
   
    -   **Power Efficiency**: Operating between 10-20W, the Jetson Nano consumes significantly less power than the Raspberry Pi 5’s 25W, aligning with the project’s constraints on battery life. This efficiency ensures the robot can operate effectively within the competition’s time limit without exhausting power resources.


## Execution Plan

The current execution plans revolves around finishing the Godot simulation. The navigation portion of the navigation and master control subsystem should be trivial with the ability to use the GDScript code as a reference. Once all the ordered parts arrive, more importance will be placed on integrating the Jetson Nano with the various sensors and connection to the Arduino. By swiftly implementing the master control subsystem, development on the other subsystems can take place faster.

The simulation should, assuming current development pace, be finished before next semester.

The parts necessary for the other subsystems should arrive by the next semester.

Although the competition takes place in March, the plan is to finish by February and test during its duration. This leaves January and February to implement the navigation and master control systems. As the navigation subsystem should be easily transferrable, and the master control subsystem will be implemented with the assistance of the other subsystems, completing the robot should be be a viable task.
## References

[1] “Game Manual 2 V1.1.3,” IEEE, 2019. Accessed Nov. 26th, 2024. [Available Online] https://docs.google.com/document/d/1fN7bsJFpCJur66JkueRHXtlybt0m7QSY4Nn62lHAnrc/edit?tab=t.0
‌[2]R. Nystrom, “Game Programming Patterns”. United States. Genever Benning, 2014.
[3] GeeksforGeeks, “Dijsktra’s algorithm,” GeeksforGeeks, Nov. 19, 2018. Accessed Nov. 26th, 2024.  [Available Online] https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
[4] “A* Search Algorithm in Pytho,” GeeksforGeeks, Apr. 17, 2024.  Accessed Nov. 26th, 2024.  [Available Online] https://www.geeksforgeeks.org/a-search-algorithm-in-python/
‌[5]Rahul K, “An Introduction To Closures and Decorators in Python,” Earthly Blog, Jul. 18, 2023. Accessed Nov. 26, 2024. [Available Online]https://earthly.dev/blog/python-closures-decorators/
