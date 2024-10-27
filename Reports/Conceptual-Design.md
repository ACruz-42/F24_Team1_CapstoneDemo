# Conceptual Design
## Introduction
The Institute of Electrical and Electronics Engineers (IEEE) hosts a yearly hardware competition at its Southeast Conference (SECON) for students to compete in. Tennessee Technological University has competed in the IEEE SECON hardware competition in the past but has often had issues undiscovered until the actual competition. The aim of this project is to design and build a robust, consistent robot to place as highly as possible. 


### Restatement of Problem and Scope:
The 2025 competition rules and limitations will be listed in the specifications section below but, in short, its challenge takes place over 3 minutes and involves collecting and separating two types of 40mm icosahedrons (astral material) randomly distributed on the field. Geodinium, one type of astral material, is slightly magnetic and heavier than Nebulite, the other type. The challenge is to sort these two types of astral material into two designated containers, and then bring those containers to a randomly chosen area on the board. Additionally, there is a dark roofed “cave” area with further Geodinium and Nebulite. The board is relatively simple with few obstacles beyond the containers and astral materials to navigate around, and as such, the goal is to focus on reliability followed by an extensive testing period. There are two types of matches, qualification matches in which the eight teams with the highest scoring qualification matches, and elimination matches where two teams directly compete against each other’s scores [1].

Time is the major limiting factor as the competition takes place early into the second semester of this capstone project. By following an accelerated design and build schedule, this limits the design and testing periods for this project. The point distribution greatly rewards being able to correctly and reliably sort Geodinium and Nebulite into their corresponding containers. By implementing a camera for computer vision purposes and a heavy emphasis on testing, the robot can reliably gain the astral material points and unreliably gain others (such as for placing a beacon into a designated position), performance can be optimized for both the qualification matches and elimination matches [1].
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

### Camera

The camera will be the robot's primary means of object detection, and will also help with line detection. The camera will will send its depth and image input to the microprocessor where the input will be filtered to a usable state, while that is happening the other inputs from general sensors will also be fed to the microcoprocessor and each input will be filtered to obtain a usable input. After usable inputs are obtained the sensor and camera inputs will be be put into object and line detection algorithms, which will localize the astral material, game field and cave walls, lines, and shipping containers on the robot's inner grid system. All this information will then be processed and sent to navigation and master control. 

### General Sensors

A suite of sensor will be used for this project.
A sensor is needed to detect the lines on the ground, difference between the two materials, the LED to start the robot, and the current location of the robot.
The line sensor will need to detect the difference between the black ground and the white lines.
This will need to be used when the robot is entering and exiting the cave to make sure it is properly aligned.
The start LED sensor will need to detect the LED that starts the robot at the beginning of the match.
The start LED will have a single task of sending a signal once a LED lights up, informing the robot to begin operations.
The location sensor will need to know where the robot is.
The location of the robot will be continuously updated as the robot traverses the field.
The location sensor will use sensor fusion in order to minimize drift found in most sensors used to navigate.

All sensors will send their data to the Jetson Nano for processing and interpretation.
Data will be filtered and compared for sensor fusion for the location sensor.
For the sensors that rely solely on their own information, they will be filtered and then used as inputs to help navigate and run the robot.
All sensors will help in making sure the robot acts autonomously.

### Navigation and Master Control

The Jetson Nano functions as the hub for the both navigation algorithms and master control functions. In short, it will take sensor data from the camera and general sensors, work with these systems to localize the robot to a specific position on an internal grid, and then utilize an algorithm to find a path that will achieve the robot's objectives within the given time frame. The minimum functioning product of this subsystem will be able to, given mostly accurate sensor data, reliably navigate the robot to pick up a maximum amount of astral material within the given time frame and with few mistakes. The ideal functioning product of this subsystem will be able to reliably navigate the robot to pick up all the astral material, and finish all other objectives within the time frame with no mistakes, even given fuzzy sensor data.


