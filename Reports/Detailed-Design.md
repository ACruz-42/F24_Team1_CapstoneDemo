# Detailed Design
## Function of the Subsystem 
The motor control subsystem is meant to carry out the functions of the robot based on sensory input and the needs of the given situation during the competition as driven by the Master Control. The drivetrain motors will actuate the translation of the robot and will change the speed based on factors such as weight, obstacles, time remaining, among other crucial considerations for obtaining the maximum amount of points. Additional mechanisms on the robot will be used to collect, sort, and distribute astral material in their appropriate containers. These mechanisms will also require motor control, and they will use various types and configurations of motors. 

The drivetrain motor system functions as the feedback-based reaction center for the robot’s processes. It uses the input taken in from sensory data, such as object and line detection or map navigation, and follows the commands given to it from a microcontroller to perform the physical responses of the robot. Motor control can include the following components: a microcontroller (MC), motor, motor driver, encoder, power supply, and specific components for noise reduction and circuit protection [1]. The motor microcontroller carries the digital signal commands for the designated motor to operate as required. However, the power that the MC needs to function is not enough in comparison to what the motor needs. Therefore, it is essential to have a component that can step up the power for the motor while still using the MC for commands. This is the purpose of the motor driver. The motor microcontroller sends a digital signal to the driver using PWM to set the desired motor speed. Encoders that detect the motor shaft speed/position to provide the actual speed of the motors are useful for completing a closed loop feedback system, such as with PID control [2]. All logic control circuitry, which includes the microcontroller and encoders, will receive low voltage from the power subsystem, while the motor driver will receive high voltage in order to provide the high power needs of the motors. 

Several types of motors are utilized for the astral material collection and sorting process. Brushed DC motors are used for the mechanisms that have continuous feedback based on desired versus actual motor speed, such as with the overall robot movement and the collection of astral material. Separate motor drivers are connected to these motors and provide the appropriate power based on PWM input from the microcontroller. Linear actuators will be used for clamping onto the shipping container, and they will need drivers as well for directional control of the extension of the actuator. Servo motors will be used for the material sorting mechanism via a system of gates, lifting the shipping container, and controlling the positioning of an arm that will place the Team Beacon.  

## Specifications and Constraints 
#### 1) The motors shall operate at a voltage of less than 30 volts [S12].

Rationale: This voltage limit was put in place due to the requirements placed by Game Manual 1 at Rule 16 for the purpose of safe but capable robot operation. 

#### 2) The motor control subsystem shall be capable of an immediate termination of functions induced by an emergency stop button [S7]. 

Rationale: This command for immediate stoppage brought about by E-Stops is required by the Game Manual 1 at Rule R04 and enables increased protection for the equipment, arena, and personnel on site.  

#### 3) The motors shall be capable of speeds allowing the robot to traverse the game field at least twice (once for collecting astral material, and once for the return trip) within three minutes (the length of a match) [S2]. 

Rationale: This specification was put in place so that the robot would be equipped to at least reach any point on the map and return to deposit material for points. On this one trip, the current plan is to find the most optimal route around the field for material collection, but making it so that the robot would have the ability to quickly and efficiently traverse the entire field and back would account for any suboptimal deviations within the time limit. 

#### 4) The motors shall be capable of reversing the robot in the case that reversing the robot is the only method of not damaging the game field walls [S4]. 

Rationale: This was of consideration due to the need for the robot to be able to have escape maneuverability near field walls, with damage to the field being grounds for a penalty.  

#### 5) The motor subsystem shall be designed in such a way that accounts for background interference in the competition environment [S11]. 

Rationale: This specification was put in place due to the requirement set by Game Manual 1 at Rule R13, in which competitors should account for naturally occurring electrical noise in the competition environment that may interfere with the lower-level circuitry.  

#### 6) The motor subsystem shall have a user manual that explains functionality and design intent [C2]. 

Rationale: This specification was placed in order to follow a precedent set by prior capstone groups for creating documentation that lays out the necessary design information for any future work on a similar project or building on the same project.  

#### 7) The motor subsystem shall adhere to applicable requirements in standard IEC 60204-1 pertaining to electrical supply, electromagnetic compatibility, emergency stop, and control circuit protection [C3]. 

