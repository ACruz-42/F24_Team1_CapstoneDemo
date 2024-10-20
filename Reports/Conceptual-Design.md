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

### Motor Control
The motor control subsystem functions as the feedback-based reaction center for the robot’s processes. It uses the input taken in from sensory data, such as object and line detection or map navigation, and follows the commands given to it from the master control to perform the physical responses of the robot. The primary method that will be used for feedback response is PID control. 

The motor control subsystem is formally known as a motor drive and can include the following components: a microcontroller (MC), motor driver, motor, power supply, and specific components for noise reduction and circuit protection [17]. The motor microcontroller carries the digital signal commands from the master controller for the designated motor to operate as required. However, the power that the MC needs to function is not enough in comparison to what the motor needs. Therefore, it is essential to have a component that can step up the power from the MC to the motor. This is the purpose of the motor driver. The motor microcontroller sends a digital signal to the driver using PWM to set the desired motor speed. The driver can provide voltage regulation for the higher threshold of the motor, precision control for speed and torque, overload protection, and noise protection for the circuits involving low-power logic control [17]. The driver and motor terminals have a pair of wires that when connected, control the speed and direction of the motors. Encoders that detect the motor shaft speed/position to provide the actual speed of the motors are useful for completing a closed loop feedback system, such as with PID control [18]. All logic control circuitry, which includes the master control, motor microcontroller, and encoders, will receive low voltage from the power subsystem, while the motor driver will receive high voltage in order to provide the high power needs of the motors.


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

### Master Control and Navigation
#### Atomic Subsystem Specifications
#### Comparative Analysis of Potential Solutions
#### Ethical, Professional, and Standards Considerations
#### Resources
#### Budget
#### Skills

### Motor Control
#### Atomic Subsystem Specifications
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

#### Ethical, Professional, and Standards Considerations

The project will have an impact on the outreach of Tennessee Tech, with the team representing the school in this competition both technically and professionally. If the team can perform well, it will build on the image of the College of Engineering for prospective students, encouraging them to attend the university and be engaged in similar endeavors in the future. In preparing for the competition, the team will follow the IEEE Code of Ethics for respectful collaboration and safe design practice. To maintain a healthy relationship among team members while also holding each other accountable, each member completes evaluations for themselves and for the others on the team, providing opportunity for self-reflection of progress and for checking in on the progress of others. 

The robot movement will need to comply with Game Manual specifications. There are specific rules in place for the safety of the team and the referees/technicians at the competition. Specification 10 details the need for the robot to cease operation of all units after the given 3 minutes of play. Therefore, the motor control programming and mechanisms will need to have measures in place to quickly and safely halt the robot and any actions it is performing toward the end of the time of play. 

#### Resources

The following items are necessary for the completion of the motor control subsystem. In order for the motors to respond to environmental and robot feedback, a central motor microcontroller must be present to be able to properly distribute the large quantity of connections required for the robot to move and collect/sort astral material. In the current configuration, the robot will only need two driving brushed motors for translation along the ground, implementing the use of ball bearing wheels on the back for stability. However, these motors need a voltage regulator for speed and direction, which requires the use of two motor drivers, such as the L298N H-bridge module. In order to adjust motor commands based on the current state of the motors, the robot must collect positional data of the motor shafts, which employs the use of encoders, with optical encoders being a safe choice in comparison to magnetic encoders, which may disturb the low-level logic circuitry due to the magnetic properties. 

#### Budget

|Item|Cost per Item|Quantity|Total Cost for Item|
| :- | :- | :- | :- |
|Brushed Motors (24V)|~$60.00|2|$120.00|
|Motor Microcontroller|~$30.00|1|$30.00|
|Motor Drivers (L298N H-bridge module)|$10.00|2|$20.00|
|Optical Encoders|$20.00|2|$40.00|
|Total|||$210.00|

#### Skills

For the Motor Control subsystem, there is mainly hardware implementation, but software is required for PID control. A team member with theoretical knowledge of PID feedback loops and technical experience in programming would be well-suited for this role. Classes in Controls and Robotics would help serve as a sufficient background for the project applications. 

