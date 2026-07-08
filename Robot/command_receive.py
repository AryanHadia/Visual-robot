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
        # try to connect to pc and arduino
        self.port = 5001
        self.ip = "0.0.0.0"
        con = self.connect(self.ip , self.port)
        if con:
            self.pc_is_con = True
            self.connect_arduino()


    
    # pc connection
    def connect(self , ip , port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((ip, port))
            self.sock.listen(1)
            print("Waiting for client...")
            self.conn, self.addr = self.sock.accept()
            self.conn.settimeout(5)
            print(f"connected by {self.addr}")
            return True
        except :
            return False
            
    def receive_command(self): # receive command from pc
        """
        receive command from pc
        """
        try:
            if self.conn is not None: # if the connection is established
                self.sock.settimeout(5)
                data = self.conn.recv(1024)
                if not data:
                    print("Client disconnected")
                    self.reconnect() # reconnect
                    return None
                return data.decode().strip()
        except Exception as e:
            print(f"error receiving command: {e}")
            self.conn.close()
            self.reconnect() # reconnect
            return None


    # arduino connection
    def connect_arduino(self): # try to connect arduino with founded port
        try:
            ports = ['/dev/ttyACM0' , '/dev/ttyUSB0']
            if self.ar_attempt > 3: # if the connection attempt is more than 3 times
                raise Exception("failed to connect to arduino after multiple attempts")
            # try to connect to arduino
            for port in ports:
                try:
                    self.arduino = serial.Serial(port, 9600, timeout=1)
                    break
                except:
                    continue
            self.arduino_is_con = True
            self.ar_attempt = 0
            print("connected to arduino !")
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
        try:
            if self.conn is not None: # close connection
                self.conn.close()
            if self.sock is not None: # close socket
                self.sock.close()
        except Exception as e:
            print(f"failed to close conn: {e}")
        try:
            if self.arduino is not None:
                self.arduino.close()
        except Exception as e:
            print(f"failed to close arduino: {e}")
        print("all connections closed")

    
    # run the command receive
    def run(self):
        while True:
            command = self.receive_command()
            if command is None:
                continue
            if command is not None:
                if command == "exit":
                    self.close_all()
                    break
                print(f"received command: {command}")
                self.send_command(command) # send command to arduino
        
    """
    run the command receive

    """

    # reconnect the connections
    def reconnect(self):
        self.close_all()
        self.connect(self.ip, self.port)
        if not self.arduino_is_con:
            self.connect_arduino()
        print("reconnected the connections")

CommandReceive = CommandReceive()
CommandReceive.run()
