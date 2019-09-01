import time
from RASPI import RASPI

rpi = RASPI(init=True)

rpi.calibrate()
rpi.set_servo(92.5)
rpi.set_motor(1550)
time.sleep(2)
rpi.set_motor(1500)
for i in range(80, 100):
    rpi.set_servo(i)
    time.sleep(0.2)