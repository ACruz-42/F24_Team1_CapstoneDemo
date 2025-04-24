
# Introduction


This experimental analysis revisits the conceptual design of our autonomous robot for the IEEE SECON 2025 hardware competition. The project's overarching goal was to design and build a robust and consistent robot capable of achieving a high score in the competition by reliably performing the core tasks of astral material collection, sorting, and placement within the allotted three minutes.

Based on the conceptual design and the outlined competition rules, the most critical requirements and success criteria directly impacting the project's have been split by subsystem for ease of testing.

# Motor Control

## Relevant Critical Success Criteria:

1e.  The sorting and collecting motor systems for astral material shall be able to transfer and carry the load of at least one astral material at a time (3D printed icosahedrons, 48.2 g each for Geodinium).

1f.  The Cosmic Shipping Container motors shall be able to carry and support most of the load from a full container of astral material – 18 Geodinium for a total of 867.7 g.

## Experiment One: Astral Material Collection

1.  **Purpose and Justification**:
    
This is an experiment that combines constraints 1e and 1f for the purpose of testing the full flow of astral material through the robot. Constraint 1e addresses the need for the robot mechanisms to be able to transfer at least one astral material at a time from the point of collection to the point of the cosmic shipping container. The sweeper motor, auger motor, and sorting servo are involved in this process as the astral material makes its way toward the shipping containers. Constraint 1f addresses the need for the servos and linear actuators involved in the shipping container arm mechanism to be able to hold and fully support a full load of the heaviest configuration of astral material, which is all 18 Geodinium pieces (slightly heavier than the non-magnetic Nebulite). Therefore, this experiment fulfills both requests by properly simulating the flow of material through the robot and testing the support capabilities of the shipping container mechanism. Criteria of success will include the number of pieces that make it to the container and whether the container (after being picked up off the ground) stayed suspended or not. Also, completing a few trials with different material transfer sequences will help provide an overall picture of how the robot would perform given the unpredictable material placement. 

2.  **Detailed Procedure**:
    
The test involves keeping the robot stationary but providing power to the following motors/servos for material flow: the sweeper motor, the auger motor, the sorting servo, the linear actuator, and the shipping container arm servo. Run the function for grabbing the container via the serial input on the Arduino code until compression by the actuator is successful. Then, turn on the sweeper and auger, and move Geodinium material into the sweeper, one by one, in 10 second intervals. Continue this process until all 18 Geodinum have reached the container and then lift the robot off the ground to see if it can completely support the container when suspended.

![Material Flow Process](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/3c6ee68eb1e3d56e2a33b5806c98de7e203ab06d/Reports/Images%20and%20Sources/Experimental%20Analysis/Material_Flow_Process.jpg)

3.  **Expected Results**:
    
I would expect the robot to be fully capable of transferring the material and supporting the full load due to results from prior testing. However, there may be some slip on the hold of the shipping container, which would not be ideal as the container will already be positioned close to the ground. A complete success would be no slip, but I expect to at least see some movement.

4.  **Actual Results**:
    
The following were weights that were considered to determine the full maximum load of Geodinium:

Cosmic shipping container: 0.364 kg 


Robot Weight +  shipping container: 4.150 kg


Robot Weight: 3.786 kg


1 Nebulite: 0.010 kg


16 Total Nebulite: 0.16 kg


1 Geodinium: 0.040 kg 


18 Total Geodinium: 0.72 kg


18 Geodinium pieces were not available, so the total weight of 18 Geodinium (0.72 kg) was simulated by using the available 15 Geodinium plus 13 Nebulite. The same intended material flow process was still used, just for 28 total pieces instead of 18. 

![Container Weight](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/3c6ee68eb1e3d56e2a33b5806c98de7e203ab06d/Reports/Images%20and%20Sources/Experimental%20Analysis/Container_Weight.jpg)

![Robot Plus Container Far](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/3c6ee68eb1e3d56e2a33b5806c98de7e203ab06d/Reports/Images%20and%20Sources/Experimental%20Analysis/Robot_Plus_Container_Far.jpg)

![Full Geodinium Load Equivalent](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/3c6ee68eb1e3d56e2a33b5806c98de7e203ab06d/Reports/Images%20and%20Sources/Experimental%20Analysis/Full_Geodinium_Load_Equivalent.jpg)

