#include "sorter.h"
#include "const_declarations.h"
#include "arduino_to_nano.h"

// Define state constants for readability
#define WAIT_FOR_PRESENCE 0
#define UPDATE_GATE 10
#define WAIT_FOR_ABSENCE 20

int state = WAIT_FOR_PRESENCE;
unsigned long startTime = 0;

// Adjustable history buffer parameters
/*const int HISTORY_SIZE = 20;  // Number of hall sensor samples to store (adjust as needed)
int hallHistory[HISTORY_SIZE] = {0};
unsigned long hallTimestamps[HISTORY_SIZE] = {0};
int historyIndex = 0;*/

// Time offset (in milliseconds) to look back for the hall sensor reading.
// For example, if you want the reading from 50 ms in the past, set this to 50.
const unsigned long DESIRED_OFFSET_MS = 1500;   // will probably need to be longer. Maybe 200-300ms. will test sometime

// Replace these with your actual pin numbers and threshold values.
const int HALL_SENSOR_PINX = hallEffectPinX;
const int HALL_SENSOR_PINY = hallEffectPinY;
const int HALL_SENSOR_PINZ = hallEffectPinZ;
const int IR_SENSOR_PIN = beamBreak;
const int HALL_SENSOR_THRESHOLDX = 20; //128;
const int HALL_SENSOR_THRESHOLDY = 20;
const int HALL_SENSOR_THRESHOLDZ = 20; 
const int HALL_SENSOR_EXPECTEDX = 608; 
const int HALL_SENSOR_EXPECTEDY = 627; 
const int HALL_SENSOR_EXPECTEDZ = 644; 
const int IR_SENSOR_THRESHOLD = 575; 

bool timerFlag = false;
int materialIsMagnetic = 1;
bool pPresence = false;
int setTime = 0;

void sorter() {
  int presence = readIRSensor();
  //int sensorValueX = readHallEffectSensorX();
  int sensorValueY = readHallEffectSensorY();
  int sensorValueZ = readHallEffectSensorZ();

  //Serial.print("x:");
  //Serial.println(sensorValueX);
  // Serial.print("y:");
  // Serial.println(sensorValueY);
  // Serial.print("z:");
  // Serial.println(sensorValueZ);

  if(sensorValueY == 1 || sensorValueZ == 1){
    //Serial.println("ifstatement");
    materialIsMagnetic = -1;
    setTime = millis();
  }

  if((materialIsMagnetic == -1) && (millis() - setTime > 1000)){
    materialIsMagnetic = 1;
  }
  
  writeSorterGate(materialIsMagnetic);
}
  // Update the hall sensor history with the latest reading and timestamp.
  //hallHistory[historyIndex] = readHallEffectSensor();
  //hallTimestamps[historyIndex] = millis();
  //historyIndex = (historyIndex + 1) % HISTORY_SIZE;
  // Serial.print("state:");
  // Serial.println(state);
  // if(state == WAIT_FOR_PRESENCE) {
  //   // Check the presence sensor (IR sensor)
  //   int presence = readIRSensor();
  //   if (presence == 1) {
  //     if(materialIsMagnetic)
  //     timeFlag == false;
  //     startTime = millis();
  //     state = UPDATE_GATE;
  //   }
  // }
  // else if(state == UPDATE_GATE) {
  //   // Calculate the target time for the hall sensor reading.
  //   unsigned long targetTime = millis() + DESIRED_OFFSET_MS;
  //   // Retrieve the hall sensor value closest to the target time.
  //   int sensorValueX = readHallEffectSensorX();
  //   int sensorValueY = readHallEffectSensorY();
  //   int sensorValueZ = readHallEffectSensorZ();
    
  //   Serial.print("x:");
  //   Serial.println(sensorValueX);
  //   Serial.print("y:");
  //   Serial.println(sensorValueY);
  //   Serial.print("z:");
  //   Serial.println(sensorValueZ);


  //   // Set gate based on the retrieved hall sensor value.
  //   if(sensorValueY == 1 || sensorValueZ == 1) {
  //     if (targetTime >= millis()) {
  //       writeSorterGate(-1);   // Geodenium position
  //     } 
  //   } else {
  //     if (targetTime >= millis()) {
  //       writeSorterGate(1);  // Nebulite position
  //     } 
  //   }
    
  //   state = WAIT_FOR_ABSENCE;
  // }
  // else if(state == WAIT_FOR_ABSENCE) {
  //   unsigned long timeSinceStart = millis() - startTime;
  //   int presence = readIRSensor();
  //   if((presence == 0) || (timeSinceStart > 200)) {// change later
  //     state = WAIT_FOR_PRESENCE;
  //   }
  // }

