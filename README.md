# Vision-Based Autonomous Robot
A vision assistant robot with serial communication
### Description
This project is a vision-based robot using Raspberry Pi and Arduino.
The Raspberry Pi handles image processing and communication, while the Arduino controls hardware components such as servo motors and LCD.
### Features
- Find Qr_codes of faces or objects
- Using a AI model to recognize the objects or ...
- using a microphone to listen to the user's voice and save the conversation on sql database
### Hardware
- Raspberry Pi 3
- Arduino Uno
- Servo motor
- ic2 lcd display
- External Power supply (for raspi and servo motor)
- USB webcam
- A camputer or laptop to connect the robot
### How to use
1. First you should connect pc and raspi both to a same wifi network.
2. then you sould get raspi Ip address and give it to pc in codes (stream_receiver.py & command_sender.py)
3. then run the (run.py) in raspi.
4. run the run.py on pc.
5. and then your robot is ready to use.
### Technologies
- Python
- OpenCV
- Serial
- Socket
- datetime
- random
- time
- numpy
- subprocess
- sys
- os

### Planned features
- Find Qr_codes of faces or objects
- Using a AI model to recognize the objects or ...
- using a microphone to listen to the user's voice and save the conversation on sql database

### Architecture

PC:
- OpenCV image processing
- Face/Object/QR detection
- Decision making

Raspberry Pi:
- Camera streaming
- Network communication
- Command forwarding

Arduino:
- Servo control
- LCD control
