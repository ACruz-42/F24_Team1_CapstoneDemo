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
1.	“Mining Mayhem – Game Manual 2” Version 1.1.3, Aug. 2024. Accessed: Sep. 2024. [Online]. Available: https://docs.google.com/document/d/1fN7bsJFpCJur66JkueRHXtlybt0m7QSY4Nn62lHAnrc/edit 
1.	Safety of machinery - Electrical equipment of machines. 2016. Accessed: Sep. 2024. [Online]. Available: https://webstore.iec.ch/en/publication/26037

