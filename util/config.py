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
        cmd = "python train.py --name animate --batch 1 --max_iter 10 --disable_eval --no_wandb --dataroot_sketch ./input/sketch --dataroot_image ./input/image --g_pretrained ./pretrained/g_net.pth --d_pretrained ./pretrained/d_net.pth"
        p = Popen(cmd.split(' '), stdout=PIPE)
        while p.poll() is None:
            pass
        self.T_maxTime = process_time() - beg
        p.terminate()

        print("----- Generate test start ----")
        beg = process_time()
        cmd = "python generate.py --samples 10"
        p = Popen(cmd.split(' '), stdout=PIPE)
        while p.poll() is None:
            pass
        self.G_maxTime = process_time() - beg
        p.terminate()

    def bar(self, mode, time=-1):
        if time == -1:
            return [mode, 100, 100]
        elif mode == "Training":
            return [mode, self.T_time, time]
        elif mode == "Generate":
            return [mode, self.G_time, time]
