# Conceptual Design
## Introduction
## Restate Shall/May Statements
### Specifications
1)	The robot shall act autonomously. Rule G08 [2].
1)	The team shall design a robot to earn as many points as possible [2].
    1)	The robot may score 5 points by moving out of the landing pad [2].
    1)	The robot may score 5 points by moving out of the landing pad within 3 seconds of the Start LED [2].
    1)	The robot may score 15 points by moving into the cave [2].
    1)	The team may score 5 points by entering the Promotional Design Competition [2].
    1)	The robot may score 60 points for putting both containers in the correct zone [2].
    1)	The robot may score 34 points by completely supporting all Astral Material [2].
    1)	The robot may score 80 points by putting all Nebulite in its container [2].
    1)	The robot may score 108 points by putting all Geodinium in its container [2].
    1)	The robot may score 40 points for putting the Team Beacon in the Beacon Mast [2].
1)	The robot shall fit within a cube with 12 inches per side at the start of the match. Rule G04 [2].
1)	The robot shall be able to detect the walls of the arena, walls of the cave, and cave entrance. Rule S03 states that if the robot causes field damage, the team will be penalized. Detecting walls stops the robot from causing damage by moving into it [2].
1)	The robot shall stay on the game field. Rule S01 [2].
1)	The robot may have a single, simple electrical start button that shall be clearly labelled. The operation of this button shall prevent the robot from moving for five seconds. Rule R03 [1].
1)	The robot shall have a clearly labelled emergency stop button that immediately halts all functions safely and quickly. Rule R05 [1].
1)	The robot shall have a source of identification clearly associating it with Tennessee Technological University. Rule R10 [1].
1)	The robot may use light sources that shall not strobe, be excessively bright, or pose safety issues. Rule R17 [1].
1)	The robot shall cease operation of all its units after the allotted 3-minute timeframe of play is over, and no game element positions can be disturbed after time expires. Rule G07 [2]. 
1)	The robot shall account for background interference in the competition environment. Rule R13 [1].
1)	The robot shall sustain power of 30V maximum. Rule R16 [1].
	
### Constraints
1)	The robot shall read April Tags to help with Specifications 1, 2-v, 2-vii, 2-viii, and 2-ix. 
1)	The robot shall have a user manual that explains functionality and design intent for each subsystem.
1)	The robot shall adhere to applicable requirements in standard IEC 60204-1 pertaining to electrical supply, electromagnetic compatibility, emergency stop, and control circuit protection. The power-based and electromagnetic interactions of components in the motor control subsystem will need to adhere to this standard [3].

## High-Level Solution
### Hardware Block Diagram
### Operational Flow Chart

## Subsystems
### Camera
#### Atomic Subsystem Specifications

A camera is needed for specifcations 1, 2-vii, 2-viii, and 4 and constraint 1.
By having a camera, a robot can see very similarly to a human, but needs to have that information filter and processed in a way the robot can understand.
If it understands what it can effectively see, it shall be able to act autonomously, meeting specification 1.
Specifcations 2-vii and 2-viii both shall have the robot have a way to identify the materials in the arena.
Specifcation 4 shall have the robot detect different objects and obstacles.
The camera will be the only sensor in the front getting active feedback, due to the constraints placed by the device used to collect the materials.
The camera shall help keep the robot from running into obstacles in the front. 
Constraint 1 shall have the robot read April Tags. 
A camera is needed to read these.

#### Comparative Analysis of Potential Solutions
#### Ethical, Professional, and Standards Considerations
#### Resources
#### Budget
#### Skills

### General Sensors
#### Atomic Subsystem Specifications
#### Comparative Analysis of Potential Solutions

##### Line Sensor

The line sensor system needs to be able to detect the lines on the game field.
The primary solution is to use a reflectance sensor array.
A secondary solution is to use the camera.
The reflectance array would remove work from the camera and provide a single device whose goal is to detect the lines.
A single device focusing on line following would give better results and need less software than using a camera.
A reflectance array would have higher accuracy and less room for error than a camera.

##### Inertial Measurement Unit

