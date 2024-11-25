# Sensors Subsystem Detail Design
## Function of the Subsystem
The goal of this subsystem is to be able to provide information to the robot for multiple different types of data.
The information needed to provide includes position of the robot, number of materials collected, number of materials deposited, state of start LED, and whether the collected material is magnetic or not.

The position data is provided as feedback to the motor control.
The number of materials provides information about whether the tasks have been completed or not.
The type of material provides information to the chute control.
The state of the start LED provides information on whether the robot should start or not.
 
## Specifications and Constraints
Specifications:
1.	The robot's sensors shall be able to find the walls of the game field and the cave.
2.	The robot's sensors shall be able to detect when the start LED turns on.
3.	The robot's sensors shall be able to detect the magnetic fields of the Geodinium.
4.	The robot's sensors shall be able to work effectively despite background interference in the competition environment.

Constraints:
1.	The robot shall be able to count the number of materials collected and deposited.
2.	The robot shall know its current position.
3.	The robot's general sensor subsystem shall have a user manual that explains functionality and design intent.

## Overview of Proposed Solution
To meet the listed specifications and constraints, a suite of sensors is composed to solve each of the problems individually.
This suite includes a Light Detection and Ranging device (LiDAR), photoresistors, Hall Effect sensors, and an Inertial Measurement Unit (IMU).
The LiDAR provides direct feedback for position.
It will provide the distance between the robot and the walls of the arena.
This meets specification 1.
This also helps with constraint 2.
The photoresistors will be used to detect the presence of light.
One photoresistor will be used to detect when the start LED has turned on.
This meets specification 2.
The other photoresistors will be used with their own LEDs to count the number of materials.
This meets constraint 1.
The Hall Effect sensors will be used to detect the magnetic field from the magnetic materials.
This meets specification 3.
The IMU will be used to get position through integration of acceleration.
This will be the main solution for constraint 3.
For specification 4, the sensors most prone to noise from the environment will be the photoresistors.
They will need to be properly calibrated to make sure that they do not send a signal when they are not supposed to.

## Interface with Other Subsystems
The IMU and LiDAR will provide positional feedback to the main controller, which is a Jetson Nano.
This positional feedback will be used to set the motor controllers with feedback.
The photoresistor for the start LED will turn on the robot so that it can start completing its goals.
This will require activating the controllers, so that they can start running their scripts.
Each of the controllers will then properly set up and begin running the other subsystems.
The photoresistors for counting materials and the Hall Effect sensors will send information to the lower-level controller, which is an Arduino Mega.
This set of sensors will inform the controller about where the materials should be sent.

## Buildable Schematic
![Sensors Subsystem Schematic](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/aa634817add249cdd91bff9f9b24f9f2ba25e57d/Documentation/Images/Sensors%20Subsystem/Sensors%20Subsystem%20Schematic.svg)

## Operational Flowchart
![Sensors Subsystem Operational Flowchart](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/aa634817add249cdd91bff9f9b24f9f2ba25e57d/Documentation/Images/Sensors%20Subsystem/Sensors_Subsystem_Operational_Flowchart.svg)

## Analysis
### LiDAR
LiDAR’s implementation has a few options that would each meet our specifications.
First, if LiDAR is continuously used to get position feedback, it can be incorporated through Kalman Filters to provide higher resolution of the current position than any single sensor.
However, this option will require more time for developing than any other option [1-2].
Second, if LiDAR is checked on specific time intervals, this position data could be compared with the current position data.
If the two differ, then a correction can be made.
Third, if LiDAR is checked when an error arises, it can be used to find the current position.
Errors that could trigger the LiDAR include motors not moving the robot, such as from running into something or the IMU not reading a change in position when it should be.
This implementation requires the least work for the LiDAR, but proper flags need to be put in place for edge cases.

The current LiDAR picked out for this project is the Garmin LIDAR-Lite v4 LED.
It outputs data with 3.3V GPIO pins.
The Jetson Nano has 3.3V GPIO pins while the Arduino Mega has 5V pins, so it will be read by the Jetson Nano.
The LiDAR has a Field-of-View of 4.77 degrees.
It has a minimum distance of 5 cm and a maximum of 10 m.
Over I2C connection, it has a refresh rate of at least 200 Hz and a maximum of 400 kHz.
At best the error is +/- 1 cm and at worst +/- 5 cm.
The best case is at 2 m, and the worst case is at 10 m.
This specific LiDAR works best because it has a much smaller than average minimum distance.
The maximum at 10 m is more than enough given the farthest distance the robot would read would be 8 ft, or 2.44 m.
This LiDAR also has an onboard microprocessor that averages multiple readings and removes some noise, and it is directly connectable to the robot with standard integration [3-4].