// Searches the history buffer to find the hall sensor reading closest to (or just before)
// the desired target time.
/*int getHallSensorValueAtTime(unsigned long targetTime) {
  int bestIndex = -1;
  unsigned long bestDiff = 0xFFFFFFFF;  // initialize to a large number
  
  for (int i = 0; i < HISTORY_SIZE; i++) {
    // Compute absolute difference between stored timestamp and target time.
    unsigned long diff = (hallTimestamps[i] > targetTime) 
                         ? (hallTimestamps[i] - targetTime)
                         : (targetTime - hallTimestamps[i]);
    
    if(diff < bestDiff) {
      bestDiff = diff;
      bestIndex = i;
    }
  }
  
  if(bestIndex != -1) {
    return hallHistory[bestIndex];
  }
  
  // Fallback in case no valid sample is found
  return 0;
}*/

int readHallEffectSensorX() {
  // Serial.print("0:");
  // Serial.println(0);

  analogRead(HALL_SENSOR_PINX);
  int sensorValue = analogRead(HALL_SENSOR_PINX);
  int sampleAverageCount = 10;   // Set for now. Update as needed.

  //analogRead(HALL_SENSOR_PINX);   // used to switch adc to specific pinNumber

  float movingAverageX = movingAverageX + ((analogRead(HALL_SENSOR_PINX) - movingAverageX) / sampleAverageCount);

  // Serial.print("sensorValueX:");
  // Serial.println(sensorValue);
  return (abs(movingAverageX-HALL_SENSOR_EXPECTEDX) > HALL_SENSOR_THRESHOLDX) ? 1 : 0; // 570 is average of min and max for x
}

int readHallEffectSensorY() {
  analogRead(HALL_SENSOR_PINY);
  int sensorValue = analogRead(HALL_SENSOR_PINY);
  int sampleAverageCount = 10;   // Set for now. Update as needed.

  //analogRead(HALL_SENSOR_PINY);   // used to switch adc to specific pinNumber

  float movingAverageY = movingAverageY + ((analogRead(HALL_SENSOR_PINY) - movingAverageY) / sampleAverageCount);
  // Serial.print("sensorValueY:");
  // Serial.println(sensorValue);
  return (abs(movingAverageY-HALL_SENSOR_EXPECTEDY) > HALL_SENSOR_THRESHOLDY) ? 1 : 0; // 579 is average of min and max for y
}

int readHallEffectSensorZ() {
  analogRead(HALL_SENSOR_PINZ);
  int sensorValue = analogRead(HALL_SENSOR_PINZ);
  int sampleAverageCount = 10;   // Set for now. Update as needed.

  //analogRead(HALL_SENSOR_PINZ);   // used to switch adc to specific pinNumber

  float movingAverageZ = movingAverageZ + ((analogRead(HALL_SENSOR_PINZ) - movingAverageZ) / sampleAverageCount);
  //  Serial.print("sensorValueZ:");
  //  Serial.println(sensorValue);
  return (abs(movingAverageZ-HALL_SENSOR_EXPECTEDZ) > HALL_SENSOR_THRESHOLDZ) ? 1 : 0; // 625 is average of min and max for z
}

int readIRSensor() {
  int sensorValue = analogRead(IR_SENSOR_PIN);
  return (sensorValue > IR_SENSOR_THRESHOLD) ? 1 : 0;
}

void writeSorterGate(int dir) {
  // Servo sorterServo; // Assuming sorterServo is declared and initialized elsewhere
  //Serial.print("dir");
  //Serial.println(dir);
  SortServo.write(135);
  // if (dir == 0) {
  //   //SortServo.write(45);
  // }
  // else if (dir == -1) {
  //   SortServo.write(45);
  // }
  // else if (dir == 1) {
  //   SortServo.write(135);
  // }
}
