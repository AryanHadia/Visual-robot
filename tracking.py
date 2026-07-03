# tracking the faces or objectes or QRcode
import cv2
import numpy as np
import time
from command import Commands

class Tracker:
    def __init__(self):
        self.errors = []       

    def face_track(self , center_x , center_s , lcd_text): # tracking the face
        pass

    def object_track(self , center_x , center_s , lcd_text): # tracking the object
        pass

    def QR_track(self , center_x , center_s): # tracking the QRcode
        if center_x is None or center_s is None:
            return None
        # if the center_x is not in the center of the screen
        if center_x > center_s + 50: # if the center_x is in the right side of the screen
            return 'R'
        elif center_x < center_s - 50: # if the center_x is in the left side of the screen
            return 'L'
        else: # if the center_x is in the center of the screen
            return 'C'

    def calculate_error(self , center_x):
        pass
