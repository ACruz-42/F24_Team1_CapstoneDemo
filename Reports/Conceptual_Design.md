# Subsystems

### Motor Control

#### Atomic Subsystem Specifications
1) The motors shall operate at a voltage of less than 30 volts [S12].
1) The motor control subsystem shall be capable of an immediate termination of functions induced by an emergency stop button [S7].
1) The motors shall be capable of speeds allowing the robot to traverse the game field at least twice (once for collecting astral material, and once for the return trip) within three minutes (the length of a match) [S2]. 
1) The motors shall be capable of reversing the robot in the case that reversing the robot is the only method of not damaging the game field walls [S4]
1) The motor subsystem shall be be designed in such a way that accounts for background interference in the competition environment [S11]
1) The motor subsystem shall have a user manual that explains functionality and design intent [C2]
1) The motor subsystem shall adhere to applicable requirements in standard IEC 60204-1 pertaining to electrical supply, electromagnetic compatibility, emergency stop, and control circuit protection [C3].

### Navigation and Master Control

#### Atomic Subsystem Specifications
![Atomic Hardware Block Diagram](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/Navigation-Master-Control--Edits--Conceptual-Design/Reports/Photos/Conceptual%20Design/Master_Control_Subsystem_V1.png?raw=true)
The main component in the navigation and master control subsystem is the Jetson Nano. The choice of the Jetson Nano is discussed below. The Jetson Nano will take in data from the sensor-related subsystems, interpret that data, form , utilize a navigation algorithm to plot a course through the game field maximizing the points obtained, then communicate to the motor subsystem the distance and angle to the desired position of the robot. Additionally, at the start of each game round, the Jetson Nano will start and maintain the movement of the auxiliary motors (such as for the auger, the roller, and potentially the docking of the cosmic shipping containers).
#### Comparative Analysis of Potential Solutions.
The processing power required to complete the atomic specifications for navigation, master control, and potentially localization is higher than any microcontroller on the market. Determining processing suitability (or unsuitability) for a given task is best proven experimentally. The ESP32 microcontroller [10] and Teensy 3.5 [11] both struggle with real-time image processing and computer vision but are capable of it. Attempting to optimize one microcontroller to accomplish everything needed would likely require more time than available. Connecting multiple microcontrollers to separately accomplish computer vision, localization, and navigation tasks would require extensive communication work, be at higher risk of background interference (S11), and introduce more possible points of failure.

A system on module with carrier board like the Jetson Nano, or a single board computer like the Raspberry Pi have higher processing power than a given microcontroller. This means that all of the given tasks could be run on a single system, reducing complexity and failure points. The Jetson Nano presents a compelling solution due to its superior machine vision capabilities and lower power consumption, operating between 10-20W, compared to the Raspberry Pi 5's 25W. This efficiency not only enhances the overall system performance but also contributes to longer operational durations in battery-powered applications. Moreover, the Jetson Nano is specifically designed for AI and deep learning tasks, making it particularly well-suited for the real-time image processing and localization needs of our project [12]. By centralizing processing within the Jetson Nano, we can streamline system architecture, reducing the potential for communication delays and minimizing points of failure. Thus, opting for the Jetson Nano aligns with our goals of reliability and performance while ensuring effective resource management.

For a robot tasked with picking up static objects, such as small icosahedrons on a flat board, A* is particularly effective for this scenario, as it efficiently computes the shortest path to each target while accounting for the fixed locations of the astral material. Its heuristic-based approach [13] enables the robot to prioritize routes, reducing the overall travel time and enhancing operational efficiency. In comparison to algorithms like Dijkstra’s, which can be less efficient due to their exhaustive exploration of all paths, A* provides a more targeted and expedient solution [13]. Additionally, while algorithms like Greedy Best-First Search can quickly find a path, they may be prone to getting stuck in loops [14]. Given the Jetson Nano's processing capabilities, A* can be executed in real-time, allowing for quick recalculations if the robot encounters obstacles on its path. By employing A*, we can ensure that the robot navigates the board efficiently, optimizing its collection of materials while maintaining reliability and minimizing computational overhead. This approach effectively aligns with the project’s goals of streamlined performance and resource management.

#### Budget
|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|Jetson Nano | $260|1|$260
|Total|||$260|

#### Skills Necessary
Some hardware knowledge is required in determining the connections from the Jetson Nano to other subsystems, and to the auxiliary motors. Predominantly, the skills necessary are software related. Programming, knowledge of pathfinding algorithms, and experience with systems on module will be the limiting factors in the navigation and master control subsystem.


## Statement of Contributions

 - Alex Cruz - Navigation and Master Control (everything except specifications), Motor Control (only specifications)

## Works Cited
10.  ESP32 cam Object Detection. Accessed: Oct. 2024. [Online]. Available: https://webstore.iec.ch/en/publication/26037https://eloquentarduino.com/posts/esp32-cam-object-detection
11. Another T3.5 Rover with a OpenMV Camera (Machine Vision). Aug. 2017. Accessed: Oct. 2024. [Online]. Available: https://forum.pjrc.com/index.php?threads/another-t3-5-rover-with-a-openmv-camera-machine-vision.45741/
12. Nvidia Jetson Nano vs Raspberry Pi - Which one is better for your project? May 2024. Accessed: Oct. 2024.[Online].Available: https://www.socketxp.com/iot/nvidia-jetson-nano-vs-raspberry-pi-which-one-is-better-for-your-project/
13. Comparing Dijkstra’s and A* Search Algorithm. May 2022. Accessed: Oct. 2024. [Online]. Available: https://medium.com/@miguell.m/dijkstras-and-a-search-algorithm-2e67029d7749
14. A.I.: Informed Search Algorithms. Accessed: Oct. 2024 [Online]. Available: https://web.pdx.edu/~arhodes/ai6.pdf

