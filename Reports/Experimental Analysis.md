
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