| Trial | Order of Material Entry | Number of Material Successfully Transferred (out of 28) | Did Cosmic Shipping Container Remain Supported? |
| :-- | :-------------------------- | :------------------------------ | :----------------------- |
| 1   | Nebulite, then Geodinium, then Geodinium glue pieces | 26                      | Yes - lift robot test worked               |
| 2   | Alternating until Geodinium only, then glue pieces | 24                      | Yes - lift robot test worked               |
| 3   | Geodinium, then Nebulite, then glue pieces | 12                      | Yes - lift robot test worked               |
| 4   | Geodinium, then Nebulite, then glue pieces | 26                      | Yes - lift robot test worked               |

5.  **Interpretation and Conclusions**:
    
- Provide a detailed analysis explaining the significance of the results.

Trial 1 successfully transferred 26 out of the 28 attempted pieces, and when the lift test was attempted, the robot successfully maintained grip on the cosmic shipping container. This means that the robot has the capability to support the weight of nearly a full load of Geodinium pieces, which is the maximum weight configuration. The two that did not make it were stuck on the sorting station chute. These pieces were the last to go through the robot, which may mean the backend of material flow will be less successful.

Trial 2 was still mostly successful with 24 out of 28 transferred. The last 4 that were left to transfer ended up getting stuck on the sorting station platform. This group was composed of two Nebulite and the same two pieces that got stuck on Trial 1, which have an excess of glue on them. The robot did successfully maintain a grip on the cosmic shipping container. This trial continues to support the theory that the last pieces that go through the sorting station will not make it to the shipping container. 

Trial 3 was not successful in material flow, but it did maintain grip on the shipping container. The material pieces were almost halfway through being transferred when an accumulation of material began to build up on the sorting station. Like Trial 2, this build up consisted of 4 pieces. Unlike Trial 2, all 4 were standard Nebulite pieces, and the build up was backed up toward the station entrance rather than being more spread out, which occurred in Trial 2. The build up was followed by another piece that got near the top but couldn’t get to the entrance and caused the auger motor to stall. It seems that the light weight of the Nebulite may have helped cause this buildup, as all four pieces involved were Nebulite. 

A fourth trial was tested in order to provide a larger sample size for the sequence of material that caused the most error. In the same configuration of all Geodinium, followed by all Nebulite, and finally the two remaining glue pieces, every piece was transferred except for the glue pieces. These two were then manually inserted into the container just to confirm the lift test for the full load, and the load was still successfully lifted. 

- State whether results matched your expectations and explain any discrepancies.

These results mostly match my expectations, as most of the material was transferred smoothly and there was very little slip on the container hold. However, the two pieces that did not make it in Trial 1 need to be addressed. These pieces had a significant amount of glue on their exterior, which likely made transport more difficult through the increased friction. These pieces were also the last two. One observation for all trials that I had was that most of the time, material would get stuck on the servo chute platform, but would be pushed into the container by the next one after it. Therefore, if there is a need to push the material stuck on the chute, then it may be unlikely for the robot to transfer every material piece to the respective container. Just all of the ones that lead up to the last couple would be the most reliable. Also, if there is a long sequence of lighter pieces, then a buildup failure will be more likely to occur due to less weight forcing the pieces down the chute.

- When you have complete all of the experiments: clearly summarize whether your experiments demonstrated that your project meets the original success criteria outlined in your conceptual design. If success criteria were not met, discuss the reasons and outline steps for improvement.



# Sensors

## Critical Aspects of Sensors

Specifications:
1.	The robot's distance measurement sensor shall be able to find the walls of the game field and the cave.
2.	The robot's light detector shall be able to detect when the start LED turns on.
3.	The robot's magnetic sensors shall be able to detect the magnetic fields of the Geodinium.
4.	All of the robot's sensors shall be able to work effectively despite background interference in the competition environment.

Constraints:
1.	The robot shall know its current position.
2.	The magnetic sensor shall provide a signal that is larger than the resolution of the Arduino's Analog-to-Digital Converter.
3.	The light detector shall provide a signal visible through the background noise.

The sensor subsystem needs to know the robot’s location to avoid walls and stay on the game field. The subsystem helps gain points by sorting materials and using the referee controlled starting LED. These sensors need to work in a noisy environment and provide readable signals.

## Sensors Experimental Overview
The sensors subsystem has 3 main components. There is the Optical Tracking and Odometry Sensor (OTOS), photoresistors, and hall effects. Each of these components will be tested on the robot to verify that it works properly with the total system.

