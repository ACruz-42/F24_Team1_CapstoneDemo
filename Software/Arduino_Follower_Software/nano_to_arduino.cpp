#include "nano_to_arduino.h"

// This file is for functions that are used to communicate data from the arduino to the nano.

// Input left then right wheel. Controls drivetrain (2 motors) speed and direction.
void robotSpeedFunction(float leftWheelSpeed, float rightWheelSpeed) {
    // Constrain wheel speeds between -100 and 100
    leftWheelSpeed = constrain(leftWheelSpeed, -100, 100);
    rightWheelSpeed = constrain(rightWheelSpeed, -100, 100);

    // Set Left Motor
    if (leftWheelSpeed > 0) {
        digitalWrite(leftDriveDir1Pin, HIGH);
        digitalWrite(leftDriveDir2Pin, LOW);
        analogWrite(leftDrivePWMPin, map(leftWheelSpeed, 0, 100, 0, 255));
    } 
    else if (leftWheelSpeed < 0) {
        digitalWrite(leftDriveDir1Pin, LOW);
        digitalWrite(leftDriveDir2Pin, HIGH);
        analogWrite(leftDrivePWMPin, map(-leftWheelSpeed, 0, 100, 0, 255));
    } 
    else {
        digitalWrite(leftDriveDir1Pin, LOW);
        digitalWrite(leftDriveDir2Pin, LOW);
        analogWrite(leftDrivePWMPin, 0);
    }

    // Set Right Motor
    if (rightWheelSpeed > 0) {
        digitalWrite(rightDriveDir1Pin, HIGH);
        digitalWrite(rightDriveDir2Pin, LOW);
        analogWrite(rightDrivePWMPin, map(rightWheelSpeed, 0, 100, 0, 255));
    } 
    else if (rightWheelSpeed < 0) {
        digitalWrite(rightDriveDir1Pin, LOW);
        digitalWrite(rightDriveDir2Pin, HIGH);
        analogWrite(rightDrivePWMPin, map(-rightWheelSpeed, 0, 100, 0, 255));
    } 
    else {
        digitalWrite(rightDriveDir1Pin, LOW);
        digitalWrite(rightDriveDir2Pin, LOW);
        analogWrite(rightDrivePWMPin, 0);
    }
}


// Input +/- 1 or 0. Controls whether the auger (1 motor) is on and direction
void augerFunction(int auger) {
    if (auger == -1) {
    digitalWrite(augerDirPin1, LOW);
    digitalWrite(augerDirPin2, HIGH);
    analogWrite(augerPWMPin, 255);
    //Serial.println("Auger: Negative direction");
    } else if (auger == 0) {
    digitalWrite(augerDirPin1, LOW);
    digitalWrite(augerDirPin2, LOW);
    analogWrite(augerPWMPin, 0);
    //Serial.println("Auger: No rotation");
    } else if (auger == 1) {
    digitalWrite(augerDirPin1, HIGH);
    digitalWrite(augerDirPin2, LOW);
    analogWrite(augerPWMPin, 255);
    //Serial.println("Auger: Positive direction");
    }
}


// Input +/- 1 or 0. Controls whether the sweeper (1 motor) is on and direction
void sweeperFunction(int sweeper) {
    if (sweeper == -1) {
        digitalWrite(sweeperDirPin1, LOW);
        digitalWrite(sweeperDirPin2, HIGH);
        analogWrite(sweeperPWMPin, 175);
        //Serial.println("Sweeper: Negative direction");
    } else if (sweeper == 0) {
        digitalWrite(sweeperDirPin1, LOW);
        digitalWrite(sweeperDirPin2, LOW);
        analogWrite(sweeperPWMPin, 0);
        //Serial.println("Sweeper: No rotation");
    } else if (sweeper == 1) {
        digitalWrite(sweeperDirPin1, HIGH);
        digitalWrite(sweeperDirPin2, LOW);
        analogWrite(sweeperPWMPin, 175);
        //Serial.println("Sweeper: Positive direction");
    }
}


