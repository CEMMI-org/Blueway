import time
from lighting.config import M,N

class LightingPattern(object):
    duration = 10
    stop = False

    def __init__(self, args):
        if len(args) > 0: self.duration = float(args[0])

    def display_pattern(self,t):
        raise NotImplementedError

    def illuminate(self):
        self.stop = False
        t0 = time.time()
        t = time.time()
        while t < t0 + self.duration and not self.stop:
            self.display_pattern(t)
            t = time.time()

    def stop(self):
        self.stop = True
