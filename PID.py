import time
class PID:
    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.prev_time = time.time()
        self.dt = 0
        self.prev_error = 0
    def calc(self, err):
        self.dt = (time.time()- self.prev_time)
        self.res = self.kP*err + self.kD*(err-self.prev_error)
        self.prev_error = err
        return self.res