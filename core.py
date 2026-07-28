import cv2
import numpy as np
from stream_reciver import Receiver
from command import Commands 
from tracking import Tracker
from datetime import datetime
import time
from insightface.app import FaceAnalysis


class Core: # main core
    def __init__(self):
        self.receive = Receiver()
        self.commands = Commands()
        self.tracker = Tracker()
        self.frame_width = 640
        self.frame_height = 480
        self.dead_zone = 40
        self.qr_detector = cv2.QRCodeDetector()
        self.stuck_counter = 0 # counter for the stuck
        self.brightness_factor = 1 # brightness factor for the frame brightness
        self.is_streaming = False # flag to monitor stream status
        self.errors = []
        self.log = []
        self.last_qr_data = "" # last QRcode data received
        self.frame_counter = 0 # counter for the frame received
        self.app = FaceAnalysis()
        self.app.prepare(ctx_id=0)
        self.last_state = None # last state of the robot
        self.detection_timing = 0 # timing for the detection
        self.data = None
        self.center_x = None
        self.faces = 0

    def get_frame(self): # get frame from the camera
        """
        the get_frame function get the frame from the camera
        """
        frame = self.receive.recv()
        self.frame_counter += 1
        cv2.imshow("frame" , frame)
        return frame


    def should_detect(self): # timer for the detection
        if self.detection_timing <= 60:
            self.detection_timing += 1
            return False
        else:
            self.detection_timing = 0
            return True


    def change_state(self , state , lcd_text=None , option=None): # change the state of the robot
        if state != self.last_state: # if the state is changed
            self.last_state = state # update the last state
            if state == 'turn':
                return self.commands.state(state=state , option=option , lcd_text=lcd_text)
            return self.commands.state(state , lcd_text)
            # return True
        else:
            return False

     # ======= frame processor ========
    def Qrcode(self , frame): # detecting the QRcode
        if frame is not None:
            if self.should_detect() is True: # if the detection time is not up
                data, value,_ = self.qr_detector.detectAndDecode(frame) # detect the QRcode
            else: 
                if self.center_x is None:
                    return False
                command = self.tracker.tracker(center_x=self.center_x)
                self.change_state(state='turn' , option=command , lcd_text=self.data)
                return False
            # if the QRcode is detected
            if data:
                # if the QRcode data is changed
                if self.last_qr_data != data:
                    print(f"QRcode data: {data}")
                    self.data = data
                    self.last_qr_data = data
                # calculating the center of QRcode
                center = np.mean(value[0], axis=0)
                center_x = int(center[0])
                command = self.tracker.tracker(center_x=center_x)
                self.change_state(state='turn' , option=command , lcd_text=data)
                self.center_x = center_x
                return True
            else:
                self.data = None
                self.center_x = None
                self.faces = 0
                self.change_state(state='sleep_mode' , lcd_text="No QRcode")
                return False

    
    def face_detect(self , frame): # detecting the face
        if frame is not None:
            if self.should_detect() is True: # if the detection time is not up
                faces = self.app.get(frame)
            else: 
                if self.center_x is None:
                    return False
                command = self.tracker.tracker(center_x=self.center_x)
                self.change_state(state='turn' , option=command , lcd_text=self.faces)
                return False
            # if the face is detected
            if faces:
                center_x = int((faces[0].bbox[0] + faces[0].bbox[2]) // 2)
                command = self.tracker.tracker(center_x=center_x)
                self.change_state(state='turn' , option=command , lcd_text=str(len(faces)))
                self.center_x = center_x
                self.faces = len(faces)
                return True
            else:
                self.center_x = None
                self.faces = 0
                self.change_state(state='sleep_mode' , lcd_text="No face")
                return False

    
    def object_detect(self , frame): # detecting the object
        pass

    
    # ======= stuck detection & states ========
    def stuck_detection(self , center_x): # found out if camera stuck
        pass


    # ======= flushing the logs and errors ========
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


    # ======= frame configuration ========
    def brightness(self , frame): # make a desicion to turn the light on or off
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

    
    #====================== running the program ======================
    def run(self , option='qrcode'): # run the program
        options = {'qrcode' : self.Qrcode , 'face' : self.face_detect}


        # log the time 
        self.log.append(f"{datetime.now()} - Program started / option: {option}")
        while True:
            try:
                # if the stream is not streaming
                frame = self.get_frame() # get the frame
                self.frame_counter += 1
                if frame is None:
                    continue
                frame = cv2.resize(frame , (self.frame_width , self.frame_height))
                frame = self.brightness(frame)
                options[option](frame)

                # if frame found,
                if cv2.waitKey(1) & 0xFF == ord('q'): # if q is pressed, break the loop
                    self.close_all()
                    break
                

            except Exception as e: # if it failed to process the frame
                self.errors.append(f"Error: {e}")
                self.log.append(f"Error: {e}")
                continue
        self.close_all()

    def close_all(self):

        # log the time 
        self.log.append(f"{datetime.now()} - Program terminated")
        self.log.append(f"Total frames processed: {self.frame_counter}")
        # save the log
        self.flush_error()
        self.log_flush() 
        # close all windows
        cv2.destroyAllWindows()
