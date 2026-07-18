# sending the command to the raspi with socket
import socket
from datetime import datetime

class CommandSender:
    def __init__(self):
        self.error_log = []
        self.is_connected = False
        self.port = 5001
        self.ip = '192.168.1.57' # raspi ip
        # command saving file
        self.file = open("commands.txt", "a")
        self.connection_Attempt = 0 # number of times it tried to connect
        # connect 
        self.connection(ip=self.ip, host=self.port)
        self.last_command = "" # last command sent


    def connection(self , ip , host): # connecting to raspi
        try:
            print("sender: connecting to robot...")
            self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            print("sender: socket created successfully")
            self.socket.connect((ip , host))
            self.is_connected = True
            print(f"connected to {ip}:{host}")
        except Exception as e:
            try:
                self.socket.close()
                self.socket = None
            except:
                pass
            print(f"error connecting: {e}")

    def send(self , command): # command sender
        self.last_command = command
        try:
            self.socket.sendall(command.encode()) # send the command to robot
            self.com_saver(command=command)
            print(f"send: sent command: {command}")
        except Exception as e:
            print(f"send: Failed to send the command. error = {e}")
            self.error_log.append(f"send: Failed to send the command. error = {e}")
           
            if not self.con_check():
                self.is_connected = False
                self.reconnect()
            try:
                self.socket.sendall(command.encode())
                self.com_saver(command=command)
            except Exception as e:
                print(f"commandsender / Failed to send the command. error = {e}")
                self.error_log.append(f"commandsender / Failed to send the command. error = {e}")
                pass

    def com_saver(self , command): # save the command in the txt file
        # save the command in the txt file
        self.file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  : {command} \n')
        self.file.flush()

    def close(self): # close all the programs
        try:
            # close the connection
            if hasattr(self, "socket"):
                self.socket.close()
                self.socket = None
            # close the command saving file
            self.file.close()
            self.connection_Attempt = 0
            self.is_connected = False
        except Exception as e:
            print(f"commandsender / Failed to close the connection. error = {e}")
            self.error_log.append(f"commandsender / Failed to close the connection. error = {e}")
            pass

    def reconnect(self): # restart the connection
        self.connection_Attempt += 1
        self.close()
        self.is_connected = False
        for i in range(3):
            self.connection(ip=self.ip, host=self.port)
            if self.con_check():
                break
        else:
            self.close()

    def con_check(self): # check if its connected
        try:
            self.socket.getpeername()
            return True
        except:
            return False

    def save_error(self): # save the error log in the txt file
        with open("error_log.txt", "w") as f:
            for error in self.error_log:
                f.write(error + "\n")
        self.error_log = []

    def file_close(self): # close the command saving file
        self.file.close()
        