The robot needs to know its location on the game field.
Muliple different sensors can read data provided by the robot to know its inertia, which gives it change in location over time.
These sensors include speedometers, tachometers, accelerometers, gyroscopes, and odometers.
Electric speedometers and odometers in vehicles use a magnet on the wheel to send a signal to a sensor near the wheel when the magnet passes by the sensor [4-5].
A tachometer measures the rotation of an object.
For the robot, it would measure the rotation of the wheels or motor shaft that drives the wheels.
An accelerometer measures the linear and angular acceleration of the robot in three dimensions.
A gyroscope measure the relative position to Earth's northern magnetic field.
A Speedometer or odometer would require parts to be constructed with them in place.
A tachometer would give the rotational speed and then need to be converted to a linear distance.
This would require the speed of all wheels to be known and certain algorithms to be made to account for turning.
Accelerometers give the total acceleration of the robot but need to be integrated to get position.
Gyroscopes give the position relative to a set object but can be interferred with noise from motors or magnetic materials.
Accelerometers and gyroscopes come in small, single-chip package that are interfaceable with a microcontroller and are known as inertial measurement units [6].
However, a tachometer would require two individual units to measure each of the motors or wheels.

##### Location Sensor

Specification 3 requires the robot to detect walls of the arena and cave to keep it from running into and damaging them.
Both an infrared sensor and an ultrasonic sensor would be able to detect the walls of the arena.
The infrared sensor, such as a time-of-flight or LiDAR, would cost more but be more precise.
The ultrasonic sensor has a very large field-fo-view that could interact with the materials that are placed throughout the field.
The infrared sensor has a smaller field-of-view that allows it to ignore the materials so that it can see tha absolute limits of the arena [7-8].

A second option for a location sensor could be a computer mouse.
They have a navigation chip that uses light to detect change in position.
The biggest issue is that they need to be very close to the object that they are detecting.
This means the mouse would need to be sliding along the ground.
The light used on the mouse also needs to be a continous LED and not a strobe light [9].

##### Start LED Sensor

Specification 2-ii requires the robot to start based on an input from a LED.
The simplest method is to use a photoresistor.
A photoresistor gets a lower resistance as the incident light increases.
This change in resistance can be read as a change in voltage on the lower side of the photoresistor.
A photoresistor is a simple and robust sensor that will work easily and repeatedly [10].

##### Magnetic Sensor

Specifications 2-vii and 2-viii require the material to be in its proper container for maximum points.
The easiest way to distinguish between the two is to use a magnetic, or hall effect, sensor.
Hall effect sensors produce a more positive or negative voltage depending on whether it detects a positive or negative magnetic field.
A different voltage gives a way for the microcontroller to determine where a certain material should go [11].

A second option is to use weight.
This require whatever is being used to transport the material to be weighed as well.
Unless, the material is placed directly on a scale, but then it also has to be moved off of the scale.
The weight sensor would also need to account for the acceleration of the robot, which gives more room for error and causes more work for software.

#### Ethical, Professional, and Standards Considerations

Resources and materials uses for this subsystem will be built following an expected use.
This use will be listed in their datasheets, and their datasheets will be followed properly.
The rules point out safety measures that will be taken throughout the competition.
A rule that sensors need to abide by is no visible strobe lights.
Furthermore, if using non-visble lasers, lasers will need to be safe for human interaction.

#### Resources

Each sensor will need to be purchased at least once.
The robot will need three of either ultrasonic or LiDAR based sensors, two for each side and one for the back.
Depending on budget, it may be a good idea to purchase extra in the case of a failure.
All sensors will need to be calibrated and properly connected.

#### Budget

|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|Reflectance Array|$10|1|$10|
|Inerital Measurement Unit|$30|1|$30|
|LiDAR|$45|3|$135|
|Photoresistor|$4|1|$4|
|Hall Effect Sensor|$4|1|$4|
|Total|||$183|

#### Skills

Software for the each of the sensors will need to be made.
The reflectance array, inertial measurement unit, and LiDAR will take the most work.
The other two should be a simple voltage comparison, or trigger.
The first three will need to be tested repeatedly.
The gyroscope on the inertial measurement unit will need to be tested with the motors running and with the magnetic material.


### Navigation and Master Control

