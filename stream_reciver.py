# receiving the stream from the server take a frame and send it to the core.py
import socket
import cv2
import numpy as np

class Reciver:
    def __init__(self):
        self.data = b""
        self.is_connect = False 
        # host and port
        HOST = '0.0.0.0'
        PORT = 5000
        # socket conmnection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.sock.bind((HOST, PORT))
        # listen for the connection
        self.listen()

    def listen(self): # listen for the connection
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        print(f"Connected from {self.addr}")
        self.conn.settimeout(10)
        self.is_connect = True

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
                    chunk = self.conn.recv(4096)
                    if not chunk:
                        print("Connection lost")
                        return None
                    self.data += chunk
                except socket.timeout:
                    # No data yet, continue loop
                    continue
                except Exception as e:
                    print(f"Socket error: {e}")
                    return None
        except Exception as e:
            print(f"Error in recv: {e}")
            return None

    def disconnect(self): # disconnect the connection
        self.is_connect = False
        if self.conn:
            self.conn.close()
            print("connection disconnected")
        if self.sock:
            self.sock.close()
            print("socket disconnected")

    def is_connected(self): # check if the connection is connected
        if self.is_connect:
            return True
        else:
            return False

    def run(self): # run the reciver
        self.listen()
        while self.is_connect:
            frame = self.recv()
            if frame is not None:
                return frame
            else:
                return None
