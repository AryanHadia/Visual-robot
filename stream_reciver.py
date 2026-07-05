# receiving the stream from the server take a frame and send it to the core.py
import socket
import cv2
import numpy as np
import time

class Reciver:
    def __init__(self):
        self.data = b""
        self.is_connect = False 
        # host and port
        self.host = '0.0.0.0'
        self.port = 5000
        self.conn = None
        # connect
        con = self.connect()
        while con == False:
            con = self.connect()

    def connect(self): # connection
        # making socket
        try:
            print("making socket !")
            self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            print("done")
            self.sock.bind((self.host , self.port))
            self.sock.listen()
            print("listening !")
            self.conn, addr = self.sock.accept()
            print(f"connected by ({addr})")
            return True
        except:
            print("failed to connect !!")
            self.conn.close()
            self.sock.close()
            time.sleep(4)
            

    def recv(self): # receive the stram part by part
        try:
            print('try to receive !!')
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
