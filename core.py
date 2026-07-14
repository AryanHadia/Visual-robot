import cv2
import numpy as np
from stream_reciver import Receiver
from command import Commands 
from tracking import Tracker
from datetime import datetime


class Core: # main core
    def __init__(self):
        self.receive = Receiver()
        self.commands = Commands()
        self.tracker = Tracker()
        self.frame_width = 640
        self.frame_height = 480
        self.dead_zone = 40
        self.QRcode_center_x = 0
        self.qr_detector = cv2.QRCodeDetector()
        self.stuck_counter = 0 # counter for the stuck
        self.brightness_factor = 1 # brightness factor for the frame brightness
        self.errors = []
        self.log = []

    
    def get_frame(self): # get frame from the camera
        """
        the get_frame function get the frame from the camera
        """
        return self.receive.recv()


    def processor(self , frame , option = None): # process the frame
        if frame is None:  # if no frame received
           return None

        # if frame found,
        frame = cv2.resize(frame , (self.frame_width , self.frame_height))
        
        if option is None:
            return None , None
        elif option == 'QRcode': # QRcode tracking
            found , data , center_x , points = self.QRcode(frame)
            if found == False: # if no QRcode found
                self.commands.sleep_mode(lcd_text="Sleeping !!")
                return None , None
            # if QRcode found
            if found:
                command = self.tracker.QR_track(center_x)
                if command is not None: # if command found
                    self.commands.turn(command , lcd_text=data)
                    stuck = False # if robot not stuck then continue tracking
                    if command != 'C':
                        stuck = self.stuck_detection(center_x)
                    if stuck == True:
                        self.state('stuck' , lcd_text='Stuck :(')
                        return None , None
                    self.QRcode_center_x = center_x
                    return found , data
                return found , data
            else: # if no command found
                self.state('search' , lcd_text='Searching')
                return None , None
        else:
            return None , None

    def QRcode(self , frame): # QRcode detector
        found = False
        data, points, _ = self.qr_detector.detectAndDecode(frame) # detect and decode the QRcode
        # if QRcode found,
        if points is not None and data != '': # if a QRcode found
            self.log.append(f"{datetime.now()} - QRcode found: {data}")
            print(f"QRcode: {data}")
            found = True
            points = points.astype(int)

            # calculating the center of QRcode
            center = np.mean(points[0], axis=0)
            center_x = int(center[0])

            return found , data , center_x , points
        else: # if no QRcode found
            self.log.append(f"{datetime.now()} - No QRcode found")
            return found , None , None , None

    
    def stuck_detection(self , center_x): # found out if camera stuck
        if abs(center_x - self.QRcode_center_x) < 3:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0

        if self.stuck_counter > 20:
            return True
        else:
            return False


    def state(self , state , lcd_text): # change the state of robot
        states = {
            'stuck': self.commands.stuck,
            'search': self.commands.search_mode,
            'sleepmode': self.commands.sleep_mode,
        }
        func = states.get(state)
        if func:
            func(lcd_text=lcd_text)


    def flush_error(self): # saving the error into txt file
        with open('error.txt' , 'a') as f:
            for _ in self.errors:
                f.write(_ + "\n")
        self.errors.clear()

    
    def log_flush(self): # save the log into file
        with open('log.txt' , 'a') as f:
            for _ in self.log:
                f.write(_ + "\n")
        self.log.clear()


    def show_frame(self , frame): # show the frame in the window
        cv2.imshow('frame' , frame)
        cv2.waitKey(1)


    def brightness(self , frame): # make a desicion to turn the light on or off
        gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        if brightness <= 50: # if its dark
            self.brightness_factor = 4  # increasing the frame brightnes
            frame = cv2.convertScaleAbs(frame , alpha=self.brightness_factor , beta=0)
        elif 50 < brightness <= 100: # if its not dark
            self.brightness_factor = 3  # decreasing the frame brightnes
            frame = cv2.convertScaleAbs(frame , alpha=self.brightness_factor , beta=0)
        elif 100 < brightness <= 150: # if its not dark
            self.brightness_factor = 1.5  # increasing the frame brightnes
            frame = cv2.convertScaleAbs(frame , alpha=self.brightness_factor , beta=0)
        else: # if its not dark
            self.brightness_factor = 1  # decreasing the frame brightnes
            frame = cv2.convertScaleAbs(frame , alpha=self.brightness_factor , beta=0)
        return frame

    
    def run(self): # run the program
        while True:
            frame = self.get_frame() # get the frame
            if frame is None:
                continue

            frame = self.brightness(frame)
            found , data = self.processor(frame , option='QRcode')
            self.show_frame(frame) # show the frame
            if cv2.waitKey(1) & 0xFF == ord('q'): # if q is pressed, break the loop
                break
        
        # save the log and error log
        self.flush_error()
        self.log_flush()
        cv2.destroyAllWindows()
            
