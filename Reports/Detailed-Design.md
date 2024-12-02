# Detailed Design for Object and Line Detetion
## Function of Subsystem
The function of this subsystem is to provide the location of the astral materials, lines, and walls on the game field, as well as read the april tags and then provide this information to Master Control, so that Master Control can plot an effecient path to pick up all astral material, as well as sort the shipping containers at the end of the match, while unsuring the robot does not collide with anything from the front.

## Specifications and Constraints 
### Specifications
1. The robot shall act autonomously [S1].
2. The camera shall detect the Nebulite [S2-vii].
3. The camera shall detect the Geodinium [S2-viii].
4. The robot shall be able to detect the walls of the arena, walls of the cave, and cave entrance. Rule S03 states that if the robot causes field damage, the team will be penalized. Detecting walls stops the robot from causing damage by moving into it. The camera will be the only sensor on the front and will need to do the listed objectives [S4].
5. The camera shall read April Tags to help with Specifications 1, 2-v, 2-vii, 2-viii, and 2-ix [C1].

These Specifications stem from the the game rules and are intended to set into strict goals the methods by which the robot will score points and therefore do well in the competition. 

### Constraints
1. The camera will be able to work in both light and dark conditions
2. In order to keep costs down the robot will only have 1 RGBD camera
3. The robot will be able detect the white lines on the game field

Constraint 1 stems from the fact that the game field will have a dark cave, which will contain astral material, and as such the robot will need to enter the cave and search for astral material.
Constraint 2 stems from socio-economic concerns, the camera will comprise roughly 15% of the robots total budget, and as such it will be advantageous if only one is used to keep costs down and allow more room in the budget for other sybsystems. 
Constraint 3 stems from the robots need to use the white lines to navigate the game field as well as score points by sorting the filled shipping containers.

## Proposed Solution
In order to meet the specifications and constraints the robot will need an RGBD camera, this camera will be able to pick out the RGB values of the astral matrials and lines on the game field against the dark background of the game field, this will help meet Specifications 2 and 3 and contraint 3.
The camera will also be able to pick out the depth, or distance from the camera, of the astral material, the shipping containers, and the walls of the game field, this will help meet Specifications 1, 2, and 3.
The information from the camera and the other sensors as on the robot will be used by an object detection algorithm to the robot where the objects are on the game field, mainly the astral material, walls, and shipping containers, this will help meet Specifications 1, 2, 3, and 4.
The image data from the camera will also be used by a line detection algorithm to find the white lines on the game field to assist in navigation and sorting of the shipping containers, this will help meet constraint 3.
Finally the image data will undergo an image processing algorithm which will allow it to read the april tags, much in the same way a phone can read a qr code from a picture or screenshot, this will help meet specification 5.

## Interface with Other Systems
The camera will connect to the Jetson nano using a USB-C 3.1 Gen 1, this connection will transfer the image data, which includes including RGB values and depth values, the camera will also be powered through this connection and will take a 5V supply[2]. 
The primary responisibility of the camera will be to find the astral material on the game field and then send its location to Navigation and Master Control for the purpose of finding an effecient path to pick up all astral material.
The next responsibility of the camera will be to find the white lines on the game field and then send their locations to Navigation and Master Control for the purposes of navigation and sorting the shipping containers. 
The camera will also be responsible for reading the april tags and sending their values to Master Control for the purpose of sorting the shipping containers into the correct telemetry zones. 
The camera will also aid in locating the walls of the game field, and will be responsible for making sure that the robot does not crash into anything from the front.
Since both Navigation and Master Control and the detection and image processing algorithms will all be housed on the Jetson Nano so all communication betweeen these algorithms will be done internally.

## Buildable Schematic
![Buildable schematic](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/Object-and-Line-Detection-Edits/Reports/Photos/Buildable%20Diagram.svg)