### Motor Control
The motor control subsystem functions as the feedback-based reaction center for the robot’s processes. It uses the input taken in from sensory data, such as object and line detection or map navigation, and follows the commands given to it from the master control to perform the physical responses of the robot. Motor control can include the following components: a microcontroller (MC), motor, motor driver, encoder, power supply, and specific components for noise reduction and circuit protection [1]. The motor microcontroller carries the digital signal commands for the designated motor to operate as required. However, the power that the MC needs to function is not enough in comparison to what the motor needs. Therefore, it is essential to have a component that can step up the power from the MC to the motor. This is the purpose of the motor driver. The motor microcontroller sends a digital signal to the driver using PWM to set the desired motor speed. Encoders that detect the motor shaft speed/position to provide the actual speed of the motors are useful for completing a closed loop feedback system, such as with PID control [2]. All logic control circuitry, which includes the master control and encoders, will receive low voltage from the power subsystem, while the motor driver will receive high voltage in order to provide the high power needs of the motors.

### Power Management

### Hardware Block Diagram
![Hardware Block Diagram](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/1fa993cd7f82cd33691eebe0be5f6cf70c7abc0e/Reports/Photos/Conceptual%20Design/BlockDiagram.jpg)
### Operational Flow Chart
![Operation Flow Chart](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/1fa993cd7f82cd33691eebe0be5f6cf70c7abc0e/Reports/Photos/Conceptual%20Design/Robot_Flowchart.png)

## Subsystems
### Camera
Customer: Dakota Moye

Designer: Sam Hunter

#### Atomic Subsystem Specifications

1. The robot shall act autonomously [S1].
2. The camera shall detect the Nebulite [S2-vii].
3. The camera shall detect the Geodinium [S2-viii].
4. The robot shall be able to detect the walls of the arena, walls of the cave, and cave entrance. Rule S03 states that if the robot causes field damage, the team will be penalized. Detecting walls stops the robot from causing damage by moving into it. The camera will be the only sensor on the front and will need to do the listed objectives [S4].
5. The camera shall read April Tags to help with Specifications 1, 2-v, 2-vii, 2-viii, and 2-ix [C1].

#### Comparative Analysis of Potential Solutions

The robot will need a camera with both RGB and dpeth sensing capabillites.
One option is a RGBD camera using an infrared projector, this camera
has 2 cameras in it, 1 is a 2D camera which will be used like a normal 2D camera for video and RGB values.
The second camera is an infrared camera which uses an infrared laser detector which seperates objects into layers. 
The primary purpose of the camera will be to identify the astral material and then accurately place it on the game field for the navigation algorithm.
The camera will use the 2D RGB camera to find and differentiate the different objects, including astral material, game field walls, and cave walls.
It will then use the infrared camera to accurately place the objects in relation to the robot.[24]


Another option is to use a stereo vision 3d camera.
This type of camera uses 2 or more 2d RGB cameras to contruct a concept of depth in the same way humans do with our 2 eyes.
The camera takes the 2 or more inputs from slightly different perspectives then compares them to each other and does some calculations,
then from these calculations a distance is determined.
This distance is then used in the same way it will be for an infrared camera, to locate the objects on the game field.
Either way the cameras will need to interface with the microprocessor using a USB connection.

#### Resources

The robot will only need 1 such camera, which will be mounted on the front of the robot facing forward. 

#### Budget

|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|RGBD Camera|$272|1|$272|
|Total|||$272|

#### Skills

The image from the camera will need to be processed so that the algorithms using it will be able to pull useful data.
The camera will also need to be interfaced with the master control microprossesor 

### General Sensors
Customer: Sam Hunter

Designer: Dakota Moye

#### Atomic Subsystem Specifications

1) The robot's sensors shall be able to find the walls of the game field and the cave, specifications 4 and 5.
1) The robot's sensors shall be able to detect the white lines on the game board, specifications 2 iii and v.
1) The robot's sensors shall be bale to detect when the start LED turns on, specifications 2 i and ii.
1) The robot's sensors shall be able to detect the magnetic fields of the Geodinium, specifications 2 vii and viii.
1) The robot's sensors shall be able to work effectively despite background interference in the competition environment, specification 11.
1) The robot's general sensor subsystem shall have a user manual that explains functionality and design intent, constraint 2.

#### Comparative Analysis of Potential Solutions

##### Line Sensor

The line sensor system needs to be able to detect the lines on the game field.
The primary solution is to use a reflectance sensor array.
A secondary solution is to use the camera.
The reflectance array would remove work from the camera and provide a single device whose goal is to detect the lines.
A single device focusing on line following would give better results and need less software than using a camera.
A reflectance array would have higher accuracy and less room for error than a camera [25].