### Power Management
#### Atomic Subsystem Specifications

There are several quantifiable specifications and constraints for the power subsystem given the competition rules and the adherence to safe engineering practice. Procedurally, the main areas of focus are the start and stop mechanisms during play. In accordance with Specification 2-ii and 6, the robot functionality may have a trigger based on a given Start LED controlled by the referee or through a clearly labeled electrical start button. For the manual start button, the robot shall not move for five seconds after activation, but onboard commands can run during this time in preparation for play. The robot shall be able to safely and efficiently pause all its functions using a clearly labeled emergency stop button according to Specification 7. If there are multiple independently acting ‘Robot Units’, each shall have their own emergency stop button. Regarding power system requirements, the robot shall not go beyond 30V, as given by Specification 12. It shall also implement proper circuit shielding and isolation based on the disturbances from background interference in the competition environment, as given by Specification 11. Constraint 3 deals with International Electrotechnical Commision regulations for power supply, emergency stop, and circuit protection requirements. From this standard, the circuitry of the robot shall account for and add appropriate devices to promote safety measures such as overcurrent, overload, and over-temperature protection [3]. The power subsystem of this robot will be the electrical backbone of the project. Without a structured model of power management and distribution, the robot would not be able to meet all functions, specifications and constraints. For this subsystem to work correctly with the scope of the project, we must install a battery/(ies) so that the robot can be powered without a cord attached to a wall socket.

#### Comparative Analysis of Potential Solutions

This power subsystem requires adequate power management and distribution of all hardware within the robot. Since we must power both the microcontroller and the motor subsystems, it would be wise to separate the power buses at a certain point so that neither subsystems connected to the power subsystem will interfere with each other, but work together towards a common goal. Based on last year’s SECON Modular-Based Robot, creating a power distribution circuit that isolates 2 batteries to power both subsystems we believe will be most optimal. For Specification 6 and 2-ii, the start button mentioned within the sensor section will be connected to the power subsystem. Once pressed, it will have both batteries provide sufficient voltage and current to both the motor and microcontroller, but will not start moving until 5 seconds after the button or LED receiver  is triggered. Similarly, Specification 7 refers to an Emergency Stop button that is required within the Game Rules. This E-Stop button will also be connected to the circuit. Once pressed, the circuit shall open the power bus to the motor while the bus to the microcontrollers will stay closed. Thus, giving the microcontroller power to process still, and cutting off all power to the motor for optimal safety while also saving critical data.

#### Ethical, Professional, and Standards Considerations

The Game Manual provided structures for the competition to follow IEEE guidelines and general electrical standards. Resources mentioned such as datasheets and procedures correlated with clean power transmission will be followed closely. For example, the E-stop mentioned in the rules are for the safety of the competitors, judges, and audience in the case of a motor malfunction.

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

## Timeline
## Statement of Contributions
  - Sean Borchers - Motor Control Subsystem Information (Excluding Main Specifications)
  - Alex Cruz -
  - Sam Hunter -
  - Alejandro Moore - Power Management Subsystem Information
  - Dakota Moye - 

