import cv2
import numpy as np
from stream_reciver import Reciver
import random
from command import Commands 
from tracking import Tracker
from datetime import datetime


class Core: # main core
    def __init__(self):
        self.receive = Reciver()
        self.commands = Commands()
        self.tracker = Tracker()
        self.frame_width = 640
        self.frame_height = 480
        self.dead_zone = 40
        self.QRcode_center_x = 0
        self.QRcode_center_y = 0
        self.qr_detector = cv2.QRCodeDetector()
        self.errors = []

    
    def get_frame(self): # get frame from the camera
        """
        the get_frame function get the frame from the camera
        """
        try:
            return self.receive.receive() # returning hte received frame
        except:
            self.errors.append("Error: get_frame")
            return None


    def processor(self , frame , option = None): # process the frame
        if frame is None:  # if no frame received
           return None
        # if frame found,
        frame = cv2.resize(frame , (self.frame_width , self.frame_height))
        # removing the noise from frame
        frame = cv2.GaussianBlur(frame , (5 , 5) , 0)
        
        if option is None:
            return None
        elif option == 'QRcode':
            found , data , center_x , center_y , points = self.QRcode(frame)
            if found == False: # if no QRcode found
                return None
            if found and data != '':
                command = self.tracker.QR_track(center_x , center_y)
                if command is not None:
                    self.commands.turn(command , lcd_text=data)
                
                return found , data
            else:
                return None
        else:
            return None

    def QRcode(self , frame): # QRcode detector
        found = False
        data, points, _ = self.qr_detector.detectAndDecode(frame)
        # if QRcode found,
        if points is not None and data != '':
            found = True
            points = points.astype(int)
            for i in range(4):
                # drawing the QRcode border
                cv2.line(frame , tuple(points[i][0]) , tuple(points[(i+1)%4][0]) , (0 , 255 , 0) , 2)

            # calculating the center of QRcode
            center = np.mean(points[0], axis=0)
            center_x = int(center[0])
            center_y = int(center[1])

            return found , data , center_x , center_y , points
        else: # if no QRcode found
            return found , None , None , None , None


    def stuck(self): # stuck state
        """
        the stuck state robot try to escape
        """
        self.commands.stuck(lcd_text='Stuck_try to escape')


    def search(self): # search state
        """
        the search state robot try to find the target
        """
        self.commands.search_mode(lcd_text='Searching')


    def sleepmode(self): # SleepMode
        """
        the sleepmode robot sleep for a while
        """
        self.commands.sleep_mode(lcd_text='Sleeping')

    def flush_error(self , error): # saving the error into txt file
        with open('error.txt' , 'w') as f:
            f.write(error)
        self.errors = []