A reflectance array will be used for this project.

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

The accelerometer and gyroscope give the most data for the least amount of effort.
They will be used for this project.

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

The infrared sensors will be used for this project.
The mouse will be experimented with if times permits.

##### Start LED Sensor

Specification 2-ii requires the robot to start based on an input from a LED.
The simplest method is to use a photoresistor.
A photoresistor gets a lower resistance as the incident light increases.
This change in resistance can be read as a change in voltage on the lower side of the photoresistor.
A photoresistor is a simple and robust sensor that will work easily and repeatedly [10].

A photoresistor will be used for this project.

##### Magnetic Sensor

Specifications 2-vii and 2-viii require the material to be in its proper container for maximum points.
The easiest way to distinguish between the two is to use a magnetic, or hall effect, sensor.
Hall effect sensors produce a more positive or negative voltage depending on whether it detects a positive or negative magnetic field.
A different voltage gives a way for the microcontroller to determine where a certain material should go [11].

A second option is to use weight.
This requires whatever is being used to transport the material to be weighed as well.
Unless, the material is placed directly on a scale, but then it also has to be moved off of the scale.
The weight sensor would also need to account for the acceleration of the robot, which gives more room for error and causes more work for software.

The Hall effect sensor will be used for this project.

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
Customer: Alejandro Moore

Designer: Alex Cruz

#### Atomic Subsystem Specifications
The main component in the navigation and master control subsystem is the Jetson Nano. The choice of the Jetson Nano is discussed below. The Jetson Nano will take in data from the sensor-related subsystems via I2C, SPI, and USB (as depicted in the block diagram), interpret that data, form a position from that interpretation, utilize a navigation algorithm to plot a course through the game field maximizing the points obtained, then communicate to the motor subsystem the distance and angle to the desired position of the robot. Additionally, at the start of each game round, the Jetson Nano will start and maintain the movement of the auxiliary motors (such as for the auger, the roller, and potentially the docking of the cosmic shipping containers).
#### Comparative Analysis of Potential Solutions.
The processing power required to complete the atomic specifications for navigation, master control, and potentially localization is higher than any microcontroller on the market. Determining processing suitability (or unsuitability) for a given task is best proven experimentally. The ESP32 microcontroller [15] and Teensy 3.5 [16] both struggle with real-time image processing and computer vision but are capable of it. Attempting to optimize one microcontroller to accomplish everything needed would likely require more time than available. Connecting multiple microcontrollers to separately accomplish computer vision, localization, and navigation tasks would require extensive communication work, be at higher risk of background interference (S11), and introduce more possible points of failure.

A system on module with carrier board like the Jetson Nano, or a single board computer like the Raspberry Pi have higher processing power than a given microcontroller. This means that all of the given tasks could be run on a single system, reducing complexity and failure points. The Jetson Nano presents a compelling solution due to its superior machine vision capabilities and lower power consumption, operating between 10-20W, compared to the Raspberry Pi 5's 25W. This efficiency not only enhances the overall system performance but also contributes to longer operational durations in battery-powered applications. Moreover, the Jetson Nano is specifically designed for AI and deep learning tasks, making it particularly well-suited for the real-time image processing and localization needs of our project [12]. By centralizing processing within the Jetson Nano, we can streamline system architecture, reducing the potential for communication delays and minimizing points of failure. Thus, opting for the Jetson Nano aligns with our goals of reliability and performance while ensuring effective resource management.

For a robot tasked with picking up static objects, such as small icosahedrons on a flat board, A* is particularly effective for this scenario, as it efficiently computes the shortest path to each target while accounting for the fixed locations of the astral material. Its heuristic-based approach [13] enables the robot to prioritize routes, reducing the overall travel time and enhancing operational efficiency. In comparison to algorithms like Dijkstra’s, which can be less efficient due to their exhaustive exploration of all paths, A* provides a more targeted and expedient solution [13]. Additionally, while algorithms like Greedy Best-First Search can quickly find a path, they may be prone to getting stuck in loops [14]. Given the Jetson Nano's processing capabilities, A* can be executed in real-time, allowing for quick recalculations if the robot encounters obstacles on its path. By employing A*, we can ensure that the robot navigates the board efficiently, optimizing its collection of materials while maintaining reliability and minimizing computational overhead. This approach effectively aligns with the project’s goals of streamlined performance and resource management.