// Input +/- 1 or 0. Controls whether the beacon arm (servo) is resting, at initial rotation, or desired location
void beaconArmFunction(int beaconArm) {
    if (beaconArm == -1) {
        beaconArmServo.write(desiredAngleBeaconArm);
        //Serial.println("Beacon Arm: Negative position (down)");
    } else if (beaconArm == 0) {
        //Serial.println("Beacon Arm: No rotation");
    } else if (beaconArm == 1) {
        beaconArmServo.write(initialAngleBeaconArm);
        //Serial.println("Beacon Arm: Positive position (vertical)");
    }
}


// Input +/- 1 or 0. Controls whether the beacon gripper (servo) is resting, at initial rotation, or desired location
void beaconGripperFunction(int beaconGripper) {
    if (beaconGripper == -1) {
        beaconGripperServo.write(desiredAngleBeaconGripper);
        //Serial.println("Beacon Gripper: Negative position (opened)");
    } else if (beaconGripper == 0) {
        //Serial.println("Beacon Gripper: No rotation");
    } else if (beaconGripper == 1) {
        beaconGripperServo.write(initialAngleBeaconGripper);
        //Serial.println("Beacon Gripper: Positive position (closed)");
    }
}


// Input +/- 1 or 0. Controls whether the GSC gripper (linear actuator) is resting, is open, or is closed
void gscGripperFunction(int gscGripper) {
    if (gscGripper == -1) {
        digitalWrite(gscGripperDirPin1, LOW);
        digitalWrite(gscGripperDirPin2, HIGH);
        analogWrite(gscGripperPWMPin, 255);
        //Serial.println("GSC Gripper: Negative direction");
    } else if (gscGripper == 0) {
        digitalWrite(gscGripperDirPin1, LOW);
        digitalWrite(gscGripperDirPin2, LOW);
        analogWrite(gscGripperPWMPin, 0);
        //Serial.println("GSC Gripper: No rotation");
    } else if (gscGripper == 1) {
        digitalWrite(gscGripperDirPin1, HIGH);
        digitalWrite(gscGripperDirPin2, LOW);
        analogWrite(gscGripperPWMPin, 255);
        //Serial.println("GSC Gripper: Positive direction");
    }
}


// Input +/- 1 or 0. Controls whether the NSC gripper (linear actuator) is resting, is open, or is closed
void nscGripperFunction(int nscGripper) {
    if (nscGripper == -1) {
        digitalWrite(nscGripperDirPin1, LOW);
        digitalWrite(nscGripperDirPin2, HIGH);
        analogWrite(nscGripperPWMPin, 255);
        //Serial.println("NSC Gripper: Negative direction");
    } else if (nscGripper == 0) {
        digitalWrite(nscGripperDirPin1, LOW);
        digitalWrite(nscGripperDirPin2, LOW);
        analogWrite(nscGripperPWMPin, 0);
        //Serial.println("NSC Gripper: No rotation");
    } else if (nscGripper == 1) {
        digitalWrite(nscGripperDirPin1, HIGH);
        digitalWrite(nscGripperDirPin2, LOW);
        analogWrite(nscGripperPWMPin, 255);
        //Serial.println("NSC Gripper: Positive direction");
    }
}


// Input +/- 1 or 0. Controls whether the NSC gripper (servo) is resting, at initial rotation, or desired location
void gscLeanerFunction(int gscLeaner) {
    if (gscLeaner == -1) {
        gscLeanerServo.write(desiredAngleGSC);  
        //Serial.println("GSC Leaner: Negative position (leaning)");
    } else if (gscLeaner == 0) {
        //Serial.println("GSC Leaner: No rotation");
    } else if (gscLeaner == 1) {
        gscLeanerServo.write(initialAngleGSC); 
        //Serial.println("GSC Leaner: Positive position (vertical)");
    }
}


// Input +/- 1 or 0. Controls whether the NSC gripper (servo) is resting, at initial rotation, or desired location
void nscLeanerFunction(int nscLeaner) {
    if (nscLeaner == -1) {
        nscLeanerServo.write(desiredAngleNSC);
        //Serial.println("NSC Leaner: Negative position (leaning)");
    } else if (nscLeaner == 0) {
        //Serial.println("NSC Leaner: No rotation");
    } else if (nscLeaner == 1) {
        nscLeanerServo.write(initialAngleNSC);
        //Serial.println("NSC Leaner: Positive position (vertical)");
    }
}

