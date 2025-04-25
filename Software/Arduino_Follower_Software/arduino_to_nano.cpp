#include "arduino_to_nano.h"


// Function to read the sweeper current sensor and return stall status
int sweeperCurrentSensorFunction() {
   /* // Read the current sensor value (this is just an example)
    analogRead(sweeperCurrentPin);   // used to switch adc to specific pinNumber
    // no power 0.27V
    // 
    //
    voltageSweeperSensor = analogRead(sweeperCurrentPin) * (5.0 / 1023.0); // Convert ADC value to voltage
    //Serial.print("debug - ");
    //Serial.println(average_analogRead(sweeperCurrentPin, voltageSweeperSensor));
    average_analogRead(sweeperCurrentPin, voltageSweeperSensor);
    currentSweeperSensor = (voltageSweeperSensor - sensorOffset) / sensitivity; // Convert voltage to current
    //Serial.print("debug - analogRead(sweeperCurrentPin): ");
    //Serial.println(analogRead(sweeperCurrentPin));
    //Serial.print("debug - voltageSweeperSensor: ");
    //Serial.println(voltageSweeperSensor);
    //Serial.print("debug - currentSweeperSensor: ");
    //Serial.println(currentSweeperSensor);
    /*if(currentSweeperSensor > 0.35) {    // Threshold may need to be adjusted to 1A
        // Stalled
        return 1;
    } else {
        // Not stalled
        return 0;
    }*/
    return 0;
}


// Function to read the auger current sensor and return stall status
int augerCurrentSensorFunction() {
   /* //Serial.print("debug - ");
    //Serial.println(average_analogRead(augerCurrentPin, voltageAugerSensor));
    average_analogRead(augerCurrentPin, voltageAugerSensor);
    currentAugerSensor = (voltageAugerSensor - sensorOffset) / sensitivity; // Convert voltage to current
    //Serial.print("debug - analogRead(augerCurrentPin): ");
    //Serial.println(analogRead(augerCurrentPin));
    //Serial.print("debug - voltageAugerSensor: ");
    //Serial.println(voltageAugerSensor);
    //Serial.print("debug - currentAugerSensor: ");
    //Serial.println(currentAugerSensor);
    /*if(currentAugerSensor > 0.35) {    // Threshold may need to be adjusted to 1A
        // Stalled
        return 1;
    } else {
        // Not stalled
        return 0;
    }*/
    return 0;
}


// Function to read the GSC pressure sensor and return pressure value (0..100)
float gscPressureSensorFunction() {
    // Read the pressure sensor value (this is just an example)
    analogRead(gscPressurePin);   // used to switch adc to specific pinNumber
    float gscPressureSensor = analogRead(gscPressurePin);

    // Convert raw sensor value to a percentage (0-100)
    float pressure = map(gscPressureSensor, 0, 1023, 0, 100);
    
    return pressure;
}


// Function to read the NSC pressure sensor and return pressure value (0..100)
float nscPressureSensorFunction() {
    // Read the pressure sensor value (this is just an example)
    analogRead(nscPressurePin);   // used to switch adc to specific pinNumber
    float nscPressureSensor = analogRead(nscPressurePin);

    // Convert raw sensor value to a percentage (0-100)
    float pressure = map(nscPressureSensor, 0, 1023, 0, 100);

    return pressure;
}


// Function to read the GSC limit switch and return pressed status
int gscLimitSwitchFunction() {
    // Read the limit switch value
    int gscLimitSwitch = 1-limG.getStateRaw();    // If getStateRaw is 0 (low), the button is pressed

    // Return pressed (1) or not pressed (0)
    return gscLimitSwitch;
}


// Function to read the NSC limit switch and return pressed status
int nscLimitSwitchFunction() {
    // Read the limit switch value
    int nscLimitSwitch = 1-limN.getStateRaw();    // If getStateRaw is 0 (low), the button is pressed

    // Return pressed (1) or not pressed (0)
    return nscLimitSwitch;
}


// Helper function for photosensorFunction()
float average_analogRead(int pinNumber, float &movingAverage){
  int sampleAverageCount = 10;   // Set for now. Update as needed.

  analogRead(pinNumber);   // used to switch adc to specific pinNumber

  movingAverage = movingAverage + ((analogRead(pinNumber) - movingAverage) / sampleAverageCount);

  float movingAverageVolts = movingAverage * (5.0 / 1023.0);   // Find Volts by dividing by bin width and multiplying by 5 (max voltage)
  return movingAverageVolts;
}


// Function to read the photoresistor and return detection status
int photosensorFunction() {

  ambientSensorVoltage1 = average_analogRead(ambientPhotoSensorPin1, movingAverageAmbient1);   // pin and average for ambient photoresistor
  ambientSensorVoltage2 = average_analogRead(ambientPhotoSensorPin2, movingAverageAmbient2);   // pin and average for ambient photoresistor
  startLEDSensorVoltage = average_analogRead(detectingPhotoSensorPin, movingAverageDetecting);   // pin and average for start LED photoresistor
  if(((startLEDSensorVoltage < ambientSensorVoltage2) && (startLEDSensorVoltage < ambientSensorVoltage1))
  
  
  
  ){
    return 0; // Not Detected
  } else{
    return 1; // Detected
  }
}