## Purpose and Justification:
### OTOS
The accuracy of the linear and angular displacements was measured. By knowing the accuracy of the OTOS, the navigation can set narrower tolerances on the area of the destination point. This will allow the robot to travel to more precise locations. If the robot does not know its current location well enough, it will fail. A different method available is to use distance sensors.

### Hall Effect
The range and noise of the hall effect sensors were measured. This determines the tolerance for detecting magnetic material. If the noise is too large and the signal is too small, the signal will be lost. If the robot cannot detect magnetic materials, it will not sort them. This is alright as the robot will still score points for putting materials in the wrong bin.

### Photoresistor
The number of accurate start LED detections was counted. This would determine if there were any false readings and how often they would happen. This experiment would find if the robot would ever have a false start or not start. If the robot does not start successfully, a different start method would need to be built. A long timer was used before, but a button or switch would be the best.

## Detailed Procedure:
### OTOS
The OTOS was left attached to the robot. If there was any issue with how level the OTOS was, it would be discovered and fixed. Since the OTOS was tested on the robot, the drive wheels were removed to reduce noise from the forced spin of the motors. Data is taken with the Jetson Nano. The starting point is always set as (0, 0, 0) for X, Y, and heading.  The ending point is the same. Only the final position point is recorded.
For the linear displacement experiment, the robot was rolled on neutral wheels on a flat surface against a flat object. The robot was moved forward 105 inches by hand, back to the start and repeated 3 times in a single run for a total of 630 inches. The robot had the same starting and ending position to easily compare the drift. The choice of total distance was arbitrary but was suggested by the manufacturer to be more than 100 inches to see significant drift. The larger the distance, the easier it was to see the drift and measure its offset. The robot was not rotated when the linear displacement was tested.

For the angular displacement experiment, the robot was spun on neutral wheels on a flat surface. It would start against a flat object and then was positioned back on the same flat object, so it had the same starting and ending angle. The robot was spun counterclockwise ten times by hand in a single run for a total of 3600 degrees. The choice of total angular rotation was suggested by the manufacturer to be at least 3600 degrees to see significant drift. The larger the distance, the easier it was to see the drift and measure its offset.

The image below shows the OTOS attached to the bottom of the robot.

<img src=https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/a7926c034d774467a321dac6adb84d7c4ea20ab2/Reports/Images%20and%20Sources/Experimental%20Analysis/attached_OTOS.jpg  alt="Attached_OTOS" width="50%"/>

### Hall Effect
The hall effects were left attached to the robot. There are three hall effects used on the robot. They are situated close together, near the exit of the auger. They are each oriented in a different axis to detect orthogonal magnetic fields. One of the sensors will have material slide over it, while the other two are placed on a nearby wall with materials about 1 cm away. Each sensor is tested to check the capability of its data. Power is applied to the robot. The auger is turned on, and data is taken with the Arduino Mega.

For the experiment, each of the hall effects set points were measured. To find the setpoint, an average of the voltage with no magnetic field near the sensors was measured with 100 data points. After measuring the setpoint, the maximum and minimum are measured for each hall effect. To measure the maximum and minimum, a timer is set for 15 seconds in the Arduino Mega. At the end of the 15 seconds, the maximum and minimum measured by the hall effects is recorded by the Arduino Mega. During the 15 seconds, the auger turned on, and then a single material travels up the auger and past the hall effects. This way, each run corresponds to a single magnetic material traveling past the hall effects. At the end of each run, the average set point for the last 100 measurements is also recorded. This average is long after the material had passed by the hall effects, so it will not include any of the data from the material passing by. Lastly, two extra runs are taken to see the background noise.

The two images below show the hall effects and a magnetic material next to them. The hall effect by itself is number 1 in the following tables and hall effect X in the Arduino code. The bottom hall effect of the two together is number 2 in the following tables and hall effect Y in the Arduino code. The top hall effect of the two together is number 3 in the following tables and hall effect Z in the Arduino code.

<img src=https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/a7926c034d774467a321dac6adb84d7c4ea20ab2/Reports/Images%20and%20Sources/Experimental%20Analysis/attached_Hall_Effects_drawn.jpg alt="Attached_Hall_Effects_with_Drawing" width="49%"/> <img src=https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/004042acc7b07eae4a1d0b5fc1c5e7ef025c2119/Reports/Images%20and%20Sources/Experimental%20Analysis/magnetic_material_hall_effect_sensor.jpg alt="Attached_Hall_Effects_with_Magnetic_Material" width="49%"/>

