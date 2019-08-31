import pigpio
import time
import os
class RASPI:
    def __init__(self, init = False, ESC = 17, STEER = 18, ENC = 26):
        if init == True:
            os.system("sudo pigpiod")
        time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error
        # import pigpio

        self.ESC = ESC
        self.STEER = STEER
        self.ENC = ENC
        self.pi = pigpio.pi()
        self.pi.set_servo_pulsewidth(self.ESC, 0)
        self.pi.set_servo_pulsewidth(self.STEER, 0)
        self.pi.set_mode(self.ENC, pigpio.INPUT)
        self.encoder = 0
        self.count_t = False
        self.prev_level = 0
        time.sleep(1)
        # self.pi.set_servo_pulsewidth(ESC, 1500)
        # time.sleep(1)

        
    def calibrate(self):
        self.pi.set_servo_pulsewidth(self.ESC, 0)
        time.sleep(1)
        self.pi.set_servo_pulsewidth(self.ESC, 1500)
        time.sleep(2)
        self.pi.set_servo_pulsewidth(self.ESC, 0)

    def set_motor(self, v):
        self.pi.set_servo_pulsewidth(self.ESC, v)
    
    def set_servo_pwm(self, v):
        self.pi.set_servo_pulsewidth(self.STEER, v)
    def chek_sig(self, q):
        if (q >= 500) and  (q<= 2500):
            return q
        else:
            return int(16.6666666*abs(90))
    def set_servo(self, a):
        self.pi.set_servo_pulsewidth(self.STEER, int(int(16.6666666*a)))

    
    def read_enc(self):
        return self.encoder // 2
    def encoder_callback(self, gpio, level, tick):
        
        if gpio == self.ENC and self.count_t == True:
            # print("Helo", level)
            if level ==0 and self.prev_level==1:
                self.encoder += 1
            self.prev_level = level


    def start_enc(self):
        self.cbA = self.pi.callback(self.ENC, pigpio.EITHER_EDGE, self.encoder_callback)
        self.count_t = True
    def zero_enc(self):
        self.encoder = 0
        self.prev_level = 0
    def stop_enc(self):
        self.cbA.cancel()
        