#### Resources

#### Budget
|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|Jetson Nano | $260|1|$260
|Total|||$260|

#### Skills Necessary
Some hardware knowledge is required in determining the connections from the Jetson Nano to other subsystems, and to the auxiliary motors. Predominantly, the skills necessary are software related. Programming, knowledge of pathfinding algorithms, and experience with systems on module will be the limiting factors in the navigation and master control subsystem.


### Motor Control
Customer: Alex Cruz

Designer: Sean Borchers

#### Atomic Subsystem Specifications
1) The motors shall operate at a voltage of less than 30 volts [S12].
1) The motor control subsystem shall be capable of an immediate termination of functions induced by an emergency stop button [S7].
1) The motors shall be capable of speeds allowing the robot to traverse the game field at least twice (once for collecting astral material, and once for the return trip) within three minutes (the length of a match) [S2]. 
1) The motors shall be capable of reversing the robot in the case that reversing the robot is the only method of not damaging the game field walls [S4]
1) The motor subsystem shall be be designed in such a way that accounts for background interference in the competition environment [S11]
1) The motor subsystem shall have a user manual that explains functionality and design intent [C2]
1) The motor subsystem shall adhere to applicable requirements in standard IEC 60204-1 pertaining to electrical supply, electromagnetic compatibility, emergency stop, and control circuit protection [C3].
#### Comparative Analysis of Potential Solutions
##### Motor and Driver Selection
When looking at a comparison between the types of motors that could be used for the translational motion of the robot, there are two that stand out: brushed and brushless DC motors. Factors that must be considered for the motor and driver pairing include speed, available circuit space, electrical noise reduction (such as with back emf), and design complexity.

A brushed motor mechanically switches current in the motor windings so that the rotor can spin and create the torque needed to drive the wheels [19]. It uses a stationary magnetic field set by the stator and the energized coil windings of the rotor to create a magnetic attraction between the opposing magnetic poles of the rotor and the stator, generating the movement. This process has an advantage in design simplicity in that there is no need for a controller to switch the motor winding current [19]. Instead, physical conducting brushes have a voltage applied across them that connects to different sections of the windings at different times, creating the continuous rotation due to magnetic attraction. Brushed motors are also relatively inexpensive in comparison to brushless and provide good low-speed torque, but they can generate more electrical noise, which can disrupt logic circuitry [19]. 

The motor driver that is commonly paired with a brushed motor is an H-bridge module motor driver. In general, motor drivers use PWM (pulse-width modulation) to control the amount of voltage that gets to the motors based on a controlled duty cycle [20]. The H-bridge uses four switches that create an H-shape in the circuit schematic, with the exterior segments that hold each switch connecting to either power on the top or ground on the bottom [20]. At one time, either the top left and bottom right segment switches are closed, creating a particular direction of potential difference across the motor in the middle, or vice versa, with the polarity of the motor being flipped, which changes the direction. In this way, this type of motor driver can control the speed and direction of the motor relatively simply.

Brushless DC motors do not rotate by mechanical means, such as with brushes. Instead, they require control electronics that turn on certain motor windings on the stator, with permanent magnets being on the rotor, the opposite orientation of brushed [19]. The connection required between the driver and this kind of motor implements a three-phase circuit, alternating the provided current between the three wire connections. A brushless Electric Speed Controller (ESC) is used to control the speed and direction of the three-phase brushless motor connection. The advantages of a brushless motor and ESC pairing over the brushed motor include higher efficiency, good speed control, and low electrical noise, but this pairing falls short when it comes to price and complexity. 