## Works Cited
1.	“Mining Mayhem – Game Manual 1.” Version 1.1, Apr. 2024. Accessed: Sep. 2024. [Online]. Available: https://docs.google.com/document/d/1hTvIeRj649eyGU8oWLR_yD-mYgayySX7tRQBbetUCqc/edit 
2.	“Mining Mayhem – Game Manual 2” Version 1.1.3, Aug. 2024. Accessed: Sep. 2024. [Online]. Available: https://docs.google.com/document/d/1fN7bsJFpCJur66JkueRHXtlybt0m7QSY4Nn62lHAnrc/edit 
1.	Safety of machinery - Electrical equipment of machines. 2016. Accessed: Sep. 2024. [Online]. Available: https://webstore.iec.ch/en/publication/26037
2.	C. Woodford. "Speedometers." explainthatstuff.com. Mar. 2023. Accessed: Oct. 2024. [Online]. Available: https://www.explainthatstuff.com/how-speedometer-works.html
3.	K. Nice. "How Odometers Work." howstuffworks.com. Jan. 2001. Accessed: Oct. 2024. [Online]. Available: https://auto.howstuffworks.com/car-driving-safety/safety-regulatory-devices/odometer.htm#pt2
4.	yida. "What is a Time of Flight Sensor and How does a ToF Sensor work?" seeedstudio.com. 2019. Accessed: Oct. 2024. [Online]. Available: https://www.seeedstudio.com/blog/2020/01/08/what-is-a-time-of-flight-sensor-and-how-does-a-tof-sensor-work/
5.	gunengyu. "Grove - Ultrasonic Ranger." seeedstudio.com. Mar. 2023. Accessed: Oct. 2024. [Online]. Available: https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
6.	Ralph. "What’s the Difference Between an Accelerometer, Gyroscope and IMU Sensors?" intorobotics.com. Sep. 2023. Accessed: Oct. 2024. [Online]. Available: https://intorobotics.com/accelerometer-gyroscope-and-imu-sensors-in-robotics/#3_List_of_IMU_Sensors
7.	"Optical Mouse Sensors." digikey.com. May 2007. Accessed: Oct. 2024. [Online]. Avilable: https://media.digikey.com/pdf/Data%20Sheets/Avago%20PDFs/ToolKitSelectionGuide.pdf
8.	"GL125 Series Photoresistor." knowing-tech.com. Accessed: Oct. 2024. [Online]. Avilable: https://knowing-tech.com/wp-content/uploads/data/g/GL12528.pdf
9.	"LINEAR HALL-EFFECT IC." digikey.com. Rev.1.3, Aug. 2010. Accessed: Oct. 2024. [Online]. Avilable: https://www.digikey.com/htmldatasheets/production/1364519/0/0/1/ah49e.html?utm_adgroup=General&utm_source=bing&utm_medium=cpc&utm_campaign=Dynamic%20Search_EN_RLSA&utm_term=digikey&utm_content=General&utm_id=bi_cmp-384476624_adg-1302921504343623_ad-81432643449113_dat-2333232393680005:aud-807631099:loc-190_dev-c_ext-_prd-&msclkid=ef9edc5046c81a3f6ce4bb4050601364





17.	“Motor Driver Fundamentals: Your Guide To Efficient Motor Control - Jhdpcb,” jhdpcb, Jan. 18, 2024. https://jhdpcb.com/blog/efficient-motor-control/#:~:text=The%20key%20role%20of%20the,enable%20speed%20and%20torque%20control
18.	E. P. Company, “Motor Encoders: What is a Motor Encoder? How Do Motor Encoders Work?,” www.encoder.com. https://www.encoder.com/motor-encoders#:~:text=What%20are%20motor%20encoders%3F,are%20either%20incremental%20or%20absolute
19.	Instructables, “Complete Motor Guide for Robotics,” Instructables, Dec. 13, 2015. https://www.instructables.com/Complete-Motor-Guide-for-Robotics/
20.	LastMinuteEngineers, “In-Depth: Interface L298N DC Motor Driver Module with Arduino,” Last Minute Engineers, Nov. 28, 2018. https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/
21.	“Pololu - DRV8835 Dual Motor Driver Carrier,” www.pololu.com. https://www.pololu.com/product/2135
22.	“Progeny.co.uk,” Progeny Access Control, 2015. https://progeny.co.uk/back-emf-suppression/#:~:text=The%20diode%20does%20a%20very,a%20one%20volt%20or%20so
23.	“Differences Between Optical and Magnetic Incremental Encoders Mekre Mesganaw & Isaac Lara Position Sensing.” Accessed: Oct. 19, 2024. [Online]. Available: https://www.ti.com/lit/ab/slya061/slya061.pdf?ts=1729347629954&ref_url=https%253A%252F%252Fwww.google.com%252F
