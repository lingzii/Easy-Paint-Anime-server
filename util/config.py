from subprocess import Popen, PIPE
from time import process_time


class Config:
    def __init__(self):
        self.task = None
        self.state = None
        self.T_time = None
        self.G_time = None
        self.T_maxTime = None
        self.G_maxTime = None
        self.recordFirstTime()
        print("----- Server initialized -----")
    
    def recordFirstTime(self):
        print("----- Training test start ----")
        beg = process_time()
        cmd = "python generate.py --samples 1"
        p = Popen(cmd.split(' '), stdout=PIPE)
        while p.poll() is None:
            pass
        self.T_maxTime = process_time() - beg
        p.terminate()

        print("----- Generate test start ----")
        beg = process_time()
        cmd = "python generate.py --samples 1"
        p = Popen(cmd.split(' '), stdout=PIPE)
        while p.poll() is None:
            pass
        self.G_maxTime = process_time() - beg
        p.terminate()