Ultimately, the decision for the chosen motor and driver pairing must be able to provide the best combination of speed, noise reduction, price, and design/control simplicity. The brushed motor would reduce cost and design complexity in comparison to the brushless motor, but the main issue deals with the expressed concern of more electrical noise generated. If a solution can be implemented to deal with this issue, brushed motors would be the best option. A combination of noise reduction techniques can be implemented to be able to incorporate the use of brushed motors. When finding a solution that can satisfy these constraints, one can look to IC H-bridge motor drivers, such as the DRV8835, which provides built-in protection against reverse-voltage, under-voltage, over-current, and over-temperature [21]. The potential solutions that were considered previously for motor control to address efficient robot movement and reducing electrical noise were PID control, noise filtration using capacitors, and noise reduction using DAQ techniques. It is reasonable to use a combination of these techniques to reduce noise in the environment and satisfy Specification 11. Also, the additional solution of a flywheel diode would specifically target the high voltage generated by back emf in the motors, with the reverse-bias diode only drawing current when the supply is turned off and the remaining motor voltage needs somewhere to dissipate [22]. Having this under consideration, the brushed motor orientation becomes the best option for the combination of factors.

##### Encoder Selection

Based on the selection of the motor and driver, the encoder can be chosen to address the need for feedback in the motor control subsystem. The encoder should therefore be able to precisely detect the speed and direction of the motors while being as simple and inexpensive as possible. Regarding data collection, DC motor encoders have two main types: incremental and absolute rotary encoders. Incremental encoders convert angular shaft position to a digital signal, and they provide high-speed and high-accuracy measurement [18]. They are lacking in that they don’t provide absolute position information, but they are still a widely used type due to their simplicity and low price [18]. Absolute encoders provide precise positioning using unique identifiers for positions within the motor revolution, and they can keep accuracy after the system loses power [18]. Between the two options, the incremental encoder would be the best solution, as the main disadvantage of incremental in comparison to absolute is irrelevant for the purposes of the competition. The ability for absolute to keep position accuracy after power loss is mainly applicable for systems that repeatedly turn on and off, which is not the case for the competition robot, which will continuously run only once during play. 

The type of sensor for the encoder is also an important consideration, with the two main types being magnetic and optical sensors. Magnetic encoders use a sensing circuit, rotating wheel connected to the motor, and magnetic poles on the circumference of the wheel that each go by the sensor during rotation [18]. The interaction of each detected pole with the sensor creates a measurement of magnetic field strength that corresponds to motor speed. The major advantage of magnetic encoders is that they do not succumb to physical contamination from the environment. However, they have a notable disadvantage in their susceptibility to electrical interference from magnetic fields in the environment, such as through the motor back emf. Optical encoders use light to measure the position of the motor and transform it into a digital signal, and the main components of an optical encoder include a light, a sensor, and a rotating linear code disk [18]. The code disk is connected to the rotation of the motor and sits between the light and the sensor, with the different light and dark patterns on the disk being the input for the measurement of motor speed [18]. The main advantage of optical encoders is that they are unaffected by electrical noise, but they can be disrupted if contaminated by physical debris [23]. Due to the main factors being noise interference and physical contamination and given the relatively clean competition environment of play, the best option between these sensor types would be optical. Magnetic sensors would be more necessary if the environment was full of dirt, dust, and other debris that would interfere with the light, but this will not be a notable issue in the competition arena.

#### Resources

The following items are necessary for the completion of the motor control subsystem. In order for the motors to respond to environmental and robot feedback, a central microcontroller (Jetson Nano listed in Navigation and Master Control)  must be present to be able to properly distribute the large quantity of connections required for the robot to move and collect/sort astral material. In the current configuration, the robot will only need two driving brushed motors for translation along the ground, implementing the use of ball bearing wheels on the front and back for stability. However, these motors need a voltage regulator for speed and direction, which requires the use of two motor drivers, such as the L298N H-bridge module. In order to adjust motor commands based on the current state of the motors, the robot must collect positional data of the motor shafts, which employs the use of encoders, with optical encoders being a safe choice in comparison to magnetic encoders, which may disturb the low-level logic circuitry due to the magnetic properties. 

#### Budget

|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|Brushed Motors (12-24V)|~$60.00|2|$120.00|
|Motor Drivers (L298N H-bridge module)|$10.00|2|$20.00|
|Optical Encoders|$20.00|2|$40.00|
|Total|||$180.00|

#### Skills

For the Motor Control subsystem, there is mainly hardware implementation, but software is required for PID control. A team member with theoretical knowledge of PID feedback loops and technical experience in programming would be well-suited for this role. Classes in Controls and Robotics would help serve as a sufficient background for the project applications. 

### Power Management
Customer: Sean Borchers

Designer: Alejandro Moore

#### Atomic Subsystem Specifications

