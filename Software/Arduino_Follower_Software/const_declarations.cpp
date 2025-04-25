#include "const_declarations.h"

Servo gscLeanerServo, nscLeanerServo, SortServo, beaconArmServo, beaconGripperServo;

ezButton limG(31, INTERNAL_PULLUP);
ezButton limN(14, INTERNAL_PULLUP);
ezButton limS(33, INTERNAL_PULLUP);

float voltageAugerSensor, currentAugerSensor, voltageSweeperSensor, currentSweeperSensor;
float movingAverageAmbient1, movingAverageAmbient2, movingAverageDetecting,
      ambientSensorVoltage1, ambientSensorVoltage2, startLEDSensorVoltage;
