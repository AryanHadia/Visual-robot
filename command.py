# command that will be sent to raspberry pi
import time
import random
from commandsender import CommandSender as CS
from datetime import datetime

class Commands: 
    def __init__(self):
        self.errors = []
        self.ComSender = CS()
        self.last_command = "" # last command sent


    def state(self , state , lcd_text=None , option=None): # change the state of the robot
        states = {'stuck' : self.stuck , 'search' : self.search , 'sleep_mode' : self.sleep_mode , 'turn' : self.turn}
        if state not in states:
            return False
        if state == 'turn':
            return self.turn(option=option , lcd_text=lcd_text)
        else:
            states[state](lcd_text=lcd_text)
        return True


    def send(self , command , lcd_text): # send the command bt self.ComSender
        try:
            packet = f'{command}|{lcd_text}/\n'
            if packet == self.last_command: # if the command is the same as last command
                return False
            elif packet != self.last_command:
                print(f"command / {lcd_text} / {command}")
            self.ComSender.send(packet)
            self.last_command = packet # update the last command
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
            self.send(command=direction , lcd_text=lcd_text) # send the direction to the robot
            self.send(command='S' , lcd_text=lcd_text) # send the reset command to the robot
        except Exception as e:
            error = f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Failed to send stuck command | Error: {e}'
            print(error)
            self.errors.append(error)
            return False
        return True

    
    def sleep_mode(self , lcd_text = None): # sleep mode
        try:
            self.send(command='S' , lcd_text=lcd_text)
            return True
        except Exception as e:
            error = f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Failed to send sleep mode command | Error: {e}'
            print(error)
            self.errors.append(error)
            return False


    def turn(self , option , lcd_text = None): # turning left and right
        if option == 'L':
            self.send(command='L' , lcd_text=lcd_text)
            return True
        elif option == 'R':
            self.send(command='R' , lcd_text=lcd_text)
            return True
        elif option == 'C':
            self.send(command='C' , lcd_text=lcd_text)
            return True
        else:
            print('command: Invalid option')
            self.errors.append(f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Invalid option received')


    def search(self , lcd_text = None):
        # a command that will be sent to the robot when it is searching for the target
        self.send(command='SE' , lcd_text=lcd_text)
        

    def flush_error(self): # saving error in the error file
        try:
            with open('error_log.txt', 'a') as f: # overwrite the error file
                for error in self.errors:
                    f.write(error + '\n')
                self.errors.clear() # clearing the error list
        except Exception as e :
            error = f'command / {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} / Failed to flush error | Error: {e}'
            print(error)
            self.errors.append(error)