### Photoresistor
Photoresistors will be used for two different problems.
The first issue is to detect the starting LED.
This is solved by using a photoresistor connected between 5 V and an Arduino digital interrupt pin.
When enough light is incident on the photoresistor, it will pull the digital pin high.
The photoresistor will be placed as close as possible to the start LED, so its resistance will be made very low when the LED turns on.
An interrupt pin can be used to turn the Arduino on or to wake it from sleep mode.
The Arduino Mega has 6 dedicated interrupt pins, digital pins that can be tied to interrupts, and analog pins that can be tied to interrupts [5].

The second issue is to count the materials.
They must be counted when entering and exiting the auger, or whether a material has been collected and when it has been deposited.
Keeping track of the materials allows the robot to know when to change the deposit location.
The robot has one auger that deposits into a chute with a lever to designate where the material should go.
When the material exits the chute, it will fall onto a gate that will have a photoresistor that will trigger so the Hall Effect sensors can determine if it is magnetic or not.
To implement the counters, a photoresistor will be placed across from an LED.
The materials will travel between the photoresistor and LED.
Like the start LED sensor, these photoresistors will be at digital high when there is no material and then be at digital low for a moment when a material passes between the photoresistor and LED.
This digital low can be used to count the materials.

The GL125 series photoresistors will be used for their robustness and straightforward application.
They have a maximum voltage of 250 V, much larger than anything the robot will be using.
It has a monomial response that is easily calibrated with software or hardware.
Calibration will be necessary to remove the noise from the environment [6].

### Hall Effect Sensor
There are two different materials that will be collected by the robot.
One of the materials produces a magnetic, while the other does not.
Hall Effect sensors can be used to detect the magnetic field produced by the magnetic materials.
The materials will be deposited on a gate to be measured.
While on this gate, three Hall Effect sensors will be placed along three different orthogonal axes.
The photoresistor will trigger the Hall Effect sensors to be read by the Arduino analog pins.
If any sensor is above a certain software threshold, it will trigger the lever.
Whether the sensors read a magnetic field or not, the material will be dropped after a set amount of time to its container.

The AH49E is a Hall Effect device that has a linear response to magnetic fields.
The input voltage determines the slope, or resolution, of the sensor.
The sensor output half of the input voltage when no magnetic field is present, and it either outputs a higher or lower voltage depending on whether it detects a positive or negative magnetic field.
Each sensor can only detect in one dimension, perpendicular to the flattest side of the device.
Therefore, the robot will need three sensors to detect the three different axes, since the material can be orientated in any direction.
The input voltage has a maximum of 8 V.
5 V will be used, since it is available and the maximum that can be measured by the Arduino [7].

### IMU
The IMU provides valuable feedback to the motor control.
As the robot moves, it could become offset from where it thinks it is.
It is the goal of the IMU to correct this action.
The IMU will provide acceleration and orientation data, through its accelerometer and gyroscope.
The acceleration data will be integrated twice to get position and added to previous position.
This can create detrimental levels of drift and will be accounted for through sensor fusion [8].

The SparkFun Optical Tracking Odometry Sensor (OTOS) incorporates an IMU and an optical velocity sensor to provide positional feedback.
The optical velocity sensor is the same as the one found in a computer mouse.
OTOS comes with its own on-board processor that implements a Kalman Filter between the two sensors and to judge the effectiveness of both.
It also comes with a calibration table to give the sensor a linear offset that is much easier to calibrate than a non-linear offset.
The linear offsets can be measured and input once and stored on the robot, as they will be consistent.
It does not need to move for about 0.5 seconds each time it is turned on to calibrate the gyroscope.
The sensor provides information every 3 ms.
It outputs a digital high when it is ready to send data to help with asynchronous timing.
It is powered with 3.3 V and uses 3.3 V GPIO.
It connects over I2C and will connect directly to the Jetson Nano.
It will need to be on an I2C bus, given that the LiDAR is also connected.
Code is provided to start collecting data as soon as the sensor has been connected [9-10].