There are several quantifiable specifications and constraints for the power subsystem given the competition rules and the adherence to safe engineering practice.

1)	In accordance with Specification 2-ii and 6, the robot functionality may have a trigger based on a given Start LED controlled by the referee or through a clearly labeled electrical start button. 
1)	For the manual start button, the robot shall not move for five seconds after activation, but onboard commands can run during this time in preparation for play. 
1)	The robot shall be able to safely and efficiently pause all its functions using a clearly labeled emergency stop button according to Specification 7. 
1)	If there are multiple independently acting ‘Robot Units’, each shall have their own emergency stop button. 
1)	Regarding power system requirements, the robot shall sustain power at a maximum of 30V, as given by Specification 12. 
1)	The robot shall implement proper circuit shielding and isolation based on the disturbances from background interference in the competition environment, as given by Specification 11. 
1)	The circuitry of the robot shall account for and add appropriate devices to promote safety measures such as overcurrent, overload, and over-temperature protection, as per Constraint 3 [3]. 
1)	Low level sensor and measurement units shall require 5 VDC and remain operational throughout the 3 minute time of play.
1)	The Master Control (Jetson Nano) shall require 5 VDC and at least 2.5 A [26]. It shall remain operational throughout the 3 minute time of play.
1)	The brushed motor drivers shall require at least 5-7 VDC for logic input and at least 12 VDC for motor output, with 2A continuous current per channel [20]. It shall vary the power input to the motors throughout the 3 minute time of play depending on the desired motor speed as determined by robot weight, object detection, and match time. 

The power subsystem of this robot will be the electrical backbone of the project. Without a structured model of power management and distribution, the robot would not be able to meet all functions, specifications and constraints. For this subsystem to work correctly with the scope of the project, battery/(ies) shall be installed so that the robot can be powered without a cord attached to a wall socket.

#### Comparative Analysis of Potential Solutions

This power subsystem requires adequate power management and distribution of all hardware within the robot. Since we must power both the microcontroller and the motor subsystems, it would be wise to separate the power buses at a certain point so that neither subsystems connected to the power subsystem will interfere with each other, but work together towards a common goal. Based on last year’s SECON Modular-Based Robot, creating a power distribution circuit that isolates 2 batteries to power both subsystems we believe will be most optimal. For Specification 6 and 2-ii, the start button mentioned within the sensor section will be connected to the power subsystem. Once pressed, it will have both batteries provide sufficient voltage and current to both the motor and microcontroller, but will not start moving until 5 seconds after the button or LED receiver  is triggered. Similarly, Specification 7 refers to an Emergency Stop button that is required within the Game Rules. This E-Stop button will also be connected to the circuit. Once pressed, the circuit shall open the power bus to the motor while the bus to the microcontrollers will stay closed. Thus, giving the microcontroller power to process still, and cutting off all power to the motor for optimal safety while also saving critical data.

#### Resources

At least 2 batteries are needed for this solution that follows the specifications and constraints. We may be able to salvage an older e-stop button used in past CAPSTONE projects and test to see if it works within the circuit. Further schematics and simulations will be displayed to better explain the power subsystem structure.

#### Budget

|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|Lithium Iron Phosphate Battery|$91.43|2|$182.86|
|Lithium Iron Phosphate Battery Charger|$129.27|1|$129.27|
|Total|||$312.13|

#### Skills

A more in-depth block diagram of the power management/distribution subsystem will be made. Also, further schematics in Altium and simulations in LTSpice will be displayed to better explain the power subsystem structure. Some hardware installation for the power circuit will be required.

## Ethical, Professional, and Standards Considerations

The project will have an impact on the outreach of Tennessee Tech, with the team representing the school in this competition both technically and professionally. If the team can perform well, it will build on the image of the College of Engineering for prospective students, encouraging them to attend the university and be engaged in similar endeavors in the future. In preparing for the competition, the team will follow the IEEE Code of Ethics for respectful collaboration and safe design practice. To maintain a healthy relationship among team members while also holding each other accountable, each member completes evaluations for themselves and for the others on the team, providing opportunity for self-reflection of progress and for checking in on the progress of others. 

The Game Manual provided structures for the competition to follow IEEE guidelines and general electrical standards. Resources mentioned such as datasheets and procedures correlated with clean power transmission will be followed closely. For example, the E-stop mentioned in the rules are for the safety of the competitors, judges, and audience in the case of a motor malfunction.