#### Atomic Subsystem Specifications
![Atomic Hardware Block Diagram](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/Navigation-Master-Control--Edits--Conceptual-Design/Reports/Photos/Conceptual%20Design/Master_Control_Subsystem_V1.png?raw=true)
The main component in the navigation and master control subsystem is the Jetson Nano. The choice of the Jetson Nano is discussed below. The Jetson Nano will take in data from the sensor-related subsystems, interpret that data, form , utilize a navigation algorithm to plot a course through the game field maximizing the points obtained, then communicate to the motor subsystem the distance and angle to the desired position of the robot. Additionally, at the start of each game round, the Jetson Nano will start and maintain the movement of the auxiliary motors (such as for the auger, the roller, and potentially the docking of the cosmic shipping containers).
#### Comparative Analysis of Potential Solutions.
The processing power required to complete the atomic specifications for navigation, master control, and potentially localization is higher than any microcontroller on the market. Determining processing suitability (or unsuitability) for a given task is best proven experimentally. The ESP32 microcontroller [15] and Teensy 3.5 [16] both struggle with real-time image processing and computer vision but are capable of it. Attempting to optimize one microcontroller to accomplish everything needed would likely require more time than available. Connecting multiple microcontrollers to separately accomplish computer vision, localization, and navigation tasks would require extensive communication work, be at higher risk of background interference (S11), and introduce more possible points of failure.

A system on module with carrier board like the Jetson Nano, or a single board computer like the Raspberry Pi have higher processing power than a given microcontroller. This means that all of the given tasks could be run on a single system, reducing complexity and failure points. The Jetson Nano presents a compelling solution due to its superior machine vision capabilities and lower power consumption, operating between 10-20W, compared to the Raspberry Pi 5's 25W. This efficiency not only enhances the overall system performance but also contributes to longer operational durations in battery-powered applications. Moreover, the Jetson Nano is specifically designed for AI and deep learning tasks, making it particularly well-suited for the real-time image processing and localization needs of our project [12]. By centralizing processing within the Jetson Nano, we can streamline system architecture, reducing the potential for communication delays and minimizing points of failure. Thus, opting for the Jetson Nano aligns with our goals of reliability and performance while ensuring effective resource management.

For a robot tasked with picking up static objects, such as small icosahedrons on a flat board, A* is particularly effective for this scenario, as it efficiently computes the shortest path to each target while accounting for the fixed locations of the astral material. Its heuristic-based approach [13] enables the robot to prioritize routes, reducing the overall travel time and enhancing operational efficiency. In comparison to algorithms like Dijkstra’s, which can be less efficient due to their exhaustive exploration of all paths, A* provides a more targeted and expedient solution [13]. Additionally, while algorithms like Greedy Best-First Search can quickly find a path, they may be prone to getting stuck in loops [14]. Given the Jetson Nano's processing capabilities, A* can be executed in real-time, allowing for quick recalculations if the robot encounters obstacles on its path. By employing A*, we can ensure that the robot navigates the board efficiently, optimizing its collection of materials while maintaining reliability and minimizing computational overhead. This approach effectively aligns with the project’s goals of streamlined performance and resource management.

#### Ethical, Professional, and Standards Considerations
#### Resources

#### Budget
|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|Jetson Nano | $260|1|$260
|Total|||$260|

#### Skills Necessary
Some hardware knowledge is required in determining the connections from the Jetson Nano to other subsystems, and to the auxiliary motors. Predominantly, the skills necessary are software related. Programming, knowledge of pathfinding algorithms, and experience with systems on module will be the limiting factors in the navigation and master control subsystem.


### Motor Control

#### Atomic Subsystem Specifications
1) The motors shall operate at a voltage of less than 30 volts [S12].
1) The motor control subsystem shall be capable of an immediate termination of functions induced by an emergency stop button [S7].
1) The motors shall be capable of speeds allowing the robot to traverse the game field at least twice (once for collecting astral material, and once for the return trip) within three minutes (the length of a match) [S2]. 
1) The motors shall be capable of reversing the robot in the case that reversing the robot is the only method of not damaging the game field walls [S4]
1) The motor subsystem shall be be designed in such a way that accounts for background interference in the competition environment [S11]
1) The motor subsystem shall have a user manual that explains functionality and design intent [C2]
1) The motor subsystem shall adhere to applicable requirements in standard IEC 60204-1 pertaining to electrical supply, electromagnetic compatibility, emergency stop, and control circuit protection [C3].
#### Comparative Analysis of Potential Solutions
#### Ethical, Professional, and Standards Considerations
#### Resources
#### Budget
#### Skills

### Power Management
#### Atomic Subsystem Specifications
#### Comparative Analysis of Potential Solutions
#### Ethical, Professional, and Standards Considerations
#### Resources
#### Budget
#### Skills

## Timeline
## Statement of Contributions
  - Sean Borchers -
  - Alex Cruz - Navigation and Master Control (everything except specifications), Motor Control (only specifications)
  - Sam Hunter -
  - Alejandro Moore -
  - Dakota Moye -

