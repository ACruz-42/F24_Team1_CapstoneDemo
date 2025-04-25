## Overview

This folder contains the final Arduino code presented at the SECON 2025 Hardware Competition. The Arduino code was redesigned to work as a follower or responder to the Jetson Nano leader or controller code. The Jetson Nano had all of the control and autonomous software. The Arduino had low level interface with motors for PWM signals and for reading in most sensor data.

## Dependencies
1. TimerOne by Stoyko Dimitrov, Jesse Tane, Jérôme Despatis, Michael Polli, Dan Clemens, Paul Stoffregen
2. ezButton by ArduinoGetStarted.com
3. Servo by Michael Margolis, Arduino

Dependencies 1 and 2 have to be installed. Dependency 3 came preinstalled in the Arduino IDE. The first two were installed through the Arduino IDE library search function.

## Use
### Input
The Arduino Follower Software takes in a set of inputs. These are supposed to come from the Jetson Nano code, but it can be manually input. The format is a packet or string of 10 ints in format "int,int,int,int,int,int,int,int,int,int" without the quotation marks. The first two need 201 options for data type. The rest need 3 options, which means 2 bits would work. In the center column of the following table is the allowed inputs. 

One example is "50,-20,1,1,0,0,1,-1,0,1". This sets left wheel speed to forward 50%, right wheel speed backward 20%, auger forward, sweeper forward, does nothing to beacon arm, does nothing to beacon gripper, opens GSC gripper, closes NSC gripper, does nothing for GSC leaner, and moves NSC leaner to pickup angle. If one of the components is already in a specific state, it will stay in that state until sent a different one. This means everything will keep moving until told to stop. For the servo control, they will keep their angle until told to change, and then will keep that angle. The table below lists the inputs in order of placement along the packet. The table shows input to be controlled, range of input control, and what happens for that range.

In the final edition of the code, the GSC arm was not used and is manually set to be 0 in the code.

|input type|input available|input action|
|:-|:-|:-|
|left wheel speed|-100 to 100|0 to 100% speed. Negative is backwards and positive is forwards.|
|right wheel speed|-100 to 100|0 to 100% speed. Negative is backwards and positive is forwards.|
|auger forward, backward, or off|1, 0, -1|1 is forward, or desired direction. 0 is stop. -1 is backward, or undesired direction.|
|sweeper direction and on or off|1, 0, -1|1 is forward, or desired direction. 0 is stop. -1 is backward, or undesired direction.|
|beacon arm preset location|1, 0, -1|1 moves beacon arm to holding angle and is initial angle, 0 is nothing, -1 moves beacon arm to placement angle|
|beacon gripper open or closed|1, 0, -1|1 closes beacon gripper and is initial state, 0 is nothing, -1 opens beacon gripper|
|Geodinum Shipping Container (GSC) Gripper open, close, or stop|1, 0, -1|1 opens GSC gripper, 0 stops, -1 closes GSC gripper|
|Nebulite Shipping Container (NSC) Gripper open, close, or stop|1, 0, -1|1 opens NSC gripper, 0 stops, -1 closes NSC gripper|
|GSC Leaner preset location|1, 0, -1|1 is pickup angle, 0 is nothing, -1 is storing angle|
|NSC Leaner preset location|1, 0, -1|1 is pickup angle, 0 is nothing, -1 is storing angle|

### Output
The Arduino Follower Software outputs a set data when it receives a command. These are supposed to be sent to the Jetson Nano, but it can print to any serial. The format is a packet or string of 7 variables in format "bit,bit,int,int,bit,bit,bit" without the quotation marks. In the center column of the following table is the available outputs.

In the final edition of the code, the current sensors were not used and are manually set to 0 in the code.

|output type|output available|output action|
|:-|:-|:-|
|current sensor for sweeper|1, 0|1 means the sweeper has stalled, 0 means it has not|
|current sensor for auger|1, 0|1 means the auger has stalled, 0 means it has not|
|GSC pressure sensor|0, 100|0 to 100% pressure. 100% pressure is max pressure sensor can handle.|
|NSC pressure sensor|0, 100|0 to 100% pressure. 100% pressure is max pressure sensor can handle.|
|GSC limit switch|1, 0|1 means limit switch, or button, is pressed, 0 means it is not pressed|
|NSC limit switch|1, 0|1 means limit switch, or button, is pressed, 0 means it is not pressed|
|light sensor|1, 0|1 means the start LED sensor sees more light than the ambient light sensor, 0 means the opposite|

## Hall Effects
In the last edition of the code, a sorter was made to process the hall effects and object sensor. The goal was to flip the servo for the sorter flap back and forth according to the hall effects and object sensor. This ended up not working due to the hall effects having some issues discussed in the Experimental Analysis. While still in the code, sorter.cpp and sorter.h currently does nothing important.
