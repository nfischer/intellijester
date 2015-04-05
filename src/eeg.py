"""
Python class to interface with the EEG and receive a value stream
"""

from subprocess import Popen, PIPE
from functools import partial
import sys

if sys.platform[:5] == "linux":
    EXECUTE_JAR = "../outputBStream" # since Linux can't run the real jar file
else:
    EXECUTE_JAR = "java -jar eeg/target/intelligester-1.0.jar"

class EEG:
    def __init__(self):
        # Start the JAR file
        self.p = Popen(EXECUTE_JAR.split(), stdout=PIPE, bufsize=0)
        self.val = 0

        # self.p.stdout.close()
        # self.p.wait()

    def listen_to_process(self):
        for c in iter(partial(self.p.stdout.read, 1), b""):
            self.val = int(c)
        return

    def user_likes_joke(self):
        # Check the current value in the stream
        return (self.val == 1) # must be read-only

    def kill_process(self):
        # self.p.stdout.close()
        self.p.kill()

