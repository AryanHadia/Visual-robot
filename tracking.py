# tracking the faces or objectes or QRcode
import cv2
import numpy as np
import time

class Tracker:
    def __init__(self):
        self.errors = []

        self.frame_width = 640
        self.frame_height = 480

        self.center_x = self.frame_width // 2
        self.center_y = self.frame_height // 2

        self.dead_zone = 40
        

    def face_track(self , center_x , center_s): # tracking the face
        pass

    def object_track(self , center_x , center_s): # tracking the object
        pass

    def QR_track(self , center_x , center_s): # tracking the QRcode
        pass

    def calculate_error(self , center_x):
        pass