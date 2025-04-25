#include <TimerOne.h>
#include "const_declarations.h"
#include "nano_to_arduino.h"
#include "arduino_to_nano.h"
#include "sorter.h"

unsigned long t;
unsigned long t_prev = 0;
unsigned long matchTime;
float length = 0;
bool expand = false;
bool extend = false;
bool retract = true;
bool serial = true;
bool translated = false;
bool rotated = false;
bool pressureDetected;
bool int_state = false;
unsigned long previousMillis;

// ********************* Start of Package System *********************
// Define a struct to hold input data received from the Nano
struct InputData {
  //
  float leftWheelSpeed; // -100..100
  float rightWheelSpeed; // -100..100
  int auger; // -1: negative direction, 0: no rotation, 1: positive direction
  int sweeper; // -1: negative direction, 0: no rotation, 1: positive direction
  int beaconArm; // -1: negative direction, 0: no rotation, 1: positive direction
  int beaconGripper; // -1: negative direction, 0: no rotation, 1: positive direction
  int gscGripper; // -1: negative direction, 0: no rotation, 1: positive direction
  int nscGripper; // -1: negative direction, 0: no rotation, 1: positive direction
  int gscLeaner; // -1: negative direction, 0: no rotation, 1: positive direction
  int nscLeaner; // -1: negative direction, 0: no rotation, 1: positive direction
};


// Example command received: 0,0,1,0,0,0,0,0,0,0

// Define a struct to hold output data to be sent to the Nano
struct OutputData {
  int sweeperCurrentSensor; // 0: not stalled, 1: stalled
  int augerCurrentSensor; // 0: not stalled, 1: stalled
  float gscPressureSensor; // 0..100 (full pressure)
  float nscPressureSensor; // 0..100 (full pressure)
  int gscLimitSwitch; // 0: not pressed, 1: pressed
  int nscLimitSwitch; // 0: not pressed, 1: pressed
  int photosensor; // 0: not detected, 1: detected
};

// Global variables for serial data reception
String inputString = "";
bool newData = false;

// Timer variables for sending output data every 100 ms
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 100;  // in milliseconds



// Function declarations
void readSerialData();
InputData parseInputData(const String &packet);
String buildOutputPacket(const OutputData &data);

void setup() {
  Serial.begin(115200);
  pinMode(gscLimitSwitchPin, INPUT);
  pinMode(nscLimitSwitchPin, INPUT);
  pinMode(ambientPhotoSensorPin1, INPUT);
  pinMode(ambientPhotoSensorPin2, INPUT);
  pinMode(detectingPhotoSensorPin, INPUT);
  pinMode(hallEffectPinX, INPUT);
  pinMode(hallEffectPinY, INPUT);
  pinMode(hallEffectPinZ, INPUT);
  

  // Set Actuator motor driver pins
  pinMode(gscGripperPWMPin, OUTPUT);
  pinMode(gscGripperDirPin1, OUTPUT);
  pinMode(gscGripperDirPin2, OUTPUT);
  pinMode(nscGripperPWMPin, OUTPUT);
  pinMode(nscGripperDirPin1, OUTPUT);
  pinMode(nscGripperDirPin2, OUTPUT);

  // Set sweeper and sweeper arm driver pins
  pinMode(sweeperPWMPin, OUTPUT);
  pinMode(sweeperDirPin1, OUTPUT);
  pinMode(sweeperDirPin2, OUTPUT);

  // Set Auger driver pins
  pinMode(augerPWMPin, OUTPUT);
  pinMode(augerDirPin1, OUTPUT);
  pinMode(augerDirPin2, OUTPUT);

  // Set Servo system pins
  gscLeanerServo.attach(GSCServoPin);
  nscLeanerServo.attach(NSCServoPin);
  pinMode(augerCurrentPin, INPUT);
  pinMode(sweeperCurrentPin, INPUT);
  limG.setDebounceTime(1); // set debounce time to 1 millisecond
  limN.setDebounceTime(1); // set debounce time to 1 millisecond
  limS.setDebounceTime(1); // set debounce time to 1 millisecond

  SortServo.attach(SortServoPin);
  SortServo.write(135); // 90 +-45
  gscLeanerServo.write(107);
  nscLeanerServo.write(desiredAngleNSC);

  pinMode(beamBreak, INPUT);













// CHECK THAT THESE ARE THE CORRECT SERVOS ********************************************************************



  // before
  /*
  BaseServo.attach(beaconBasePin);
  WristServo.attach(beaconWristPin);
  BaseServo.write(initialAngleBase);
  WristServo.write(initialAngleWrist); 
  */
  // after
  beaconGripperServo.attach(beaconGripperPin);
  beaconArmServo.attach(beaconArmPin);
  beaconGripperServo.write(initialAngleBeaconGripper);
  beaconArmServo.write(initialAngleBeaconArm); 

  matchTime = millis();  // Start tracking match time


  //Serial.println("Arduino integrated send & receive ready...");
}







// FINISH SORT, HALL EFFECT, AND OBJECT DETECTION







