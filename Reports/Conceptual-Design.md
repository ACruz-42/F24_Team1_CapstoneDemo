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

The robot will need a camera with both RGB and dpeth sensing capabillites.
The camera has 2 cameras in it, 1 is a 2D camera which will be used like a normal 2D camera for video and RGB values.
The second camera is an infrared camera which uses an infrared laser detector which seperates objects into layers. 
The primary purpose of the camera will be to identify the astral material and then accurately place it on the game field for the navigation algorithm.
The camera will use the 2D RGB camera to find and differentiate the different objects, including astral material, game field walls, and cave walls.
It will then use the infrared camera to accurately place the objects in relation to the robot.[1]

#### Ethical, Professional, and Standards Considerations

The datasheet for the camera will be followed and the intended use matches closely with the designed use.
The infrared laser projector is safe for use in the vicinity of humans. 

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
  - Alex Cruz -
  - Sam Hunter -
  - Alejandro Moore -
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
24. 	“Intel ® RealSense TM Product Family D400 Series Datasheet Intel ® RealSenseTM Vision Processor D4, Intel,” 2022. Available: https://www.intelrealsense.com/wp-content/uploads/2022/03/Intel-RealSense-D400-Series-Datasheet-March-2022.pdf
‌

