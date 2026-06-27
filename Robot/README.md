## Vision Robot (Robot Program "Vision_robot.ino")
this part of the project is the robot program that controls the servo and the relay.
The robot is used to control the servo and the relay from the computer.
it should be used on raspberry pi.

# Hardware
 - Arduino (I used Arduino uno but you can use any other Arduino board).
 - Servo motor with 180 degree range.
 - Relay module.
 - Lcd ic2 with 16x2 display.
 - raspberry pi (I used raspberry pi 3 but you can use any other raspberry pi).

# Software
 - Arduino IDE.
 - Python 3.6 or higher.
 - RpiCamera (if you want to use the camera).
 - Rx2 display.

# Supported commands
 - Rotate the camera left.
 - Rotate the camera right.
 - Stop the camera.
 - Turn led on/off.
 - Stream the camera on pc.

# Installation
    1. install the required libraries.
    2. upload the robot program to the raspberry pi.
    3. connect the servo and the relay to the raspberry pi.
    4. run the robot program.

# How to Use
    1. connect the robot to the computer.
    2. run the robot program (robot_run.py).
    3. send the command to the robot.
    4. upload the Vision_robot.ino on Arduino.
    5. make sure your using the correct pins of Arduino.
    6. the robot will execute the command.
    7. the robot will show the command on the lcd.
    8. the robot will wait for the next command.

# Camera setup
    1. connect the camera to the raspberry pi (if it need a Driver install it).
    2. make sure the camera is working (the camera should be on '/dev/video0' if its not you should change it by yourself in robot_run.py).
    3. run the robot program (robot_run.py).
    4. send the command to the robot.
    5. the robot will execute the command.
    6. the robot will show the command on the lcd.
    7. the robot will wait for the next command.

# Good lighting
The object detection accuracy depends heavily on ambient lighting.

For best results, use a dedicated LED light mounted near the camera.

# Connectiong to the pc
it's very simple
    
    1. Connect the pc and raspi to same router.
    2. run the robot program (robot_run.py).
    
    At this moment raspi will try to find the pc by it self.
    but if it can't find the pc it's gonna ask you to enter the pc ip manually.

