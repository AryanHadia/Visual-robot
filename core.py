import cv2
import numpy as np
from stream_reciver import Reciver


class Core:
    def __init__(self):
        self.reciver = Reciver()
        # object detection
        self.object = None
        # shape detection
        self.shape = None
        # color detection
        self.color = None

    def run(self):
        # run the file
        frame = None
        while True:
            frame = self.reciver.recv() 
            if frame is None:
                continue

            if self.object is not None:
                self.ObjectDetection(frame , self.object)
                self.shape = None # reset the shape when it want to detect the object
            elif self.object is None: # if the object is not found, then detect the shape
                if self.shape is not None:
                    self.shapeDetection(frame , self.shape)

            if self.color is not None: # if the color is not found, then detect the QR code
                self.ColorDetection(frame , self.color)

    def processor(self): # process by the founded data from frame
        pass
        
    def ColorDetection(self, frame , color): # color detection
        pass

    def shapeDetection(self, frame , shape): # shape detection
        pass

    def QRCodeDetection(self, frame): # QR code detection
        pass

    def ObjectDetection(self, frame , object): # object detection
        pass

    def FaceDetection(self, frame): # face detection
        pass