### Photoresistors
The photoresistors were left attached to the robot. There are three photoresistors. Two are on top of the robot and detect the ambient light level. One is at the back of the robot and detects the start LED. To determine if the start LED is on, the light level detected by the start LED photoresistor is compared to the light level detected by the ambient light photoresistors. Power is applied to the robot. Data is taken with the Arduino Mega.

For the experiment, the robot is placed by the start LED. The LED is turned on and the detection status is determined. If the start LED photoresistor reads higher than the ambient light photoresistors, then the detection status is on. If the start LED photoresistor reads lower than the ambient light photoresistors, then the detection status is off.
The first image below shows the ambient light sensors. The second image below shows the start LED light sensor.

<img src=https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/004042acc7b07eae4a1d0b5fc1c5e7ef025c2119/Reports/Images%20and%20Sources/Experimental%20Analysis/ambient_light_detector.jpg alt="Attached_Ambient_Light_Sensors" width="49%"/> <img src=https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/004042acc7b07eae4a1d0b5fc1c5e7ef025c2119/Reports/Images%20and%20Sources/Experimental%20Analysis/start_LED_detector.jpg alt="Attached_Start_LED_Light_Sensor" width="49%"/>

## Expected Results:
It is expected that the OTOS has an angular tolerance of less than 1% of total rotation and has a linear tolerance of less than 1% of total distance. It is expected that the hall effects will have a setpoint near 2.5 V. The signal from the magnetic materials will be greater than 0.1 V and the noise will be near 0.01 V. The photoresistors will detect the status of the start LED correctly every time.

## Actual Results:
### OTOS
The table below is for the angular displacement experiment. The percentage offset is the offset divided by the total rotation of 3600 degrees.

|Run Number|Angular Offset (Degrees)|Angular Percentage Offset|
|:-|:-|:-|
|1|0.0831|0.0023|
|2|1.8034|0.0501|
|3|-1.0072|-0.0280|
|4|-1.6482|-0.0458|
|5|-0.4374|-0.0122|
|6|1.2062|0.0335|

The table below is for the linear displacement experiment. The percentage offset is the offset divided by the total distance of 630 inches.

|Run Number|Linear Offset (Inches)|Linear Percentage Offset|
|:-|:-|:-|
|1|-0.7329|-0.1163|
|2|0.4085|0.0648|
|3|0.0481|0.0076|
|4|-0.4085|-0.0648|
|5|-1.2856|-0.2041|
|6|0.5767|0.0915|

### Hall Effects
The table below shows the setpoint for each hall effect before any runs are started.

|Hall Effect Number|Set Point (Volts)|
|:-|:-|
|1|2.486|
|2|2.565|
|3|2.637|

The table below shows the maximum and minimum for each run for each hall effect.

|Run Number|Max Hall Effect 1 (Volts)|Min Hall Effect 1 (Volts)|Max Hall Effect 2 (Volts)|Min Hall Effect 2 (Volts)|Max Hall Effect 3 (Volts)|Min Hall Effect 3 (Volts)|
|:-|:-|:-|:-|:-|:-|:-|
|1|2.937|2.292|3.084|2.576|3.094|0.547|
|2|4.072|3.045|3.817|3.157|3.988|3.104|
|3|3.935|2.028|4.022|2.537|4.101|0.640|
|4|4.233|3.084|3.622|3.187|3.661|3.216|
|5|3.431|2.669|3.558|2.810|3.715|1.931|
|6|3.226|1.124|3.089|2.546|3.162|0.547|
|7|3.514|2.151|3.210|2.649|3.542|2.678|
|8|3.675|2.141|3.226|2.649|3.729|2.678|
|9|3.358|2.214|3.118|2.664|3.372|2.717|
|10|3.319|2.180|3.069|2.625|3.333|2.708|
|11|3.187|2.199|3.065|2.542|3.133|2.727|
|12|3.192|2.243|3.065|2.674|3.138|2.698|

The table below shows the set points after each run.

