import socket
import serial
import serial.tools.list_ports

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
        self.connect_pc()
        self.connect_arduino()

    
    # pc connection
    def scan_ip(self): # scan the ips in the network
        for ip in range(1, 255):
            test_ip = f"192.168.1.{ip}"
            sock = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.1)
                sock.connect((test_ip, 5001))
                sock.close()
                return test_ip
            except Exception as e:
                print(f"failed to connect to {test_ip}: {e}")
                if sock is not None:
                    sock.close()
                continue
        return None

    def connect_pc(self): # try to connect pc with founded ip
        """
        try to connect pc with founded ip
        """
        port = 5001
        while not self.pc_is_con:
            ip = self.scan_ip()
            if ip is None or self.pc_attempt > 3:
                ip = input("please input the ip of the pc: ")
                # try the ip first
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                try:
                    s.connect((ip, port))
                    s.close()
                except Exception as e:
                    print(f"failed to connect to {ip}: {e}")
                    s.close()
                    continue
            # if the ip is valid, try to connect to pc
            port = 5001
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((ip, port))
                self.pc_is_con = True
                self.pc_attempt = 0
                print("connected to pc")
                return
            except Exception as e:
                self.pc_attempt += 1
                print(f"failed to connect to pc: {e}")
                if self.sock is not None:
                    self.sock.close()
                if self.pc_attempt > 3:
                    raise Exception("failed to connect to pc after multiple attempts")
    
    def receive_command(self): # receive command from pc
        """
        receive command from pc
        """
        if self.sock is not None:
            data = self.sock.recv(1024)
            if data:
                return data.decode().strip()
        return None


    # arduino connection
    def find_ar(self): # find the arduino port
        for port in serial.tools.list_ports.comports():
            if "Arduino" in port.description: # arduino port found
                return port.device
            elif "USB" in port.description: # usb port found
                return port.device
        return None

    def connect_arduino(self): # try to connect arduino with founded port
        while not self.arduino_is_con:
            port = self.find_ar()
            if port is None or self.ar_attempt > 3:
                port = input("please input the port of the arduino: ")
            try:
                self.arduino = serial.Serial(port, 9600)
                self.arduino_is_con = True
                self.ar_attempt = 0
                print("connected to arduino")
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
            if self.sock is not None:
                self.sock.close()
        except Exception as e:
            print(f"failed to close socket: {e}")
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
                self.reconnect()
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
        """
        reconnect the connections
        """
        self.connect_pc()
        self.connect_arduino()
        print("reconnected the connections")