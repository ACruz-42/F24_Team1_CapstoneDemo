#ifndef CONST_DECLARATIONS_H
#define CONST_DECLARATIONS_H

#include <Arduino.h>
#include <Servo.h>
#include <ezButton.h>
// Global variable declarations for any and all constant values

extern Servo gscLeanerServo, nscLeanerServo, SortServo, beaconArmServo, beaconGripperServo;

extern ezButton limG, limN, limS;

extern float voltageAugerSensor, currentAugerSensor, voltageSweeperSensor, currentSweeperSensor;
extern float movingAverageAmbient1, movingAverageAmbient2, movingAverageDetecting,
      ambientSensorVoltage1, ambientSensorVoltage2, startLEDSensorVoltage;

// Define sensor pins - DOUBLE CHECK - checked
const int sweeperCurrentPin = A0;
const int augerCurrentPin = A1;
const int gscPressurePin = A2;
const int nscPressurePin = A3;
const int gscLimitSwitchPin = 2;
const int nscLimitSwitchPin = 3;
const int ambientPhotoSensorPin1 = A11;
const int ambientPhotoSensorPin2 = A12;
const int detectingPhotoSensorPin = A7;
const int hallEffectPinX = A13;
const int hallEffectPinY = A14;
const int hallEffectPinZ = A15;
const int beamBreak = 47;

const long interval = 8000;
const long intervalSG = 2000;

// A1 to auger
// A0 to roller
// 47 for beambreak
// Photoresistors: A7, A11, A12
// Start Photoresistor: A7
// Ambient Photoresistors: A11, A12
// Hall Effect Sensors: A13, A14, A15

/*
// Define pins for pressure sensors and current sensor
const int presG = A2;
const int presN = A3;

const int currentSGPin = A1; // Sensor signal wire. This is the auger sensor.
const int currentSNPin = A0; // Sensor signal wire. This is the sweeper sensor.
*/

const float sensorOffset = 2.57; // Zero current output (2.5V for ACS712)
const float sensitivity = 0.185;  // 100mV per A for 20A ACS712

const int presThreshold = 100;  // not currently used as the nano is processing theshold

// Motor Pins
const int leftDriveENPin = 26;
const int leftDriveDir1Pin = 10;
const int leftDriveDir2Pin = 11;
const int leftDrivePWMPin = 9;
const int leftDriveEncAPin = 20;
const int leftDriveEncBPin = 21;

const int rightDriveENPin = 27;
const int rightDriveDir1Pin = 12;
const int rightDriveDir2Pin = 13;
const int rightDrivePWMPin = 3;
const int rightDriveEncAPin = 18;
const int rightDriveEncBPin = 19;

// CSC Servo pins 
const int GSCServoPin = 44;
const int NSCServoPin = 40; 
const int SortServoPin = 45;

// I don't think these are needed
//const int sensorPin = A0; // Photoresistor
//const int threshold = 500; // division for magnetic representation

// Beacon Servo pins
const int beaconArmPin = 33;
const int beaconGripperPin = 43;
const int initialAngleGSC = 135; //125
const int desiredAngleGSC = 110;
const int initialAngleNSC = 135; //140  // this is actually pickup angle.
const int desiredAngleNSC = 155;    // this is actually initial angle. // go back here after pick up
const int initialAngleSortServo = 0;          // THIS VALUE ISN'T CORRECT****************************************
const int desiredAngleSortServo = 0;          // THIS VALUE ISN'T CORRECT****************************************
const int initialAngleBeaconArm = 0; //105
const int desiredAngleBeaconArm = 55; //170
const int initialAngleBeaconGripper = 90;
const int desiredAngleBeaconGripper = 35;  







// Actuator motor driver pins
const byte gscGripperPWMPin = 4, gscGripperDirPin1 = 36, gscGripperDirPin2 = 37; // PUT IN PIN 4 (PWM) - left/GSC motor
const byte nscGripperPWMPin = 5, nscGripperDirPin1 = 23, nscGripperDirPin2 = 22; // PUT IN PIN 5 (PWM) - right/NSC motor

// Auger driver pins
const byte augerPWMPin = 6, augerDirPin1 = 34, augerDirPin2 = 30;

// Sweeper, Sweeper Arm driver pins
const byte sweeperPWMPin = 7, sweeperDirPin1 = 53, sweeperDirPin2 = 52;
//const byte sweepArmPWMPin = 8, sweepArmDirPin1 = 48, sweepArmDirPin2 = 49;

/*

******* L298N Pin Locations for Above Arduino Pins *******

// Actuator motor driver pins
const byte actM1PWMPin = 4 to top_left_ENA, actM1DirPin1 = 36 to top_left_IN1, actM1DirPin2 = 37 to top_left_IN2; // left/GSC motor
const byte actM2PWMPin = 5 to bottom_ENB, actM2DirPin1 = 23 to bottom_IN3, actM2DirPin2 = 22 to bottom_IN4; // right/NSC motor

// Auger driver pins
const byte augerPWMPin = 6 to top_left_ENB, augerDirPin1 = 34 to top_left_IN3, augerDirPin2 = 30 to top_left_IN4;

// Sweeper, Sweeper Arm driver pins
const byte sweepPWMPin = 7 to bottom_ENA, sweepDirPin1 = 53 to bottom_IN1, sweepDirPin2 = 52 to bottom_IN2;
const byte sweepArmPWMPin = 8 to top_right_ENB, sweepArmDirPin1 = 48 top_right_IN3, sweepArmDirPin2 = 49 top_right_IN4;

*/


#endif