|Run Number|Set Point Hall Effect 1 (Volts)| Set Point Hall Effect 2 (Volts)| Set Point Hall Effect 3 (Volts)|
|:-|:-|:-|:-|
|1|2.721|2.937|2.910|
|2|3.513|3.606|3.689|
|3|3.260|3.344|3.380|
|4|3.246|3.328|3.407|
|5|3.280|3.367|3.443|
|6|2.989|2.948|3.017|
|7|2.989|2.947|3.018|
|8|2.989|2.947|3.017|
|9|2.992|2.950|3.021|
|10|2.993|2.950|3.020|
|11|2.994|2.951|3.021|
|12|2.994|2.950|3.021|

### Photoresistors
The table below shows whether the photoresistor successfully detected the start LED status.

|Run Number|Success or Failure|
|:-|:-|
|1|Success|
|2|Success|
|3|Success|
|4|Success|
|5|Success|
|6|Success|
|7|Success|
|8|Success|
|9|Success|
|10|Success|

## Interpretation and Conclusions:
### OTOS
The OTOS can successfully measure the location of the robot’s current position. The expected tolerance was less than 1% in angular displacement and less than 1% in linear displacement. The OTOS measured less than 0.1% offset from total rotation in all runs, with the worst being about 0.05% percentage offset. The OTOS measured less than 1% offset from total distance in all runs, with the worst being about 0.2% percentage offset. The OTOS met the success criteria and expected results.

### Photoresistors
The photoresistors successfully measured the status of the start LED ten out of ten trials. The success criteria were met.

### Hall Effects
12 runs are taken for the hall effects. The set point, maximum, and minimum are measured for each hall effect for each run. Before any data was taken, the original set points were measured, which are shown in the first table under Hall Effects under Actual Results. Runs 11 and 12 are background runs to help determine the noise that the sensors see.

The set point changed by a large margin (about 0.35 V) between runs 5 and 6. This is due to the battery being replaced between these runs. Before run 5, the input voltage was about 10.8 volts. After run 5, the input voltage was about 11.8 volts. The voltage of the rail powering the hall effects was not measured, but it is controlled by a DC-DC converter. The power board is presented at this link: <https://github.com/TnTech-ECE/Spring2024-Base-Modular-Robot/blob/7f402b8c3b09a4edfa15642721f54641bdb7cd87/Documentation/Signoffs/LukeChapman-Signoff-Power-Distribution.md>. Doing some testing with the schematic shows the voltage rail does shift as the input power shifts.

To account for the shifting power supply and set point, each run has its own set point for comparing data. The table below shows the difference between the maximum or minimum and the set point for each run and hall effect. The absolute value is taken, since the difference of the minimum will be negative.

|Run Number|Max Dif Hall 1 (Volts)|Min Dif Hall 1 (Volts)|Max Dif Hall 2 (Volts)|Min Dif Hall 2 (Volts)|Max Dif Hall 3 (Volts)|Min Dif Hall 3 (Volts)|
|:-|:-|:-|:-|:-|:-|:-|
|1|0.216|0.429|0.147|0.361|0.184|2.363|
|2|0.559|0.468|0.211|0.449|0.299|0.585|
|3|0.675|1.232|0.678|0.807|0.721|2.740|
|4|0.987|0.162|0.294|0.141|0.254|0.191|
|5|0.151|0.611|0.191|0.557|0.272|1.512|
|6|0.237|1.865|0.141|0.402|0.145|2.470|
|7|0.525|0.838|0.263|0.298|0.524|0.340|
|8|0.686|0.848|0.279|0.298|0.712|0.339|
|9|0.366|0.778|0.168|0.286|0.351|0.304|
|10|0.326|0.813|0.119|0.325|0.313|0.312|
|11|0.193|0.795|0.114|0.409|0.112|0.294|
|12|0.198|0.751|0.115|0.276|0.117|0.323|

The background is then subtracted from the data above to remove the noise levels measured in runs 11 and 12. The larger of the two noise levels are subtracted, because it gives a tighter tolerance on the hall effects and leaves less room for false positives. Between runs 11 and 12, they give close values except for minimum difference for hall effect 2. In the following table, the bold numbers are greater than 0.1 V, and the bold italic numbers are above 0.2 V. Overall, the thresholds for the sensors can be derived from this table. 