## Ethics
The Sensor Subsystem uses multiple devices that have been developed by outside sources.
These sources will be properly accredited to recognize the work that was put into this project.
Out of the sensors listed, the LiDAR and OTOS both have lights.
The LiDAR uses an infrared LED that is invisible and completely safe to the human eye [3].
The OTOS has a chip that produces an infrared Class I Laser [11].
A Class I Laser is completely safe as well [12].
The rest of the sensors follow the rules and will be properly attached to the robot to prevent any hazards.
The Sensor Subsystem will also have a user manual to help future students understand how the Sensor Subsystem operated.
The user manual will provide valuable information for students trying to reproduce or build on the present design.

## Bill of Materials
|Item|Unit Price|Quantity|Total Price|URL|
| :- | :- | :- | :- | :- |
|LiDAR|$81.25|3|$243.75|https://www.mouser.com/ProductDetail/SparkFun/SEN-18009?qs=iLbezkQI%252BsjpCIKpfdq6BA%3D%3D|
|Qwiic Connector Set|$9.99|1|$9.99|https://www.amazon.com/elechawk-SparkFun-Development-Breadboard-Connector/dp/B08HQ1VSVL/ref=sr_1_1_sspa?adgrpid=1338106242467015&dib=eyJ2IjoiMSJ9.1bYPdA1ezeb5gFHXH6XsB8j_GqBRoGAk0GcUDAM8PEfYcGBJ77ShSvPEzUW_INhjSP0031AlKNB-dyPOk89fJy4qy-Nrs00ldtn9lBylSqrD7my9EsG65fyt1yICyv_RpG3J800V0t2WqEHW9XzUSBpxsr0muV04XwQAUGjOt_TkTFDKbz-XpUJfvZbKFWDLzjfvtzvdn7maGenJzwfG6enY1xPiu7dQMyvAh1TjR6U.SBWIRRDpk1HAEXicYN2aO97rvJPiCNZUDlX1QTLRpfk&dib_tag=se&hvadid=83631853403435&hvbmt=bp&hvdev=c&hvlocphy=84051&hvnetw=o&hvqmt=e&hvtargid=kwd-83632021341203%3Aloc-190&hydadcr=24331_13514981&keywords=qwiic+cable+kit&msclkid=6252f0346c8d1666d50f9770b924b95f&qid=1732564400&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1|
|4-port Qwiic I2C Bus|$6.50|2|$13.00|https://www.amazon.com/SparkFun-MultiPort-connectors-Alternative-configuration/dp/B09M9BX55S/ref=sr_1_6?adgrpid=1330410804726624&dib=eyJ2IjoiMSJ9.gPk_ld1g6NEXmTKatkj7Cas8gSAqVjb6kDyNDpHpq8CPL5vU4FsuTYZni6tLwG_-I9OLbbYBPW5UibepItnIw4CbHXDDN_rMdAf8ql-v2auIE830nDBvpk7ejmVqzQIBW865AW1UGXS26T0b_R0RYPd2cmnNnhaFUNNTCaV-IL1Nx1U3iqnLyUgejnxFECOusUZbPl3W0DtIDH4HuBkOJA._xCaRjyFhe2EFA4L4NZZlJ1Jvz8TfXVhjFHMbg9elvU&dib_tag=se&hvadid=83150967415504&hvbmt=be&hvdev=c&hvlocphy=84051&hvnetw=o&hvqmt=e&hvtargid=kwd-83151738740302%3Aloc-190&hydadcr=24364_13514975&keywords=qwiic+cable+-+grove+adapter&qid=1732563803&sr=8-6|
|Photoresistor|$16.49|1|$16.49|https://www.amazon.com/Juried-Engineering-Photoresistor-GL12528-Sensitive/dp/B08F3WPNPF|
|Green LED|$0.311|2|$0.622|https://www.newark.com/led-technology/l02r5000q1/led-green-t-1-3-4-5mm-3-7mcd-567nm/dp/97K4041?CMP=KNC-BUSA-GEN-Shopping-ALL&mckv=s_dc|pcrid||plid||kword||match|e|slid||product|97K4041|pgrid|1231453304461926|ptaid|pla-4580565455222458:aud-807872783|&msclkid=9dbbf8c3c12e198d33ec9f87232c30e8|
|Hall Effect Sensor|$0.48|3|$1.44|https://www.mouser.com/ProductDetail/Diodes-Incorporated/AH49FZ3-G1?qs=dZoB6MK9LKPUjOBJDQRw%2FA%3D%3D|
|Solderful Breadboard|$2.49|1|$2.49|https://www.digikey.com/en/products/detail/digikey/DKS-SOLDERBREAD-01/21274484|
|OTOS|$79.95|1|$79.95|https://www.amazon.com/SparkFun-Optical-Tracking-Odometry-Sensor/dp/B0D6LQGBSK?source=ps-sl-shoppingads-lpcontext&ref_=bing_fplfs&psc=1|
|Total|||$367.732|

