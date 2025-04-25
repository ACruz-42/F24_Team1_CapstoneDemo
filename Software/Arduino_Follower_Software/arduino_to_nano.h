#ifndef ARDUINO_TO_NANO_H
#define ARDUINO_TO_NANO_H

#include "const_declarations.h"
// This file is for functions that are used to communicate data from the arduino to the nano.


int sweeperCurrentSensorFunction();
int augerCurrentSensorFunction();
float gscPressureSensorFunction();
float nscPressureSensorFunction();
int gscLimitSwitchFunction();
int nscLimitSwitchFunction();
int photosensorFunction();
float average_analogRead(int pinNumber, float &movingAverage);

#endif