Rationale: This constraint was put in place for the motor subsystem to abide by established electrical codes, with this particular IEC standard laying out several different types of safety measures that would be applicable to the motor control circuitry. It aligns with the request from the Game Manuals in the mandatory inclusion of E-Stops. It also presents the necessity to include components that promote overcurrent protection and proper grounding [3]. Clear labels and documentation for the circuit components involved are also needed by this standard [3].  
 
## Overview of Proposed Solution
### Drivetrain
The solution will incorporate several layers of command for the robot movement. The first layer will involve the Arduino Mega microcontroller, which will process the logic for the PID control of the drivetrain motors. The PID parameters will be adjusted by the Mega after it calculates the error between the desired and actual speed. The motor driver that will be used to carry out the speed adjustment from the Mega is the Pololu Dual VNH5019 Motor Driver. This driver acts as a regulator for how power is used between the 12V source and the motor, using a PWM command that resulted from the speed adjustment. This motor driver is compatible with Arduino, and it can control two bidirectional brushed DC motors. The bidirectional property fulfills Specification 4, regarding the request to be able to have forward and backward control for each motor so that the robot can escape potential obstructions and damage the field. The motors that will be used are two 12V Metal DC Geared-Down Motors with built-in incremental encoders. These motors operate at a max of 12V, which fulfills Specification 1 of not exceeding the competition 30V limit. The VNH5019 driver is compatible with voltage ranges from 5.5 to 24 V, fitting the 12V motor spec. The stall current of the motor is 5.5A, and the current rating per motor for the VNH5019 is 12A, meaning that the maximum possible motor current is well within a safe threshold with this driver. The driver also has built-in overcurrent protection, reverse-voltage protection, and current sensing, which addresses the IEC 60204-1 standard constraint for safe electrical practice in the control of the motor subsystem. Electrical components such as a switch and fuse can be installed on the power line to the motor driver so that the E-Stop request from Specification 2 and IEC 60204-1 can be fulfilled and overcurrent risk can be mitigated. A user manual based on the design report documentation can be created, fulfilling Specification 6. Specification 5 can be fulfilled through proper grounding and electrical shielding/isolation techniques. As far as range is concerned, in addressing Specification 3, the chosen motor will have specs provided that can be used to calculate the motor speed, wheel speed, and resulting time taken for the robot to traverse the entire field twice. The results of said calculations are present in the Analysis section. 

### Collecting and Sorting Process
The mechanisms dedicated to collecting and sorting the astral material are primarily being designed by the Mechanical Engineering team, but the motor control for each mechanism will still be addressed here.  

At the start of the collection process, the Cosmic Shipping Containers will be picked up by two clamping arms for secure transport as the robot searches for astral material. The clamping mechanism will involve two linear actuators that will be regulated in speed and direction by their own respective motor drivers, which are controlled via PWM signals from the Jetson Nano. The actuators will receive a signal from a limit switch, placed at the ending extension point for one of the actuators, so that they can detect when the actuator reaches the desired compression length for the container. Two pressure sensors will be placed at the extremities of the actuators to quantify the compression applied. In order to lift the Cosmic Shipping Containers, two servo motors will be used on an arm that will lift the container and lean it against the base of the robot for transport. These servo motors will have their angle of inclination controlled directly by a PWM connection to the Arduino Mega.  

In order to collect astral material and put it into the correct container, there will be a roller, similar in form to a vacuum roller, at the front of the robot that will sweep up material and place it into an auger. The auger will pull up astral material, one by one, and deliver them to a sorting area. In this stage, the solution includes two brushed DC motors with each having their own motor driver, one for the speed and direction of the roller and another for the speed and direction of the auger. The drivers will be controlled via a PWM signal from the Arduino Mega.  

In the sorting stage, each astral material will go through a chute that has two gates. The first will catch the astral piece from going any further and have it scanned by three surrounding Hall Effect sensors that will determine whether it is the magnetic Geodinium or the non-magnetic Nebulite. There are two chutes for each type beyond this gate, with another gate in between that flips to one side or the other based on the type scanned. In this solution, there are two servo motors that will be implemented, with each servo driving each of the two gates. The position of the servos will be determined by a PWM signal from the Arduino Mega.  

