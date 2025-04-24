
# Introduction


This experimental analysis revisits the conceptual design of our autonomous robot for the IEEE SECON 2025 hardware competition. The project's overarching goal was to design and build a robust and consistent robot capable of achieving a high score in the competition by reliably performing the core tasks of astral material collection, sorting, and placement within the allotted three minutes.

Based on the conceptual design and the outlined competition rules, the most critical requirements and success criteria directly impacting the project's have been split by subsystem for ease of testing.

# Motor Control
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
