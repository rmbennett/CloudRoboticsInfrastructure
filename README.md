1    System Requirements

1.  Ros Groovy
2.  OpenCV
3.  Python
4.  Pip (python Package Manager)
	
	(a)  p2osdriver

	(b)  pymongo
	
	(c)  PyWit

5.  Webcam compatible with Linux (all x2 if wishing to use data sharing)
6.  Microphone
7.  Asus Xtion Pro
8.  Pioneer People Bot Robot
9.  USB Joystick controller

2    System User Guide

A basic understanding of ROS and a working installation of ROS-Groovy is assumed here.  For guides to acquiring this knowledge please see http://wiki.ros.org/groovy/Installation/Ubuntu and http://wiki.ros.org/ROS/Tutorials 

Important - Before running any commands ensure there is a roscore running.

In order to launch drive around the Pioneer People Bot please use commands:

1.  roslaunch exercise1 p3at.launch
2.  roslaunch exercise1 joystickcontroller.launch

Sonar and Bump Data collection can be run using

1.  roslaunch exercise1 p3at.launch

2.  roslaunch exercise1 joystickcontroller.launch

3.  rosrun beginnertutorials completelistener.py

Audio and Motion Data Collection
1.  roslaunch exercise1 p3at.launch

2.  roslaunch exercise1 joystickcontroller.launch

3.  rosrun beginnertutorials motiondetect.py

4.  rosrun beginnertutorials audiolistener.py


Data Sharing

1.Publishing Laptop

	(a)  roslaunch exercise1 p3at.launch
	
	(b)  roslaunch exercise1 joystickcontroller.launch

	(c)  rosrun beginnertutorials sharedMotionData.py

2.  Receiving Laptop

	(a)  roslaunch exercise1 p3at.launch

	(b)  roslaunch exercise1 joystickcontroller.launch

	(c)  rosrun beginnertutorials sdataSharerReceiver.py