## FlowChart
A quick note for the flowchart, the robot will start and then it will go about the tasks shown in the flow chart, these tasks will continue until some kind of interrupt occurs, either all astral material will be collected, or the robot will run out of time and will need to sort the shipping containers without collecting all astral material.
![Operational Flowchart](https://github.com/ACruz-42/F24_Team1_CapstoneDemo/blob/Object-and-Line-Detection-Edits/Reports/Photos/OperationalFlowchartObjectAndline.drawio.svg)

## Analysis
### The Camera
The camera will be an Intel Realsense D435 RGBD camera, this camera was chosen for its wide FOV of 87° × 58°, as well as its depth range of .3 m to 3 m. Also this camera uses stereoscopic depth technology which is needed as infrared projection technology cannot be used in conjuction with the infrared camera that is part of the game field in the cave. The camera will take a 5V voltage supply that will be transfered through a USB-C 3.1 Gen 1 connection which will also be used to transfer the image data to the Jetson Nano. This connection has a maximum information transfer rate of 5 GB per second. The cameras depth values will be greater than 98% accurate at 2 meters. The camera will send both the RGB values of the picture as well as the depth values of the picture to the Jetson Nano where these values will be used by various algorithms as described below[2].

### Object Detection Algorithm
The object detection algorithm will work similarly to many generic object detection algorithms, in that it will take an image and will scan through the pixels to find specific patterns and differences is RGB values, however it will be much simpler than most object detection values as we will be mainly trying to detect one type of object with a known size and more importantly a known RGB value and a known shape, which will be against a dark background.
This will make it easy to pick out the astral material as all the algorithm will have to do is search for that specific RGB value and the seperate each little "ball" of that color, then the algorithm will go to the depth data of the image and look at the place where it found the propor color and find the depth of that area.
Since the camera will be at a fixed place on the robot we will be able define a constant axis at the front of the robot, then using the values of RGB and depth we will be able find the angle of the astral material compared to the axis at the front of the robot and then use the depth to find the distance from the axis which will give each astral material a polar coordinate value. 
This polar coordinate value can then be transformed into cartesian coordinates on the robots internal grid system.[3]
One valuable tool that will help with this process is openCV, which is a large open source computer vision and machine learning software library[5]. Using libraries from openCV will simplify the above process greatly as there are already useful libraries written that can search for specific monochromatic colors like the ones we will need for the astral material[6].

### Line Detection Algorithm 
The line detection algorithm will work much the same to the object detection algorithm in that it will take an image as input and will use a simplified version of a generic line detection algorithm to pick out the white lines against the dark background of the game field.
Since the lines on the game field are in fixed positions the robot can use the shape and composition of these lines to determine where they belong on the game field and therefore where it is in comparison to them.
Since the lines on the game field are in fixed positions the robot can use the surrounding context such as walls to determine how far away the lines are, or in other words, the depth of the lines. Similar to with object detection we can make use of openCV where preexisting libraries exist using methods such as the hough transform to find all the lines in an image[1]. 

### Image Processing for April Tags
The image processing algorithm for the april tags will activate once Master Control sends a signal that the robot is in position, it will then scan the image much in the same way the the detection algorithms did, except it will be looking for the april tags, which should be easy to locate as it will be a box of white and black.
Once the april tag has been located it will look at the specific pixels and decode them into a number, much like a QR code scanner.
it will then send the value to Master Control along with the locations of the lines from the line detection algorithm to tell the master control which telemetry zone to put the shipping containers in[4]. As april tags are becoming more commonly used in robotics there are also preexisting libraries that can aid in reading them, that will yet again come from openCV[7]. 

### Image Processing for the Walls
The image processing for the walls is a simple algorithm that will measure the distance between the robot and the walls and will alert the robot if it gets too close to a wall. Due to the way the collection system for the astral material is being designed the camera will be the only forward facing sensor and as such will be responsible for making sure the robot does not collide with anything from the front.

## Ethics 
The camera will come as a fully built and developed device and as such full credit for camera design will be given to those responsible, the camera will also have an infrared projector which will aid in depth sensing capabilities, this infrared projector is safe for use in close proximities to humans. 
The detection and image processing algorithms will also be simplified versions of generic algorithms and as such proper credit will be given for any code or methods that are taken from other sources.
Finally the subsystem will have user manual explaining the subsystems function and operation in a way that others can clearly understand the operation of the subsystem.

## BOM
| Manufacturer   | Part Number   | Distributor   | Part Number   | Quantity   | URL  |Price |
|------------|------------|------------|------------|------------|------------|-|
| Intel| 82635AWGDVKPMP| Intel| 82635AWGDVKPMP| 1|[Intel Realsense D435](https://store.intelrealsense.com/buy-intel-realsense-depth-camera-d435.html?_ga=2.115091842.488370469.1732555865-1273271566.1726263535)|314.00 USD|

## Refrences 
[1]“OpenCV: Hough Line Transform,” docs.opencv.org. https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html  

[2]“Intel ® RealSense TM Product Family D400 Series Datasheet Intel ® RealSenseTM Vision Processor D4, Intel ® RealSenseTM,” 2024. Available: https://www.intelrealsense.com/wp-content/uploads/2024/10/Intel-RealSense-D400-Series-Datasheet-October-2024.pdf?_ga=2.12134836.184176440.1732746469-1273271566.1726263535  

[3]“What is Object Detection in Computer Vision?,” GeeksforGeeks, May 10, 2024. https://www.geeksforgeeks.org/what-is-object-detection-in-computer-vision/  
‌  
[4]X. Ling, “How to Optimize QR Recognition Performance by Image Preprocessing and Parameter Tuning,” DEV Community, Sep. 13, 2021. https://dev.to/yushulx/how-to-optimize-qr-recognition-performance-by-image-preprocessing-and-parameter-tuning-24p8 (accessed Nov. 28, 2024).

[5]OpenCV, “About OpenCV,” OpenCV, 2018. https://opencv.org/about/

[6]“Real time object color detection using OpenCV,” GeeksforGeeks, Oct. 14, 2021. https://www.geeksforgeeks.org/real-time-object-color-detection-using-opencv/

[7]A. Rosebrock, “AprilTag with Python,” PyImageSearch, Nov. 02, 2020. https://pyimagesearch.com/2020/11/02/apriltag-with-python/
‌
‌
‌
‌
‌
‌
