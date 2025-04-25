#ifndef SORTER_H
#define SORTER_H

#include <Arduino.h>
#include <Servo.h>
//#include <const_declarations.h>

// State definitions
#define WAIT_FOR_PRESENCE 0
#define UPDATE_GATE 10
#define WAIT_FOR_ABSENCE 20

// Function Prototypes

/**
 * Main sorter state machine function.
 * This function should be called continuously in the main loop.
 */
void sorter();

/**
 * Reads the hall effect sensor and returns the material type.
 * @return 1 if the sensor reading is above the threshold (magnetic material), 0 otherwise.
 */
int readHallEffectSensorX();

/**
 * Reads the hall effect sensor and returns the material type.
 * @return 1 if the sensor reading is above the threshold (magnetic material), 0 otherwise.
 */
int readHallEffectSensorY();

/**
 * Reads the hall effect sensor and returns the material type.
 * @return 1 if the sensor reading is above the threshold (magnetic material), 0 otherwise.
 */
int readHallEffectSensorZ();

/**
 * Reads the IR presence sensor.
 * @return 1 if the sensor reading is above the threshold (object present), 0 otherwise.
 */
int readIRSensor();

/**
 * Writes the sorter gate position.
 * @param dir: 0 = Mid position, -1 = Geodenium position, 1 = Nebulite position.
 */
void writeSorterGate(int dir);

/**
 * Retrieves the hall sensor value from a specific time in the past.
 * @param targetTime The target timestamp (in milliseconds) for the lookup.
 * @return The hall sensor reading (1 or 0) closest to the target time.
 */
int getHallSensorValueAtTime(unsigned long targetTime);

// External declaration for the servo object controlling the sorter gate.
// (Assume that sorterServo is defined and initialized in your source file.)
extern Servo sorterServo;

#endif // SORTER_H