Finally, the Beacon Arm will be a 1 degree-of-freedom arm that will swing out from the robot, holding the Beacon during the swing, and place the Beacon at the Beacon Mast in the middle of the west wall of the field. The motor solution that would be implemented for this includes two servo motors, one for the arm and one for the grabber, that would be controlled by PWM directly via the Arduino Mega. The team has yet to fully commit to the Beacon Arm, but this would be the solution in the event that it would be feasible to include.  

## Interface with Other Subsystems
### Drivetrain
The motor control subsystem will communicate primarily with the Jetson Nano microcontroller, designated as the Master Control. The Arduino Mega that houses the motor control processes will transfer serial data commands and information via a USB connection between the Nano (USB-A) and Mega (USB-B). Inputs from the Nano to the Mega will include desired motor speeds and directions, along with override commands to halt motor control processes in case of encountering obstructions (such as a wall) or running out of time. Outputs from the motor control subsystem to others will primarily be in the form of data updates to the Nano about motor performance and actual speed. The Mega will use the properties of the encoders to track the positioning of the motor shaft and report rotational position data that can be converted into the actual speed, given the logged time frame. The Mega will be using this reporting to make onboard adjustments to the motor speed using PID control, attempting to match the set desired speed. The Nano will keep track of the reported actual speed to understand the current state of the robot and how it should continue to implement sensor data.  

Aside from Master Control, the Motor Control subsystem will also receive inputs from the Power Management subsystem. The motors are 12V and will vary in power usage based on the VNH5019 Motor Driver module. 12V will be sent from the power circuit to the driver. The logic circuitry of the driver and the Arduino Mega will require a step down to 5V. Therefore, a buck converter that steps down the maximum supplied voltage of 12V to 5V will be connected between the power circuit and driver/ Mega as well.

### Collecting and Sorting Process
For each of the mechanisms that involve servo motors, the input going into the motor will come from PWM connections at the Arduino Mega. These mechanisms include the sorting gates, lifting arm, and Beacon arm. The type of data transmitted is positional data for the angle of inclination of the servo, controlled by the width of the PWM signal [4]. Power inputs for the servos are rated at 5V. For the mechanisms that involve brushed DC motors and drivers, which are the linear actuator and roller-auger stage, a PWM signal will be sent from the Arduino Mega as an input to the drivers for speed and direction control. Power inputs for the motor drivers are rated at 12V. The pressure sensor will transmit analog data to the Arduino Mega, while the limit switch will transmit a digital signal indicating whether a trigger was activated.  

## 3D Model of Custom Mechanical Components 

![Model_Drivetrain](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/9deccc79205ce5f38ae658b8f7e458ed510e71b9/Reports/Photos/Model_Drivetrain.png)
This is a 3D model of the drivetrain for the robot, placed at the center of the overall robot frame. There are two drive wheels attached to brushed DC motors that enable the robot to move forward, backward, and rotate at a point. This model was constructed by Cooper Nelson on the Mechanical Engineering Team. 

![Model_Auger](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/9deccc79205ce5f38ae658b8f7e458ed510e71b9/Reports/Photos/Model_Auger.png)
This is a 3D model of the Auger and Hopper (staging area) for the astral material to be picked up from the Roller collection, one by one, and taken up to the top. After reaching the top, the material will be deposited into the sorting area. This was designed by Caleb Sullivan on the Mechanical Engineering Team. 

![Model_Roller](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/9deccc79205ce5f38ae658b8f7e458ed510e71b9/Reports/Photos/Model_Roller.png)
This is a 3D model of the Roller/Sweeper mechanism, with an astral material piece at the front for reference. The material will get swept into the Roller, in a similar fashion as with a vacuum cleaner. This model was constructed by Caleb Sullivan on the Mechanical Engineering Team.  

## Buildable Schematic
The following diagram connections were informed by [6], [8], [9], [10], and [11].  