The datasheet for the camera will be followed to ensure safe and correct usage. 
Furthermore, the way it will be used in competition, for navigation and object detection, matches very well with its intended use.
The only danger to humans this component coud pose is its use of an infrared laser projecter, however, the lazer projecter is very small and completely safe for use in close proximity of living beings.  

Resources and materials uses for this subsystem will be built following an expected use.
This use will be listed in their datasheets, and their datasheets will be followed properly.
The rules point out safety measures that will be taken throughout the competition.
A rule that sensors need to abide by is no visible strobe lights.
Furthermore, if using non-visble lasers, lasers will need to be safe for human interaction.

## Timeline

## Overall Budget
|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|Reflectance Array|$10|1|$10|
|Inerital Measurement Unit|$30|1|$30|
|LiDAR|$45|3|$135|
|Photoresistor|$4|1|$4|
|Hall Effect Sensor|$4|1|$4|
|Brushed Motors (12-24V)|~$60.00|2|$120.00|
|Motor Drivers (L298N H-bridge module)|$10.00|2|$20.00|
|Optical Encoders|$20.00|2|$40.00|
|Jetson Nano | $260|1|$260
|RGBD Camera|$272|1|$272|
|Total|||$???|

## Statement of Contributions
  - Sean Borchers - Motor Control Subsystem Information (Excluding Main Specifications), Power Management (only specifications)
  - Alex Cruz - Navigation and Master Control (everything except specifications), Motor Control (only specifications)
  - Sam Hunter - Camera(all except specifications), General Sensors(specifications)
  - Alejandro Moore - Power Management Subsystem Information
  - Dakota Moye - General Senors (except specifications), Camera (only specification), Operation Flowchart