## Works Cited
1.	â€œMining Mayhem â€“ Game Manual 1.â€ Version 1.1, Apr. 2024. Accessed: Sep. 2024. [Online]. Available: https://docs.google.com/document/d/1hTvIeRj649eyGU8oWLR_yD-mYgayySX7tRQBbetUCqc/edit 
2.	â€œMining Mayhem â€“ Game Manual 2â€ Version 1.1.3, Aug. 2024. Accessed: Sep. 2024. [Online]. Available: https://docs.google.com/document/d/1fN7bsJFpCJur66JkueRHXtlybt0m7QSY4Nn62lHAnrc/edit 
3.	Safety of machinery - Electrical equipment of machines. 2016. Accessed: Sep. 2024. [Online]. Available: https://webstore.iec.ch/en/publication/26037
4.	C. Woodford. "Speedometers." explainthatstuff.com. Mar. 2023. Accessed: Oct. 2024. [Online]. Available: https://www.explainthatstuff.com/how-speedometer-works.html
5.	K. Nice. "How Odometers Work." howstuffworks.com. Jan. 2001. Accessed: Oct. 2024. [Online]. Available: https://auto.howstuffworks.com/car-driving-safety/safety-regulatory-devices/odometer.htm#pt2
6.	yida. "What is a Time of Flight Sensor and How does a ToF Sensor work?" seeedstudio.com. 2019. Accessed: Oct. 2024. [Online]. Available: https://www.seeedstudio.com/blog/2020/01/08/what-is-a-time-of-flight-sensor-and-how-does-a-tof-sensor-work/
7.	gunengyu. "Grove - Ultrasonic Ranger." seeedstudio.com. Mar. 2023. Accessed: Oct. 2024. [Online]. Available: https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
8.	Ralph. "Whatâ€™s the Difference Between an Accelerometer, Gyroscope and IMU Sensors?" intorobotics.com. Sep. 2023. Accessed: Oct. 2024. [Online]. Available: https://intorobotics.com/accelerometer-gyroscope-and-imu-sensors-in-robotics/#3_List_of_IMU_Sensors
9.	"Optical Mouse Sensors." digikey.com. May 2007. Accessed: Oct. 2024. [Online]. Avilable: https://media.digikey.com/pdf/Data%20Sheets/Avago%20PDFs/ToolKitSelectionGuide.pdf
10.	"GL125 Series Photoresistor." knowing-tech.com. Accessed: Oct. 2024. [Online]. Avilable: https://knowing-tech.com/wp-content/uploads/data/g/GL12528.pdf
11.	"LINEAR HALL-EFFECT IC." digikey.com. Rev.1.3, Aug. 2010. Accessed: Oct. 2024. [Online]. Avilable: https://www.digikey.com/htmldatasheets/production/1364519/0/0/1/ah49e.html?utm_adgroup=General&utm_source=bing&utm_medium=cpc&utm_campaign=Dynamic%20Search_EN_RLSA&utm_term=digikey&utm_content=General&utm_id=bi_cmp-384476624_adg-1302921504343623_ad-81432643449113_dat-2333232393680005:aud-807631099:loc-190_dev-c_ext-_prd-&msclkid=ef9edc5046c81a3f6ce4bb4050601364
12. Nvidia Jetson Nano vs Raspberry Pi - Which one is better for your project? May 2024. Accessed: Oct. 2024.[Online].Available: https://www.socketxp.com/iot/nvidia-jetson-nano-vs-raspberry-pi-which-one-is-better-for-your-project/
13. Comparing Dijkstra’s and A* Search Algorithm. May 2022. Accessed: Oct. 2024. [Online]. Available: https://medium.com/@miguell.m/dijkstras-and-a-search-algorithm-2e67029d7749
14. A.I.: Informed Search Algorithms. Accessed: Oct. 2024 [Online]. Available: https://web.pdx.edu/~arhodes/ai6.pdf
10.  ESP32 cam Object Detection. Accessed: Oct. 2024. [Online]. Available: https://webstore.iec.ch/en/publication/26037https://eloquentarduino.com/posts/esp32-cam-object-detection
11. Another T3.5 Rover with a OpenMV Camera (Machine Vision). Aug. 2017. Accessed: Oct. 2024. [Online]. Available: https://forum.pjrc.com/index.php?threads/another-t3-5-rover-with-a-openmv-camera-machine-vision.45741/
