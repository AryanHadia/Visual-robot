# receiving the stream from the server take a frame and send it to the core.py
import socket
import cv2
import numpy as np
import time

class Receiver:
    def __init__(self):
        self.data = b""
        self.is_connect = False 
        self.ip = '192.168.137.148'
        # connect
        self.connect_attempts = 0
        self.connect(self.ip)

    def connect(self , ip): # connection
        # making socket
        try:
            print("making socket !")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Done !')
            self.sock.settimeout(3)
            self.sock.connect((ip, 5000))
            print(f"connected by ({ip})")
            self.is_connect = True
            return True
        except:
            print("failed to connect !!")
            self.sock.close()
            self.connect_attempts += 1
            if self.connect_attempts < 4:
                self.connect(ip)
            time.sleep(2)
            

    def recv(self): # receive the stram part by part
        try:
            while True:
                # 1. Search for JPEG markers in buffer
                start = self.data.find(b'\xff\xd8')
                end = self.data.find(b'\xff\xd9', start)
                
                if start != -1 and end != -1:
                    # Complete frame found
                    jpeg_data = self.data[start:end+2]
                    self.data = self.data[end+2:]
                    
                    # Decode to OpenCV image
                    np_arr = np.frombuffer(jpeg_data, np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    return frame
                
                # 2. Need more data
                try:
                    chunk = self.sock.recv(4096)
                    if not chunk:
                        print("Connection lost")
                        return None
                    self.data += chunk
                except socket.timeout:
                    # No data yet, continue loop
                    continue
                except Exception as e:
                    print(f"Socket error: {e}")
                    self.reconnect()
                    return None
        except Exception as e:
            if self.sock:
                self.sock.close()
                self.sock = None
            print(f"Error in recv: {e}")
            return None

    def disconnect(self): # disconnect the connection
        self.is_connect = False
        self.connect_attempts = 0
        if self.sock: # close the socket
            self.sock.close()
            print("socket disconnected")

    def is_connected(self): # check if the connection is connected
        if self.is_connect:
            return True
        else:
            return False

    def reconnect(self): # reconnect the connection
        self.disconnect() # disconnect
        # reconnect
        while not self.connect(self.ip):
            print("Retrying...")
            time.sleep(2)