|Run Number|Max Thresh Hall 1 (Volts)|Min Thresh Hall 1 (Volts)|Max Thresh Hall 2 (Volts)|Min Thresh Hall 2 (Volts)|Max Thresh Hall 3 (Volts)|Min Thresh Hall 3 (Volts)|
|:-|:-|:-|:-|:-|:-|:-|
|1|0.018|-0.366|0.032|-0.048|0.067|***2.040***|
|2|***0.361***|-0.327|0.096|0.040|**0.182**|***0.262***|
|3|***0.477***|***0.437***|***0.563***|***0.398***|***0.604***|*2.417***|
|4|***0.789***|-0.633|**0.179**|-0.268|**0.137**|-0.132|
|5|-0.047|-0.184|0.076|**0.148**|**0.155**|***1.189***|
|6|0.039|***1.070***|0.026|-0.007|0.028|***2.147***|
|7|***0.327***|0.043|**0.148**|-0.111|***0.407***|0.017|
|8|***0.488***|0.053|**0.164**|-0.111|***0.595***|0.016|
|9|**0.168**|-0.017|0.053|-0.123|***0.234***|-0.019|
|10|**0.128**|0.018|0.004|-0.084|**0.196**|-0.011|

<img src=https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/dc8cb7584cbbff4bca22e3ca8325016be6d87f9e/Reports/Images%20and%20Sources/Experimental%20Analysis/Full_Table_Hall_Effects.png alt="Full_Hall_Effects_Graph" width="50%"/>

<img src=https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/dc8cb7584cbbff4bca22e3ca8325016be6d87f9e/Reports/Images%20and%20Sources/Experimental%20Analysis/Partial_Graph_Hall_Effects.png alt="Zoomed_Hall_Effects_Graph" width="50%"/>

This last table and graphs show how well each sensor sees magnetic material. The first graph shows the data from the last table grouped by run number and then color coded by sensor type. The second graph shows the same data but zoomed in to better see the thresholds. A threshold of 0.1 V would be enough, but a threshold of 0.2 V can be used as well but barely misses run 10. Higher than 0.2 V would miss runs 9 and 10. Run 3 looks like an anomaly since all values are past the threshold. The minimums for each of the sensors are farther away from the set point than the maximums for an unknown reason. A method of a moving average or set point and background subtraction could be implemented to make the data usable on an operational robot. However, it was not implemented in this project due to time constraints. Lastly, the noise values were much higher than expected. When tested on their own, hall effects have very low noise. However, all the components working at the same time on the robot caused large amounts of noise. The signal is still visible through the noise and above 0.1 V. Overall, the hall effects are successful at measuring the magnetic material, but it was not fully implemented on the final design.

# Camera
For each documented experiment, you must include:

1.  **Purpose and Justification**:
    
    -   Explain why the experiment was designed, and how it relates to your critical success criteria.
2.  **Detailed Procedure**:
    
    -   Outline clearly the methods used, ensuring another team could reproduce your experiment.
3.  **Expected Results**:
    
    -   State your initial hypothesis or expectations clearly before conducting experiments.
4.  **Actual Results**:
    
    -   Present data collected during the experiments in an organized, easy-to-interpret format (tables, graphs, charts).
5.  **Interpretation and Conclusions**:
    
    -   Provide a detailed analysis explaining the significance of the results.
    -   State whether results matched your expectations and explain any discrepancies.

When you have complete all of the experiments: clearly summarize whether your experiments demonstrated that your project meets the original success criteria outlined in your conceptual design. If success criteria were not met, discuss the reasons and outline steps for improvement.
# Navigation

## Relevant Critical Success Criteria:
1.  **The Robot shall act autonomously** (Specification 1 [1]). This was necessary for compliance with Game Manual 1.
2.  **The Robot shall be able to navigate to and position itself for the following tasks** (Specification 2 [1]). This was necessary to maximize potential points. 
		I.  Navigate out of Landing Pad (i) 
	II. Navigate within 3 seconds of Start LED (ii) 
	III. Navigating into the cave (iii) 
	IV. Navigate to correct shipping pad (v) 
	V. Navigate to and allow for placement of team beacon (ix)
3.  **The Robot shall stay on the game field** (Specification 5 [1]). This was necessary for the safety of the team and all IEEE SECON staff members.
4.  **The Robot shall cease all operation after three minute timer is done** (Specification 10 [1]). This was necessary for the safety of the team and all IEEE SECON staff members.
5.  **The Robot shall immediately cease operations upon the usage of the emergency stop button** (Specification 7 [1]). This was necessary for the safety of the team and all IEEE SECON staff members.