### Drivetrain Subsystem
![Drivetrain2](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/9deccc79205ce5f38ae658b8f7e458ed510e71b9/Reports/Photos/Drivetrain2.png)
### Servo Motor Mechanisms
![ServoMotors](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/9deccc79205ce5f38ae658b8f7e458ed510e71b9/Reports/Photos/ServoMotors.png)
### Auger and Roller Mechanisms
![Auger_Roller](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/9deccc79205ce5f38ae658b8f7e458ed510e71b9/Reports/Photos/Auger_Roller.png)
### Container Lift Mechanism Using Linear Actuators
![LinearActuators](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/9deccc79205ce5f38ae658b8f7e458ed510e71b9/Reports/Photos/LinearActuators.png)
## Operational Flowchart
### Drivetrain PID Loop
![OperationalFlowchart](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/9deccc79205ce5f38ae658b8f7e458ed510e71b9/Reports/Photos/OperationalFlowchart.png)
The operations of this flowchart were informed by [5].

## BOM
Items with an asterisk (*Part Name) will be purchased by the Electrical Engineering Team. Other items will come from the Mechanical Team.

|Part|Manufacturer|Part Number|Distributor|Distributor Part Number|Quantity|Price per Item|url|
| :- | :- | :- | :- | :- | :- | :- | :- |
|12V 50:1 Metal DC Geared-Down Motor 37Dx70L mm, with 64 CPR Encoder |CQRobot |CQR37D12V64EN-F |Amazon |ASIN: B08ZK7KNJW |2 |$33.99 |https://www.amazon.com/CQRobot-Ocean-6V-3W-20RPM-40-oz-12V-6W-40RPM-70/dp/B08ZK7KNJW/ref=sr_1_4?crid=38Y3CY1LT0YV0&dib=eyJ2IjoiMSJ9.BJInkt-mOvbyqE9rPeW5wzLtQvkRXPWz5iX5EqsGIX-S6k0LMyT6MN2WSTMazatJnzVB2sg6_rBBrgHcgQ_r5Ogm0jqRmWbpA8eLjoaKIsg7Jk9DcjW49A4Y3hu6E3x1Hv2-JO4EBvhhBa_gzpnUWwRhwE65ZetaJG3KfLtXdMNyEbeSOt5-fj-th6s2zJD28hAa7inJo4Tmj8JBafQvimgANokXgq4Pb78ep_7li1lW4a2o32BF9UcYLGARGdyxDcdF-qnXK11sxsskJ_sVptY9KB1AUIok3Jgtbowg6jM.3EWeHV1v6uEWDgtNmLtADC-KscInyWKtzwH9-ltXZVg&dib_tag=se&keywords=dc%2Bmotor%2Bwith%2Bencoder&qid=1728485580&sprefix=dc%2Bmotor%2Bwith%2Bencoder%2Caps%2C87&sr=8-4&th=1|
|*Pololu Dual VNH5019 Motor Driver Shield for Arduino |Pololu |2507 |Pololu |N/A |1|$59.95 |https://www.pololu.com/product/2507|
|*Arduino Mega |Arduino |2152366 |Amazon |ASIN: ‎ B0046AMGW0 |1|$43.56 (Will borrow from lab) |https://www.amazon.com/ARDUINO-MEGA-2560-REV3-A000067/dp/B0046AMGW0/ref=asc_df_B0046AMGW0?mcid=7091fc990cb33b948372fc448382ff81&tag=hyprod-20&linkCode=df0&hvadid=693392565994&hvpos=&hvnetw=g&hvrand=5593089195493827462&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1025954&hvtargid=pla-516265455074&psc=1|
|9g Micro Servo Motor 10 pack (Sorting and Beacon) |Miuzei |N/A |Amazon |ASIN: B072V529YD |1 |$18.99 |https://www.amazon.com/Micro-Helicopter-Airplane-Remote-Control/dp/B072V529YD/ref=asc_df_B072V529YD?mcid=26014c223ff03f518209407be7b87cb0&tag=hyprod-20&linkCode=df0&hvadid=693442482467&hvpos=&hvnetw=g&hvrand=14249445501973615169&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1025954&hvtargid=pla-568736295296&psc=1|
|35kg Servo Motor (Lifting) |ZOSKAY |35 |Amazon |ASIN: B07S9XZYN2 |2 |$28.99 |https://www.amazon.com/ZOSKAY-Coreless-Digital-Stainless-arduino/dp/B07S9XZYN2/ref=asc_df_B07S9XZYN2/?tag=hyprod-20&linkCode=df0&hvadid=693398985551&hvpos=&hvnetw=g&hvrand=9283053899120098340&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1025954&hvtargid=pla-1132196099251&mcid=58bf84c290c03c38a1f2ee34f8d58ee1&th=1|
|High-Speed 0.6"/sec Linear Actuator 12v |Rtisgunpro |MN |Amazon |ASIN: ‎ B09X994MGX |2 |$18.99 |https://www.amazon.com/High-Speed-Actuator-actuators-Cabinets-Automation/dp/B09X994MGX/ref=sr_1_5?crid=1VQ1IAOFPQL5H&dib=eyJ2IjoiMSJ9.9vA-uKal6zgPplWh71fkUWrXjIgHIQ2sZRb4GzRhSJGvMjLZPTAkdsvKkT3tCS_N2xlbI8ykjulrQ8LoiKutLNfrHx89ZdUQAv2G_aUU0t2bxKPndRvlZcfsJCxaUFM5jO0tfuDnVq2q1XCD7cruumfhwH1hG26nIDDGe9WKK3Wyth7pDDJ3mk4uXIlh1c8w53Q_wJH5HJu2E9LD_QOyyvhgb6l9z6nZ4cwf4fdioHA.R_liDHu-85GNSdjx_JRxk_EfoCpAv_Y1sLQF6AgbyHY&dib_tag=se&keywords=small%2Blinear%2Bactuator&qid=1729094388&sprefix=small%2Blinear%2Bactuator%2Caps%2C88&sr=8-5&th=1|
|Auger Greartisan DC 12V 200RPM Turbo Worm Geared Motor |Greartisan |JSX40-370 |Amazon |ASIN: B08K7HNXTM |1 |$14.99 |https://www.amazon.com/Greartisan-120RPM-Turbine-Reduction-JSX69-370/dp/B08K7HNXTM/ref=sr_1_6?crid=297B969J8J3GK&dib=eyJ2IjoiMSJ9.DmvE-0S-1vqMUtwrJu4RBTeijdliVi4GlUbSQcZpcpsVUkzn4zoJz3sHf0bKjegf6YnKT7lXt41almv6zCPcKVmeYkJOeWigW-Z3LS3Ehosy2yxVlGbInlJ0mbcyNyfRGas-f4ugUQ0N-5NthmtmXlCsw54A9XdjyVLZv80Qu9MRwtaREp8TvVw1ff6WM6cLv1TGfUlAeDl6I4J1CKz2gG9zMHzmDx-KRd4KGQZwwAHBU5czotHYPCUxUOrFDu9kaYtc31JyTF_7OLa1bPMCCSn_EGrJlBWVIUcpyqa-7D4.PgNxnbaXbRU4FKi_T0Uns1Gf1GcyQfZyRNdh0Izl42k&dib_tag=se&keywords=right%2Bangle%2Bdc%2Bmotor&qid=1730907935&sprefix=right%2Bangle%2Bdc%2Bmotor%2Caps%2C103&sr=8-6&th=1|
|Greartisan DC 12V 200RPM Turbo Worm Geared Motor with Mounting Bracket |Greartisan |JSX40-370 |Amazon |ASIN: B0D1KCX2GX |1|$24.99 |https://www.amazon.com/Greartisan-200RPM-Geared-Mounting-Bracket/dp/B0D1KCX2GX|
|*4 PACK L298N Motor Drive Controller Board DC Dual H-Bridge |AITRIP |N/A |Amazon |ASIN: B07WS89781 |1|$9.99 |https://www.amazon.com/Controller-H-Bridge-Stepper-Control-Mega2560/dp/B07WS89781/ref=asc_df_B07WS89781?mcid=42d0e88eaa493b9fb52053e1b3be29a5&tag=hyprod-20&linkCode=df0&hvadid=693508669574&hvpos=&hvnetw=g&hvrand=11400189813213800201&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1025954&hvtargid=pla-881401609127&th=1|
|HiLetgo 10pcs Micro Limit Switch |HiLetgo |3-01-1546 |Amazon |ASIN: ‎ B07X142VGC |1|$5.99 |https://www.amazon.com/gp/product/B07X142VGC/ref=sw_img_1?smid=A30QSGOJR8LMXA&psc=1|
|2Pcs Thin Film Pressure Sensor |Walfront |Walfront9snmyvxw2|Amazon |ASIN: B07T1CHY58 |2|$9.78 |https://www.amazon.com/dp/B07T1CHY58/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B07T1CHY58&pd_rd_w=zlszL&content-id=amzn1.sym.a2c35b81-48c8-45f6-82ba-746f41586c3a&pf_rd_p=a2c35b81-48c8-45f6-82ba-746f41586c3a&pf_rd_r=GE9RGFF0BBAD7MN92ASS&pd_rd_wg=keNW6&pd_rd_r=b796f1c5-01db-4ffc-b09e-d7b5a409e1db&s=appliances&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM|
|*Electronics Kit Compatible with Arduino |ELEGOO |EL-CK-003 |Amazon |ASIN: B09YRJQRFF |1|$15.99 |https://www.amazon.com/ELEGOO-Electronics-Potentiometer-tie-Points-Breadboard/dp/B09YRJQRFF/ref=sr_1_7?dib=eyJ2IjoiMSJ9.k2vYgAjJWNGKglAlIkbAgmNMmq0P2bXob5_sCJdIZxkkEiNVwg9N45kaXKx17Qie-XBoei14fdK6Fz7pzBAsQh37AvliYf2gRnOeHWhWKn1Y0aVkf-3KWNG68exhf_1XBrrye7gfiwIDO2U4Dvpeq8t8BCpZb0IT_MquAR1l4pTJqv_EZSIEDr6m-05-wGOMPWByHKuReuGqiyoq0A2RUnv76fJXjjSBYkYiEAROABVg_YTXVGhrHcD5plgwk2nDX8Pv390J895DQHs2w1uji36ySBcOhWaSy3muiPV1Amg.g6WZU5xtV00D_jDWeh-Fe-HRdF0cg_xgzKNNXAugUs8&dib_tag=se&keywords=circuit%2Bkit&qid=1732596631&sr=8-7&th=1|

