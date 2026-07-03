# command that will be sent to raspberry pi
import time
import random
from commandsender import CommandSender as CS
from datetime import datetime
from tracking import Tracker

class Commands: 
    def __init__(self):
        self.errors = []
        self.ComSender = CS()
        self.tracker_ = Tracker()

    def send(self , command , lcd_text): # send the command bt self.ComSender
        try:
            self.ComSender.send(f'{command},{lcd_text}')
            return True
        except Exception as e:
            error = f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Failed to send command | Error: {e}'
            print(error)
            self.errors.append(error)
            return False
    
    def stuck(self , lcd_text = None):
        # a command that will be sent to the robot when it is stuck to escape
        # make a ramdom direction to exape the robot
        direction = random.choice(['L' , 'R'])
        try:
            self.send(direction , lcd_text) # send the direction to the robot
            time.sleep(1)
            self.send('S' , lcd_text) # send the reset command to the robot
        except Exception as e:
            error = f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Failed to send stuck command | Error: {e}'
            print(error)
            self.errors.append(error)
            return False
        return True

    def sleep_mode(self , text): # sleep when it's no use
        return self.send('S' , text)

    def search_mode(self , lcd_text = None): # turning the servo motor to left and right
        # turn right 20 deg
        try:
            for _ in range(1,10): # turn right 20 deq
                self.send('R' , lcd_text)
            self.send('C' , lcd_text) # recentering the servo motor
            for _ in range(1,10): # turning left for 20 deg
                self.send('L' , lcd_text)
            self.send('C' , lcd_text) # recentering the servo motor
            return True
        except: # and if it failed
            return False
    
    def sleep_mode(self , lcd_text): # sleep mode
        try:
            self.send(command='S' , lcd_text=lcd_text)
            return True
        except:
            return False

    def turn(self , option , lcd_text = None): # turning left and right
        if option == 'L':
            return self.send('L' , lcd_text)
        elif option == 'R':
            return self.send('R' , lcd_text)
        else:
            print('Invalid option')
            self.errors.append(f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Invalid option received')

    def search(self , lcd_text = None):
        # a command that will be sent to the robot when it is searching for the target
        search_step = 10 # 20 deg
        try:
            for _ in range(search_step):
                self.send('R' , lcd_text)
                time.sleep(0.5)
            self.send('C' , lcd_text) # send the recenter command to the robot
            for _ in range(search_step):
                self.send('L' , lcd_text)
                time.sleep(0.5)
            self.send('C' , lcd_text) # send the recenter command to the robot
        except Exception as e:
            error = f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Failed to send search command | Error: {e}'
            print(error)
            self.errors.append(error)
            return False    
        return True
        

    def flush_error(self): # saving error in the error file
        try:
            with open('error_log.txt', 'w') as f: # overwrite the error file
                for error in self.errors:
                    f.write(error + '\n')
                self.errors.clear() # clearing the error list
        except Exception as e :
            error = f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Failed to flush error | Error: {e}'
            print(error)
            self.errors.append(error)