## Works Cited
1.	“Mining Mayhem – Game Manual 1.” Version 1.1, Apr. 2024. Accessed: Sep. 2024. [Online]. Available: https://docs.google.com/document/d/1hTvIeRj649eyGU8oWLR_yD-mYgayySX7tRQBbetUCqc/edit 
2.	“Mining Mayhem – Game Manual 2” Version 1.1.3, Aug. 2024. Accessed: Sep. 2024. [Online]. Available: https://docs.google.com/document/d/1fN7bsJFpCJur66JkueRHXtlybt0m7QSY4Nn62lHAnrc/edit 
3.	Safety of machinery - Electrical equipment of machines. 2016. Accessed: Sep. 2024. [Online]. Available: https://webstore.iec.ch/en/publication/26037
4.	C. Woodford. "Speedometers." explainthatstuff.com. Mar. 2023. Accessed: Oct. 2024. [Online]. Available: https://www.explainthatstuff.com/how-speedometer-works.html
5.	K. Nice. "How Odometers Work." howstuffworks.com. Jan. 2001. Accessed: Oct. 2024. [Online]. Available: https://auto.howstuffworks.com/car-driving-safety/safety-regulatory-devices/odometer.htm#pt2
6.	yida. "What is a Time of Flight Sensor and How does a ToF Sensor work?" seeedstudio.com. 2019. Accessed: Oct. 2024. [Online]. Available: https://www.seeedstudio.com/blog/2020/01/08/what-is-a-time-of-flight-sensor-and-how-does-a-tof-sensor-work/
7.	gunengyu. "Grove - Ultrasonic Ranger." seeedstudio.com. Mar. 2023. Accessed: Oct. 2024. [Online]. Available: https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
8.	Ralph. "What’s the Difference Between an Accelerometer, Gyroscope and IMU Sensors?" intorobotics.com. Sep. 2023. Accessed: Oct. 2024. [Online]. Available: https://intorobotics.com/accelerometer-gyroscope-and-imu-sensors-in-robotics/#3_List_of_IMU_Sensors
9.	"Optical Mouse Sensors." digikey.com. May 2007. Accessed: Oct. 2024. [Online]. Avilable: https://media.digikey.com/pdf/Data%20Sheets/Avago%20PDFs/ToolKitSelectionGuide.pdf
10.	"GL125 Series Photoresistor." knowing-tech.com. Accessed: Oct. 2024. [Online]. Avilable: https://knowing-tech.com/wp-content/uploads/data/g/GL12528.pdf
11.	"LINEAR HALL-EFFECT IC." digikey.com. Rev.1.3, Aug. 2010. Accessed: Oct. 2024. [Online]. Avilable: https://www.digikey.com/htmldatasheets/production/1364519/0/0/1/ah49e.html?utm_adgroup=General&utm_source=bing&utm_medium=cpc&utm_campaign=Dynamic%20Search_EN_RLSA&utm_term=digikey&utm_content=General&utm_id=bi_cmp-384476624_adg-1302921504343623_ad-81432643449113_dat-2333232393680005:aud-807631099:loc-190_dev-c_ext-_prd-&msclkid=ef9edc5046c81a3f6ce4bb4050601364
12. Nvidia Jetson Nano vs Raspberry Pi - Which one is better for your project? May 2024. Accessed: Oct. 2024.[Online].Available: https://www.socketxp.com/iot/nvidia-jetson-nano-vs-raspberry-pi-which-one-is-better-for-your-project/
13. Comparing Dijkstra’s and A* Search Algorithm. May 2022. Accessed: Oct. 2024. [Online]. Available: https://medium.com/@miguell.m/dijkstras-and-a-search-algorithm-2e67029d7749
14. A.I.: Informed Search Algorithms. Accessed: Oct. 2024 [Online]. Available: https://web.pdx.edu/~arhodes/ai6.pdf
15.  ESP32 cam Object Detection. Accessed: Oct. 2024. [Online]. Available: https://webstore.iec.ch/en/publication/26037https://eloquentarduino.com/posts/esp32-cam-object-detection
16. Another T3.5 Rover with a OpenMV Camera (Machine Vision). Aug. 2017. Accessed: Oct. 2024. [Online]. Available: https://forum.pjrc.com/index.php?threads/another-t3-5-rover-with-a-openmv-camera-machine-vision.45741/
17.	“Motor Driver Fundamentals: Your Guide To Efficient Motor Control - Jhdpcb,” jhdpcb, Jan. 18, 2024. https://jhdpcb.com/blog/efficient-motor-control/#:~:text=The%20key%20role%20of%20the,enable%20speed%20and%20torque%20control
18.	E. P. Company, “Motor Encoders: What is a Motor Encoder? How Do Motor Encoders Work?,” www.encoder.com. https://www.encoder.com/motor-encoders#:~:text=What%20are%20motor%20encoders%3F,are%20either%20incremental%20or%20absolute
19.	Instructables, “Complete Motor Guide for Robotics,” Instructables, Dec. 13, 2015. https://www.instructables.com/Complete-Motor-Guide-for-Robotics/
20.	LastMinuteEngineers, “In-Depth: Interface L298N DC Motor Driver Module with Arduino,” Last Minute Engineers, Nov. 28, 2018. https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/
21.	“Pololu - DRV8835 Dual Motor Driver Carrier,” www.pololu.com. https://www.pololu.com/product/2135
22.	“Progeny.co.uk,” Progeny Access Control, 2015. https://progeny.co.uk/back-emf-suppression/#:~:text=The%20diode%20does%20a%20very,a%20one%20volt%20or%20so
23.	“Differences Between Optical and Magnetic Incremental Encoders Mekre Mesganaw & Isaac Lara Position Sensing.” Accessed: Oct. 19, 2024. [Online]. Available: https://www.ti.com/lit/ab/slya061/slya061.pdf?ts=1729347629954&ref_url=https%253A%252F%252Fwww.google.com%252F
24.	"Intel RealSense Product Family D400 Series." intelrealsense.com. Rev. 012, Mar. 2020. Accessed: Oct. 2024. [Online]. Available: https://www.intelrealsense.com/wp-content/uploads/2022/03/Intel-RealSense-D400-Series-Datasheet-March-2022.pdf
25.	"QTR-8A and QTR-8RC Reflectance Sensor Array User's Guide." pololu.com. Accessed: Oct. 2024. [Online]. Available: https://www.pololu.com/docs/pdf/0J12/QTR-8x.pdf
26.	I. Wu, “Power Supplies for Jetson Nano Developer Kit: The Definitive Guide,” Piveral, Jun. 07, 2021. https://piveral.com/jetson-nano-power-supply-guide/ (accessed Oct. 26, 2024).
‌
