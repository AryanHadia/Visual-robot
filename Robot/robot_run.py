# running the command_receive and stream and command sender to ardunino on raspi3
import subprocess
import time
import signal
import sys
import os
import socket

class RunRobot:
    def __init__(self):
        # camera stream
        self.stream = None
        self.is_streaming = False
        self.Camera_Device = '/dev/video0' # camera device path
        self.PYTHON_VENV = '/home/aryan/myenv/bin/python3'
        self.stream_port = 5000
        self.first_connect = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind(("0.0.0.0", 5000))
        self.server.listen(1)

        print("Waiting for PC...")

        self.conn, self.addr = self.server.accept()

        print(f"Connected: {self.addr}")

        # command receiver
        self.COMMAND_RECEIVER_PATH = '/home/aryan/visual/command_receiver.py'

        # process
        self.cr_process = []

        # signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def cleanup(self):
        try:
            for process in self.cr_process:
                if process.poll() is None:
                    os.killpg(
                    os.getpgid(process.pid),
                    signal.SIGTERM)
                    print(f"terminated process {process.pid}")

        except Exception as e:
            print(f"failed to terminate process: {e}")
        time.sleep(1) # wait for the process to terminate
        for process in self.cr_process:
            try:
                if process.poll() is None:
                    process.kill()
            except Exception as e:
                print(f"failed to kill process: {e}")
                pass
        print("all processes terminated")
        sys.exit(0)


    def signal_handler(self, signal, frame):
        self.cleanup()


    def main(self): # start the stream
        print(f"starting stream. camera is on port {self.stream_port}") 
        stream_cmd = [
    "ffmpeg",
    "-fflags", "nobuffer",
    "-flags", "low_delay",
    "-f", "v4l2",
    "-framerate", "20",
    "-video_size", "640x480",
    "-i", "/dev/video0",
    "-f", "mjpeg",
    "-q:v", "5",
    "-"
]
        p1 = subprocess.Popen(
    stream_cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL
)
        self.cr_process.append(p1)
        print("stream started")
        self.is_streaming = True
        # command receiver
        print("trying to run command receiver")
        cr_cmd = f"{self.PYTHON_VENV} {self.COMMAND_RECEIVER_PATH}"
        p2 = subprocess.Popen(
        [self.PYTHON_VENV, self.COMMAND_RECEIVER_PATH],
        preexec_fn=os.setsid
        )
        print("command receiver started")
        self.cr_process.append(p2)
        # wait for the processes to complete
        while True:
            # if the stream is not streaming
            data = p1.stdout.read(4096)
            if not data:
                break

            # send the data to the client
            self.conn.sendall(data)
        p2.wait()
        print("stream and command receiver terminated")
        self.is_streaming = False

        

robot = RunRobot()
robot.main()