As most of these criteria are actions the robot can take sequentially and are not mutually exclusive, two experiments were designed. In brief, the two experiments would sequentially run through the tasks as described in critical success criterion two (**The Robot shall be able to navigate to and position itself for the following tasks [...]**). In experiment one, the emergency stop button was pressed after the completion of the tasks described in critical success criterion two. In experiment two, the robot was instead left to rotate in circles after completion of tasks described in critical success criterion two until the three minute timer expired so as to ensure timely cessation of operations. Each experiment would be run three times. Additionally, it should be noted that the programming of the robot was changed before either experiment, as the robot performed accurately when used at the IEEE SECON competition fields or on the Tennessee Tech Capstone Lab practice field but yielded inaccurate runs when moved between the two. In particular, the coordinates used needed to be adjusted (by a factor of a few inches). It is also worth noting that during the runs at the IEEE SECON competition field, the robot abided by the success criteria outlined in this subsection except for success criterion four (**The Robot shall cease all operation after three minute timer is done**). The robot's operation never went over three minutes, and so success criterion four was simply never tested.

## Experiment One: Navigation Sequence and Emergency Stop

### Purpose and Justification:

This experiment was designed to test the robot's ability to execute a critical sequence of navigation tasks required for scoring points in the competition, as outlined in **Critical Success Criterion 2** (**The Robot shall be able to navigate to and position itself for the following tasks [...]**). Simultaneously, it served to verify the emergency stop function mandated by **Critical Success Criterion 5** (**The Robot shall immediately cease operations upon the usage of the emergency stop button**). Successful completion of this experiment would demonstrate the robot's capability to traverse key areas of the field and confirm the reliable function of the emergency stop.

### Detailed Procedure:

The experiment was conducted on a practice field configured by our attached mechanical engineering capstone team to replicate the dimensions and key features of the IEEE SECON competition arena. Before starting this experiment, the robot's navigation code was updated based on observations from previous testing on different fields, adjusting internal coordinate mapping to improve positional accuracy on the current practice field setup.

Each run followed this procedure:
1. The python program was started.
1. The robot was placed on the designated landing pad.
2. A hand was waved in front of the front photoresistors (simulating and functionally equivalent a light shining on the rear photoresistor).
3. The robot was tasked with executing the following sequential navigation maneuvers:
    * Navigate autonomously out of the Landing Pad.
    * Attempt to navigate within 3 seconds of a simulated Start LED signal (representing the rapid initial movement requirement).
    *  Navigate to a position suitable for deploying the team beacon.
    * Navigate towards and enter the cave area.
    * Navigate from the cave area to a pre-defined location indicating the correct shipping pad zone.
4. Immediately after the robot completed the final navigation task in the sequence (positioning for beacon placement), the emergency stop button on the robot was pressed.
5. The robot's response was observed to ensure all movement and active components ceased immediately.

This procedure was repeated for a total of three independent runs to assess consistency.

### Expected Results:

Based on the performance at the IEEE SECON competition and coordinate adjustments made to the navigation code prior to this experiment, we expected the robot to successfully perform the entire sequence of navigation tasks in each run, reaching the intended areas on the field. Furthermore, given the hitherto reliable nature of the emergency stop as a safety feature, we hypothesized that activating the button would result in an immediate and complete cessation of all robot functions in all three runs.

### Actual Results:

The results for the three runs of Experiment One are presented below:

| Run | Navigate out of Landing Pad | Navigate within 3s of Start LED | Navigating into the Cave | Navigate to Shipping Pad | Navigate to Beacon Position | Emergency Stop Functionality |
| :-- | :-------------------------- | :------------------------------ | :----------------------- | :----------------------- | :-------------------------- | :--------------------------- |
| 1   | Successful                  | Successful                      | Successful               | Successful               | Successful                  | Immediate Cessation          |
| 2   | Successful                  | Successful                      | Successful               | Successful               | Successful                  | Immediate Cessation          |
| 3   | Successful                  | Successful                      | Successful               | Successful               | Successful                  | Immediate Cessation          |


In all three runs, the robot successfully navigated through the defined sequence of points on the practice field. Upon activation of the emergency stop button after the final navigation task, the robot immediately halted all movement and operations in every instance.

### Interpretation and Conclusions:

