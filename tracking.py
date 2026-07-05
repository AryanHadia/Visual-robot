# tracking the target
class Tracker:
    def __init__(self):
        self.errors = []   
        self.center_s = 320

    def face_track(self , center_x , center_s , lcd_text): # tracking the face
        pass

    def object_track(self , center_x , center_s , lcd_text): # tracking the object
        pass

    def QR_track(self , center_x): # tracking the QRcode
        if center_x is None:
            return None
        # if the center_x is not in the center of the screen
        if center_x > self.center_s + 50: # if the center_x is in the right side of the screen
            return 'R'
        elif center_x < self.center_s - 50: # if the center_x is in the left side of the screen
            return 'L'
        else: # if the center_x is in the center of the screen
            return 'C'

    def calculate_error(self , center_x):
        pass
