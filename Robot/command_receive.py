import socket
import serial
import serial.tools.list_ports
import time

# try to connect to pc for receiving commands and Arduino for sending commands

class CommandReceive:
    def __init__(self):
        # connection attempt:
        self.ar_attempt = 0
        self.pc_attempt = 0
        # try to connect to pc and arduino
        self.arduino_is_con = False
        self.pc_is_con = False
        self.sock = None
        self.arduino = None
        self.connection_attempts = 0
        # ip and port
        self.ip = "0.0.0.0"
        self.port = 5001

    
    # pc connection
    def connect(self , ip , port):
        try:
            print("recv: making socket connection")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)           
            print("recv: socket created")
            self.sock.bind((ip, port))
            print("recv: socket bound")
            self.sock.listen(1)
            print("recv: socket listening")
            print("Waiting for client...")
            self.conn, self.addr = self.sock.accept()
            self.conn.settimeout(5) # 
            print(f"connected by {self.addr}")
            self.connection_attempts = 0
            self.pc_is_con = True
            self.pc_attempt = 0
            return True
        except Exception as e:
            print(f"Connect Error: {e}")
            return False
            

    def receive_command(self): # receive command from pc
        """
        receive command from pc
        """
        if self.conn is not None: # if the connection is established
            try:
                print("waiting for command...")
                data = self.conn.recv(1024) # receive the command from pc
                if not data: # if no data received
                    return False
                print(f"recv: received command: {data.decode().strip()}")

                return data.decode().strip()
            except Exception as e:
                print(f"error receiving command: {e}")
                return False


    # arduino connection
    def connect_arduino(self): # try to connect arduino with founded port
        try:
            ports = ['/dev/ttyACM0' , '/dev/ttyUSB0'] # Ardunino portes
            if self.ar_attempt > 3: # if the connection attempt is more than 3 times
                raise Exception("failed to connect to arduino after multiple attempts")
            # try to connect to arduino
            for port in ports:
                try:
                    self.arduino = serial.Serial(port, 9600, timeout=1)
                    self.arduino_is_con = True
                    print("connected to arduino !")
                    break
                except:
                    continue
            self.ar_attempt = 0
            return
        except Exception as e:
            self.ar_attempt += 1
            print(f"failed to connect to arduino: {e}")
            if self.ar_attempt > 3:
                raise Exception("failed to connect to arduino after multiple attempts")


    def send_command(self, command): # send command to Arduino 
        """
        send command to Arduino
        """
        if self.arduino is not None:
            self.arduino.write(command.encode())
            print(f"sent command: {command}")
    

    # closing all connections
    def close_all(self):
        """
        close all connections
        """
        if self.conn is not None: # closing the connection
            self.conn.close()
            self.conn = None
            print("conn closed")
        if self.sock is not None: # closing the socket
            self.sock.close()
            self.sock = None
            print("sock closed")
        if self.arduino is not None: # closing the Arduino
            self.arduino.close()
            self.arduino = None
            print("arduino closed")
        
    
    # run the command receive
    def run(self):
        # connecting to the computer
        self.connect(self.ip, self.port) # Connecting

        if self.pc_is_con is True: # if connected
            self.connect_arduino()
            if self.arduino_is_con is True:
                print("connected to arduino !")
            else: # if failed to connecting to the Arduino
                print("failed to connect to arduino !")
                return False
        else: # if not connected
            print("failed to connect to pc !")
            return False


        print("Done !")
        while True:
            # check if connection is lost
            if self.conn is None:
                print("connection lost, reconnecting...")
                self.reconnect()
                continue

            command = self.receive_command() # receive the command
            if command is False: # if no command received
                self.reconnect()
                continue
             
            if command == "exit": # if the command is exit
                self.close_all()
                break

            print(f"received command: {command}")
            self.send_command(command) # send command to arduino


    # reconnect the connections
    def reconnect(self):
        self.close_all()
        self.connection_attempts += 1
        if self.connection_attempts > 3:
            raise Exception("failed to reconnect the connections after multiple attempts")
        self.connect(self.ip, self.port)
        if not self.arduino_is_con:
            self.connect_arduino()
        print("reconnected the connections")

if __name__ == "__main__": # if the program is run directly
    CommandReceive = CommandReceive()
    CommandReceive.run()