## Analysis
### Wheel Speed
In order to verify that the robot would be able to fulfill the motor performance specifications, a series of calculations must be performed based on the motor characteristics and estimated wheel size. The first objective is to determine the wheel speed. It is assumed that the angular speed of the motor in RPM is equivalent to the angular wheel speed, as the given no-load speed accounts for the gear ratio of 50:1 internally. Wheel speed is calculated via the following equation [7]: 

$S=\pi \cdot D\cdot \left(\frac{RPM}{60\ s}\right)$

S=linear wheel speed, RPM=wheel rotations per minute, D=wheel diameter 

Based on the allotted 12x12 inch space and the estimated vertical space available from the base of the robot to the ground, the Mechanical Engineering team calculated that the wheels should at least have a diameter of 102 mm. The angular speed of the chosen motor is 200 RPM. This value and the wheel diameter in mm can be inserted into the equation for linear wheel speed, as done below: 

$S=\pi \cdot \left(102\ mm\right)\cdot \left(\frac{200\ RPM}{60\ s}\right)=1068.14\ \frac{mm}{s}=42.05\ \frac{in}{s}$
 
Using a linear wheel speed of 42.05 in/s, the time it takes to traverse the game field twice can be calculated, with one path being for collecting astral material and one for the return trip. If the result is within 3 minutes of gameplay, the request from Specification 3 is satisfied. The total area of the field is 93x45= 4185 square inches. Assuming the robot takes up the 12x12 inch starting floor space, one can divide the total area by 144 square inches to get the estimated number of square segments for the robot to move in, which would be about 29 segments. Accounting for a worst case path scenario would mean the robot would traverse every segment on the field twice, which would bring the value up to 58 segments. Moving from one segment to another would involve a displacement of 12 inches forward. The robot can move 42.05 in/s. Therefore, it would take 0.29 seconds (12 in / (42.05 in/s)) for the robot to translate a full segment. To find the total time it would take to traverse 58 segments, each with 12x12 square inches, multiply the time to traverse a full segment by the number of segments, which is demonstrated below:  

