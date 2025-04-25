#ifndef NANO_TO_ARDUINO_H
#define NANO_TO_ARDUINO_H

#include "const_declarations.h"
// This file is for functions that are used to communicate data from the nano to the arduino.

void robotSpeedFunction(float leftWheelSpeed, float rightWheelSpeed);
void augerFunction(int auger);
void sweeperFunction(int sweeper);
void beaconArmFunction(int beaconArm);
void beaconGripperFunction(int beaconGripper);
void gscGripperFunction(int gscGripper);
void nscGripperFunction(int nscGripper);
void gscLeanerFunction(int gscLeaner);
void nscLeanerFunction(int nscLeaner);

#endif