void loop() {
limG.loop(); // MUST call the loop() function first
limN.loop(); // MUST call the loop() function first

  // Continuously check for incoming data
  readSerialData();
  
  // When a complete input packet is received (terminated by '\n')
  if (newData) {
    
    lastSendTime = millis();
    InputData inputData = parseInputData(inputString);
    
    // Debug print for input data
    //Serial.println("Debug | Received input data at " + millis());
    /*Serial.print("debug -  Left wheel speed: ");
    Serial.println(inputData.leftWheelSpeed);
    Serial.print("debug -  Right wheel speed: ");
    Serial.println(inputData.rightWheelSpeed);
    Serial.print("debug -  Auger: ");
    Serial.println(inputData.auger);
    Serial.print("debug - Sweeper: ");
    Serial.println(inputData.sweeper);
    Serial.print("debug - Beacon Arm: ");
    Serial.println(inputData.beaconArm);
    Serial.print("debug - Beacon Gripper: ");
    Serial.println(inputData.beaconGripper);
    Serial.print("debug - GSC Gripper: ");
    Serial.println(inputData.gscGripper);
    Serial.print("debug - NSC Gripper: ");
    Serial.println(inputData.nscGripper);
    Serial.print("debug -  GSC Leaner: ");
    Serial.println(inputData.gscLeaner);
    Serial.print("debug - NSC Leaner: ");
    Serial.println(inputData.nscLeaner);
    Serial.println("-------------------------------------");*/

    // call all nano_to_arduino functions
    robotSpeedFunction(inputData.leftWheelSpeed, inputData.rightWheelSpeed);
    augerFunction(inputData.auger);
    sweeperFunction(inputData.sweeper);
    beaconArmFunction(inputData.beaconArm);
    beaconGripperFunction(inputData.beaconGripper);
    gscGripperFunction(0);
    nscGripperFunction(inputData.nscGripper);
    gscLeanerFunction(0);
    nscLeanerFunction(inputData.nscLeaner);
    
    // Reset for next input packet
    inputString = "";
    newData = false;


    
    
    // Simulate output data values; replace with your actual sensor readings
    OutputData outputData;
    //OutputData outputData;      // this was here twice for some reason. Should just be deleted but left it in case
    /*
    outputData.sweeperCurrentSensor = analogRea/*d(sweeperCurrentPin) > 500 ? 1 : 0;
    outputData.augerCurrentSensor = analogRead(augerCurrentPin) > 500 ? 1 : 0;
    outputData.gscPressureSensor = (analogRead(gscPressurePin) / 1023.0) * 100;
    outputData.nscPressureSensor = (analogRead(nscPressurePin) / 1023.0) * 100;
    outputData.gscLimitSwitch = digitalRead(gscLimitSwitchPin);
    outputData.nscLimitSwitch = digitalRead(nscLimitSwitchPin);
    outputData.photosensor = digitalRead(photoSensorPin);
    */

    // call all arduino_to_nano functions
    outputData.sweeperCurrentSensor = sweeperCurrentSensorFunction();
    outputData.augerCurrentSensor = augerCurrentSensorFunction();
    outputData.gscPressureSensor = gscPressureSensorFunction();
    outputData.nscPressureSensor = nscPressureSensorFunction();
    outputData.gscLimitSwitch = gscLimitSwitchFunction();
    outputData.nscLimitSwitch = nscLimitSwitchFunction();
    outputData.photosensor = photosensorFunction();
    

    // Build and send the output packet
    String packetToSend = buildOutputPacket(outputData);
    //Serial.println("Debug | Sent output data at " + String(millis()));
    Serial.println(packetToSend);
    //Serial.println(millis()-lastSendTime);
  }
  
  // Check if it's time to send output data (every 100 ms)
  //if (millis() - lastSendTime >= sendInterval) {
  //}
  sorter();
}











// Function definitions

// Reads available characters from Serial and flags when a newline is detected
void readSerialData() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    //Serial.write(c);
    if (c == '\n') {
      newData = true;
    } else {
      inputString += c;
    }
  }
}

// Parses a comma-separated string into an InputData struct
InputData parseInputData(const String &packet) {
  InputData data;
  int startIndex = 0;
  int commaIndex;
  
  // Helper lambda to extract the next field
  auto getNextField = [&]() -> String {
    commaIndex = packet.indexOf(',', startIndex);
    if (commaIndex == -1) {
      commaIndex = packet.length();
    }
    String field = packet.substring(startIndex, commaIndex);
    startIndex = commaIndex + 1;
    return field;
  };

  data.leftWheelSpeed  = getNextField().toFloat();
  data.rightWheelSpeed = getNextField().toFloat();
  data.auger           = getNextField().toInt();
  data.sweeper         = getNextField().toInt();
  data.beaconArm       = getNextField().toInt();
  data.beaconGripper   = getNextField().toInt();
  data.gscGripper      = getNextField().toInt();
  data.nscGripper      = getNextField().toInt();
  data.gscLeaner       = getNextField().toInt();
  data.nscLeaner       = getNextField().toInt();
  
  return data;
}

// Builds a comma-separated output packet from OutputData struct values
String buildOutputPacket(const OutputData &data) {
  String packet = "";
  packet += String(data.sweeperCurrentSensor)     + ",";
  packet += String(data.augerCurrentSensor)       + ",";
  packet += String(data.gscPressureSensor, 2)     + ",";
  packet += String(data.nscPressureSensor, 2)     + ",";
  packet += String(data.gscLimitSwitch)           + ",";
  packet += String(data.nscLimitSwitch)           + ",";
  packet += String(data.photosensor);
  return packet;
}
