# running the command_receive and stream and command sender to ardunino on raspi3
import subprocess
import time
import signal
import sys
import os

class RunRobot:
    def __init__(self):
        # camera stream
        self.stream = None
        self.is_streaming = False
        self.Camera_Device = '/dev/video0' # camera device path
        self.PYTHON_VENV = '/home/aryan/myenv/bin/python3'
        self.stream_port = 5000
        self.first_connect = False

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
        stream_cmd = f"ffmpeg -fflags nobuffer -flags low_delay -f v4l2 -framerate 30 -video_size 640x480 -input_format mjpeg -i /dev/video0 -an -f mjpeg -q:v 5 - 2>/dev/null | nc -l -p {self.stream_port}"
        p1 = subprocess.Popen(stream_cmd, shell=True, preexec_fn=os.setsid)
        self.cr_process.append(p1)
        print("stream started")
        self.is_streaming = True
        # command receiver
        print("trying to run command receiver")
        cr_cmd = f"{self.PYTHON_VENV} {self.COMMAND_RECEIVER_PATH}"
        p2 = subprocess.Popen(cr_cmd, shell=True, preexec_fn=os.setsid)
        print("command receiver started")
        self.cr_process.append(p2)
        # wait for the processes to complete
        while True:
            # if the stream is not streaming
            time.sleep(1)
        p2.wait()
        print("stream and command receiver terminated")
        self.is_streaming = False

        

robot = RunRobot()
robot.main()
