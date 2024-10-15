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

GOAL FOR THIS SECTION: In this section, various potential solutions are hypothesized, design considerations are discussed, and factors influencing the selection of a solution are outlined. The chosen solution is then identified with justifications for its selection.

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
Accelerometers and gyroscopes come in small, single-chip package that are interfaceable with a microcontroller.
However, a tachometer would require two individual units to measure each of the motors or wheels.

##### Location Sensor

##### Start LED Sensor

##### Magnetic Sensor

#### Ethical, Professional, and Standards Considerations
#### Resources
#### Budget
#### Skills

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
2.	https://www.explainthatstuff.com/how-speedometer-works.html
3.	https://auto.howstuffworks.com/car-driving-safety/safety-regulatory-devices/odometer.htm#pt2