The actual results of Experiment One matched our expectations. The consistent successful completion of the navigation sequence across all runs validates that the navigation subsystem is capable of guiding the robot through key areas of the competition field as required by Critical Success Criterion 2. The immediate and reliable cessation of operation upon pressing the emergency stop button in every run confirms the proper functioning and critical safety compliance of this feature, satisfying Critical Success Criterion 5. 

## Experiment Two: Navigation Sequence and 3-Minute Timer Cessation

### Purpose and Justification:

This experiment was designed to evaluate the robot's ability to perform the same critical sequence of navigation tasks as in experiment one and, more importantly, to test adherence to **Critical Success Criterion 4** (**The Robot shall cease all operation after three minute timer is done**). This criterion had not been explicitly tested under controlled conditions in previous trials where the robot completed tasks before the time limit. Ensuring the robot automatically and reliably stops after the 3-minute match duration is crucial for competition compliance and safety.

### Detailed Procedure:

Experiment Two was conducted on the same configured practice field as Experiment One, utilizing the robot with the same pre-experiment navigation code adjustments.

Each run followed this procedure:
1. The python program was started.
1. The robot was placed on the designated landing pad.
2. A hand was waved in front of the front photoresistors (simulating and functionally equivalent a light shining on the rear photoresistor).
3. The robot was tasked with executing the following sequential navigation maneuvers:
    * Navigate autonomously out of the Landing Pad.
    * Attempt to navigate within 3 seconds of a simulated Start LED signal (representing the rapid initial movement requirement).
    *  Navigate to a position suitable for deploying the team beacon.
    * Navigate towards and enter the cave area.
    * Navigate from the cave area to a pre-defined location indicating the correct shipping pad zone.
4. Immediately after the robot completed the final navigation task in the sequence (positioning for beacon placement), the emergency stop button on the robot was pressed.
4. After successfully completing the final navigation task in the sequence, the robot was programmed to perform a simple, non-scoring action (specifically, rotating in place) and was allowed to continue operating without external intervention until its internal 3-minute match timer expired.
5. The robot's state was observed to confirm that all movement and active components ceased precisely at the 3-minute mark.

This procedure was repeated for a total of three independent runs.

### Expected Results:

Based on the successful navigation performance observed in Experiment One and the implementation of an internal timer designed to enforce the 3-minute limit, we expected the robot to successfully complete the defined navigation sequence in all three runs. Crucially, we hypothesized that the robot would autonomously cease all operations (including the programmed rotation) exactly when the 3-minute timer elapsed in every run, thereby fulfilling Critical Success Criterion 4 which had not been definitively validated before.

### Actual Results:

The results for the three runs of Experiment Two are presented below:

| Run | Navigate out of Landing Pad | Navigate within 3s of Start LED | Navigating into the Cave | Navigate to Shipping Pad | Navigate to Beacon Position | Cessation time |
| :-- | :-------------------------- | :------------------------------ | :----------------------- | :----------------------- | :-------------------------- | :-------------------------- |
| 1   | Successful                  | Successful                      | Failure               | Successful               | Successful                  | 2:55        |
| 2   | Successful                  | Successful                      | Successful               | Successful               | Successful                         |2:55
| 3   | Successful                  | Successful                      | Successful               | Successful               | Successful                  | 2:56        |

In two runs, the robot successfully navigated through the defined sequence of points on the practice field. After completing the sequence, the robot continued its programmed action (rotation) until the 3-minute mark was reached, at which point it successfully and automatically ceased all operations in every instance. In the first run, the side of the robot clipped the entrance of the cave and needed to be manually assisted inside. It's possible that other runs may have had issues had the robot needed to pick up the shipping containers (as the shipping containers add about an extra inch or two to the width of the robot), but this was not a success criterion, and is simply noted for posterity.

### Interpretation and Conclusions:

The results of Experiment Two nearly aligned with our expectations. The almost consistent successful navigation sequence implies that the overall function of the navigation subsystem is working as intended, but perhaps needed some tweaks to make the robot fully autonomous. More importantly, the successful and timely cessation of all robot operations at the 3-minute mark in every run definitively validates Critical Success Criterion 4. This experiment confirms that the robot's state machine correctly 
 
# Conclusion
When you have complete all of the experiments: clearly summarize whether your experiments demonstrated that your project meets the original success criteria outlined in your conceptual design. If success criteria were not met, discuss the reasons and outline steps for improvement.

# Statement of Contributions
Alex Cruz - Navigation, Introduction, Conclusion.
