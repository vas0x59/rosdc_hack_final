import cv2 
from PID import PID
from RegLine import RegLine
from RASPI import RASPI
import time
import numpy as np

servo_pid = PID(0.20, 0, 0)
servo_center = 92.5
servo_angle = servo_center

rpi = RASPI(init=True)
rpi.set_servo(servo_angle)
rpi.set_motor(0)
time.sleep(4)
rpi.calibrate()
rpi.set_motor(1550)

# cap = cv2.VideoCapture(r"output.avi")
cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    print("Cannot open input video")
    exit()

img_size = [200, 360]  # Размеры изображения с которым мы работаем

rl = RegLine(img_size)
while True:
    ret, frame = cap.read()
    # if ret==False:
    #     print("End of video")
    #     cap.release()
    #     cap = cv2.VideoCapture(r"test_videos/output1280.avi")
    #     ret, frame = cap.read()
    frame = cv2.resize(frame, (img_size[1], img_size[0]))
    bin = rl.thresh(frame)

    e, e2 = rl.reg_line(bin, show=False)

    crop = bin[img_size[1]//10*4:img_size[1]//10*5].copy()
    su = np.sum(crop[:, :])
    print("sum:", su)
    if (su > 219555):
        print("stop")
        rpi.set_motor(1450)
        time.sleep(0.5)
        rpi.set_motor(1500)
        time.sleep(3.6)
        rpi.set_servo(servo_center)
        rpi.set_motor(1550)
        time.sleep(2)
    
    
    servo_angle = servo_center+servo_pid.calc(e*0.728 + e2*0.3)    # 0.27
    # print(servo_angle)
    # cv2.waitKey(1)
    rpi.set_servo(servo_angle)