# Detailed Design for Object and Line Detetion
## Function of Subsystem
The function of this subsystem is to provide the location of the astral materials and lines on the game feild, as well as read the april tags. 

## Specifications and Constraints 
### Specifications
1. The robot's sensors shall be able to find the walls of the game field and the cave, specifications 4 and 5.
2. The robot's sensors shall be able to detect the white lines on the game board, specifications 2 iii and v.
3. The robot's sensors shall be bale to detect when the start LED turns on, specifications 2 i and ii.
4. The robot's sensors shall be able to detect the magnetic fields of the Geodinium, specifications 2 vii and viii.
5. The robot's sensors shall be able to work effectively despite background interference in the competition environment, specification 11.
6. The robot's general sensor subsystem shall have a user manual that explains functionality and design intent, constraint 2.

### Constraints

## Proposed Solution
* add specifacations and constraints when done.
In order to meet the specifications and constraints the robot will need an RGBD camera, this camera will be able to pick out the RGB values of the astral matrials and lines on the game field against the dark background of the game field.
The camera will also be able to pick out the depth, or distance from the camera, of the astral material, the shipping containers, and the walls of the game field.
The information from the camera and the other sensors as detailed by the sensor subsystem detail design will be used by an object detection algorithm to the robot where the objects are on the game field, mainly the astral material, walls, and shipping containers.
The image data from the camera will also be used by a line detection algorithm to find the white lines on the game field to assist in navigation and sorting of the shipping containers.
Finally the image data will undergo an image processing algorithm which will allow it to read the april tags, much in the same way a phone can read a qr code from a picture or screenshot.

## Interface with Other Systems
The 
## Buildable Schematic
## FlowChart
## Analysis
## Ethics 
## Refrences 