$\frac{0.29\ s}{1\ segment}\cdot 58\ segments=16.82\ s$

Therefore, the robot would take approximately 17 seconds at continuous speed operation to traverse the entire field twice, which is well under the 180 second timeframe. However, this is using the maximum, no-load speed, and there will be parts of the chosen path in which the robot is not constantly moving. Nevertheless, this serves as a good estimate for the worst case path scenario and allows more than enough time for stoppages during the match. The chosen motor subsystem satisfies the performance requests of Specification 3. 

### Torque and Maximum Power
Wheel speed is an important factor in understanding how qualified a motor is for satisfying specifications. However, torque is another characteristic that is important for when the robot will carry a heavy load. The relationship between speed and torque is inversely proportional. As motor speed increases, torque decreases, and vice versa [12]. The stall torque is representative of the state in which the motor is not rotating, having no angular speed. The given stall torque from the 50:1 DC Geared-Down Motor at 12V is 21 kg*cm or 2.06 N*m. When the torque is zero, the speed is at its maximum no-load speed, which as discussed previously is 200 RPM, or  20.94 rad/s, for this motor. Maximum power is equal to the product of half the no-load speed and half the stall torque [13]. Therefore, the following equation can be used to find the maximum power for the given motor: 

$P_{\max }=\left(\frac{2.06\ N\cdot m}{2}\right)\cdot \left(\frac{20.94\ \frac{rad}{s}}{2}\right)=10.78\ W$

