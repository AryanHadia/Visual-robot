# sending the command to the raspi with socket
import socket
from datetime import datetime

class CommandSender:
    def __init__(self):
        self.error_log = []
        self.is_connected = False
        self.port = 5001
        self.ip = '0.0.0.0' # every
        # command saving file
        self.file = open("commands.txt", "a")
        self.connection_Attempt = 0 # number of times it tried to connect
        # connect to the robot
        self.connection()

    def connection(self): # connecting to raspi
        try:
            while self.connection_Attempt < 3:
                # connect
                self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                print("Making socket !")
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow to reuse the address
                print("Done")
                self.socket.bind((self.ip , self.port))
                self.socket.listen(1)
                print("listening !")
                self.conn, addr = self.socket.accept()
                self.is_connected = True # its connected
                print(f"connected to {addr}")
                self.connection_Attempt = 0
                break
        except Exception as e: # if failed to connect
            self.connection_Attempt += 1
            print(f'Failed to connect error: {e}')
            self.error_log.append(f'commandsender / Failed to connect error: {e}')
            self.is_connected = False

    def send(self , command): # command sender
        try:
            self.conn.sendall(command.encode()) # send the command to robot
            self.com_saver(command=command)
        except Exception as e:
            print(f"commandsender / Failed to send the command. error = {e}")
            self.error_log.append(f"commandsender / Failed to send the command. error = {e}")
           
            if not self.con_check():
                self.close()
                self.is_connected = False
                self.connection()
            try:
                self.conn.sendall(command.encode())
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
            if hasattr(self, "conn"):
                self.conn.close()
            # close the socket
            if hasattr(self, "socket"):
                self.socket.close()
            # close the command saving file
            self.connection_Attempt = 0
            self.is_connected = False
        except Exception as e:
            print(f"commandsender / Failed to close the connection. error = {e}")
            self.error_log.append(f"commandsender / Failed to close the connection. error = {e}")
            pass

    def restart(self): # restart the connection
        self.close()
        self.is_connected = False
        self.connection_Attempt = 0
        self.connection()

    def con_check(self): # check if its connected
        return (self.is_connected and hasattr(self, "conn"))

    def save_error(self): # save the error log in the txt file
        with open("error_log.txt", "w") as f:
            for error in self.error_log:
                f.write(error + "\n")
        self.error_log = []

    def file_close(self): # close the command saving file
        self.file.close()