## Works Cited
1.	G. Welch, G. Bishop. “An Introduction to the Kalman Filter.” mit.edu. Mar. 2002. Accessed: Nov. 2024. [Online]. Available: https://www.mit.edu/course/16/16.070/www/project/PF_kalman_intro.pdf
2.	“How a Kalman filter works, in pictures.” bzarg.com. Apr. 2015. Accessed: Nov. 2024. [Online]. Available: https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/ 
3.	“LIDAR-Lite v4 LED.” garmin.com. Accessed: Nov. 2024. [Online]. Available: https://www.garmin.com/en-US/p/610275#specs
4.	“LIDAR-LITE V4 LED: OPERATION MANUAL AND TECHNICAL SPECIFICATIONS.” garmin.com. Sep. 2020. Accessed: Nov. 2024. [Online]. Available: https://static.garmin.com/pumac/LIDAR-Lite%20LED%20v4%20Instructions_EN-US.pdf
5.	“Arduino® Mega 2560 Rev3: Product Reference Manual.” arduino.cc. Nov. 2024. Accessed: Nov. 2024. [Online]. Available: https://docs.arduino.cc/resources/datasheets/A000067-datasheet.pdf
6.	“GL125 Series Photoresistor.” know-tech.com. Accessed: Nov. 2024. [Online]. Available: https://knowing-tech.com/wp-content/uploads/data/g/GL12528.pdf
7.	“LINEAR HALL-EFFECT IC : AH49E.” digikey.com. Rev. 1.3, Aug. 2010. Accessed: Nov. 2024. [Online]. Available: https://www.digikey.com/htmldatasheets/production/1364519/0/0/1/ah49e.html?utm_adgroup=General&utm_source=bing&utm_medium=cpc&utm_campaign=Dynamic%20Search_EN_RLSA&utm_term=digikey&utm_content=General&utm_id=bi_cmp-384476624_adg-1302921504343623_ad-81432643449113_dat-2333232393680005:aud-807631099:loc-190_dev-c_ext-_prd-&msclkid=ef9edc5046c81a3f6ce4bb4050601364
8.	“LSM6DSO: Datasheet.” st.com. Rev. 3, Jun. 2024. Accessed: Nov. 2024. [Online]. Available: https://www.st.com/resource/en/datasheet/lsm6dso.pdf
9.	loricrotser. “SparkFun Optical Tracking Odometry Sensor - PAA5160E1 (Qwiic) Hookup Guide.” sparkfun.com. Nov. 2024. Accessed: Nov. 2024. [Online]. Available: https://docs.sparkfun.com/SparkFun_Optical_Tracking_Odometry_Sensor/introduction/
10.	“SparkFun_Optical_Tracking_Odometry_Sensor.” github.com. Nov. 2024. Accessed: Nov. 2024. [Online]. Available: https://github.com/sparkfun/SparkFun_Optical_Tracking_Odometry_Sensor
11.	“PAA5160E1-Q: Optical Tracking Chip.” sparkfun.com. Ver. 0.8, Sep. 2022. Accessed: Nov. 2024. [Online]. Available: https://cdn.sparkfun.com/assets/c/6/8/0/5/PAA5160_Datasheet_General.pdf
12.	J. Maltais. “Class 1 Laser Products: Regulations Explained.” laserax.com. Aug. 2021. Accessed: Nov. 2024. [Online]. Available: https://www.laserax.com/blog/class-1-laser-products-regulations#:~:text=A%20class%201%20laser%20product%20is%20a%20device,a%20%E2%80%9CClass%201%20laser%20product%E2%80%9D%20label%20are%20safe