The speed at a maximum power of 10.78 W will be half of the previously tested speed, but this state of the motor will provide more torque for a more realistic average load expectation. Calculating the new angular speed and the resulting time it would take to traverse the field twice is done below: 

$\frac{200\ RPM}{2}=100\ RPM$

$S=\pi \cdot \left(102\ mm\right)\cdot \left(\frac{100\ RPM}{60\ s}\right)=534.07\ \frac{mm}{s}=21.03\ \frac{in}{s}$

$\frac{12\ in}{21.03\ \frac{in}{s}}=0.57\ s$

$\frac{0.57\ s}{1\ segment}\cdot 58\ segments=33.06\ s$

As demonstrated through these calculations, when a balance of half the potential torque and half the potential speed is available, the robot still traverses the field twice in about 33 seconds.  

### Battery Life and Speed Relationship
In order to determine the longevity of the robot using the motor specifications, one must consider the number of matches that will be played and the battery usage per match. Game Manual 1 states that there will be three qualifying matches and three elimination rounds on the path to first place. It will be assumed that the robot is operating for a full three minutes in each and that the motors will be operating with a worst-case, heavy load current of 5.5A, the stall current. According to [15], the discharge time for a battery is equal to the estimated battery capacity in amp-hours divided by the current draw (amps) from the electrical load. The two motors are the electrical load in this case, each with a maximum 5.5A of current draw for a total of 11A. Six matches, at 3 minutes each, equals 18 minutes or 0.3 hours. Multiply this necessary discharge time of 0.3 hours by the 5.5A maximum to get the necessary battery capacity for the two motors, which equals 1.65 ah. This desired capacity is a small fraction of the available capacity for the 24V batteries being considered, with 100ah or more being a commonly used threshold. Therefore, the battery loss from round to round should not be an issue with regard to the motors. 

It is still important to consider the fact that the speed will drop as the available battery voltage decreases. If the voltage were reduced to 6V instead of the full 12V for the motors, the listed no-load speed would be 100 RPM, which would double the time estimate for the no-load, field segment calculations. Doubling the time estimate for the original no-load speed would result in 34 seconds, which meets Specification 3. Overall, the trend for the relationship between speed and voltage can be seen from [16], with the equation below: 

$RPM=V \cdot Kv\$

RPM=linear wheel speed, V=test voltage, Kv=(No-Load RPM / No-Load Voltage)

During testing, voltage to the motors can be measured using a multimeter, and the relative speed can be calculated using the test voltage and the process above. Exact voltage to speed data can then be extracted and used to make adjustments and assess what motor performance range is available. 

### PID Parameter Calculation  
As far as PID tuning is concerned for the Drivetrain motor control, the operational flow chart serves as a visual for how the closed-loop feedback control would look. The algorithm for the PID values is demonstrated here [14]:  

