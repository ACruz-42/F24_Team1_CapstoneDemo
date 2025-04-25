## Overview

This folder contains the final Jetson Nano code presented at the SECON 2025 Hardware Competition. The Jetson Nano code was redesigned to work as a leader or controller to the Arduino follower or responder code. The Jetson Nano had all of the control and autonomous software. The Arduino had low level interface with motors for PWM signals and for reading in most sensor data.

This folder also contains one other program that was used to test the OTOS. qwiic_otos_ex1_basic_readings.py is a copy of the example provided by Sparkfun for testing the OTOS with a python controller, such as the Jetson Nano. It has been slightly modified to only record the last data point after a set timer ends. It is not used for running the robot.

The following link goes to the Arduino Follower Software readme. This provides information on how the data is sent back and forth and how the arduino controls the lower level logic: https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/c923fd8bf496c972fe1331faf40be674d2dc7530/Software/Arduino_Follower_Software/README.md


## Dependencies

smbus2, other otos, camera, python3.11.smth