$u\left(t\right)=K\left(e\left(t\right)+\frac{1}{T_i}\int _0^te\left(\tau \right)d\tau +T_d\frac{de\left(t\right)}{dt}\right)$

The PID control loop will be represented using Arduino, with parameters for the proportional, integral, and derivative values being inputs that can change based on experimental feedback. For example, if one starts with just proportional control, the output will oscillate and settle with a significant steady state error. Adding a constant for integral control would help correct the steady state error but add to the settling time. Adding a constant for derivative control would reduce the settling time, which would result in full PID control, the best combination of tools available for adjusting the reaction of the robot as it targets the desired motor speed.  

## References
1.	“Motor Driver Fundamentals: Your Guide To Efficient Motor Control - Jhdpcb,” jhdpcb, 	Jan. 18, 2024. https://jhdpcb.com/blog/efficient-motor-control/#:~:text=The%20key%20role%20of%20the,enable%20speed%20and%20torque%20control 
2.	E. P. Company, “Motor Encoders: What is a Motor Encoder? How Do Motor Encoders 	Work?,” www.encoder.com. 							https://www.encoder.com/motorencoders#:~:text=What%20are%20motor%20encoders%3F,are%20either%20incremental%20or%20absolute 
‌
3.	Safety of machinery - Electrical equipment of machines. 2016. Available: 			https://webstore.iec.ch/en/publication/26037 
4.	Sparkfun, “Servos Explained - SparkFun Electronics,” www.sparkfun.com. 		https://www.sparkfun.com/servos 
5.	“PID CONTROLLER Archives - The Engineering Concepts,” The Engineering Concepts, 	2018. https://www.theengineeringconcepts.com/tag/pid-controller/ (accessed Nov. 26, 	2024). 
6.	F. Zhang, “How Does Limit Switch Feedback Work in Actuators,” Progressive 		Automations, Mar.18, 2021. https://www.progressiveautomations.com/blogs/how-to/how-	does-limit-switch-feedback-work-in-actuators (accessed Nov. 26, 2024). 
7.	“Wheel Speed Calculator,” Calculator Academy. https://calculator.academy/wheel-	speed-	calculator/ 
8.	“In-Depth: Interface L298N DC Motor Driver Module with Arduino,” Last Minute 		Engineers, Nov.28, 2018. https://lastminuteengineers.com/l298n-dc-stepper-driver-	arduino-tutorial/#google_vignette 
9.	N. Bong, “Components of an Electric Linear Actuator,” Progressive Automations, Oct. 	26, 2021. https://www.progressiveautomations.com/blogs/products/inside-an-electric-	linear-actuator?srsltid=AfmBOopJH-								4XrJ9V0OS1Lk9yvIklYkLR6PysyYtZrjL_aBocRBR64l8M (accessed Nov. 26, 2024). 
10.	“3-pin pressure sensor,” Arduino Forum, Jul. 24, 2018. https://forum.arduino.cc/t/3-pin-	pressure-sensor/538150 
11.	“Arduino - Limit Switch | Arduino Tutorial,” Arduino Getting Started. 			https://arduinogetstarted.com/tutorials/arduino-limit-switch 
12.	“Speed vs Torque,” Power Electric. https://www.powerelectric.com/motor-blog/speed-vs-	torque 
13.	“Motor Calculations Calculating Mechanical Power Requirements.” Available: 	https://pages.mtu.edu/~wjendres/ProductRealization1Course/DC_Motor_Calculations.pdf 
14.	K. J. Astrom, “PID Control,” 2002. Available: 						https://www.cds.caltech.edu/~murray/courses/cds101/fa02/caltech/astrom-ch6.pdf
15. D. Power, “How To Calculate Battery Run Time,” Lithium ion Battery Manufacturer and Supplier in China-DNK Power. https://www.dnkpower.com/how-to-calculate-battery-run-time/
‌
16. “Voltage To Rpm Calculator - Calculator Academy,” Calculator Academy, Feb. 2024. https://calculator.academy/voltage-to-rpm-calculator/ (accessed Nov. 30, 2024).
‌
