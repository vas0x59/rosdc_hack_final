import cv2
import numpy as np
from RegLine import RegLine
from PID import PID
import time

servo_pid = PID(0.6, 0, 0.3)
servo_center = 93
servo_angle = servo_center

cap = cv2.VideoCapture(r"output.avi")

if cap.isOpened() == False:
    print("Cannot open input video")
    exit()

img_size = [200, 360]  # Размеры изображения с которым мы работаем

rl = RegLine(img_size)
while (cv2.waitKey(24) != 27):
    ret, frame = cap.read()
    if ret==False:
        print("End of video")
        cap.release()
        cap = cv2.VideoCapture(r"output.avi")
        ret, frame = cap.read()
    frame = cv2.resize(frame, (img_size[1], img_size[0]))
    bin = rl.thresh(frame)
    # bin = rl.thresh(frame)
    
    # e = rl.reg_line(bin, show=True)
    e, e2 = rl.reg_line(bin, show=True)
    crop = bin[img_size[1]//10*5:img_size[1]//10*6].copy()
    su = np.sum(crop[:, :])
    # print(e, e2 )
    if (su > 220065):
        print("stop")
    servo_angle = servo_center+servo_pid.calc(e*0.8 + e2*0.2)
    # print(servo_angle)
    # print(e, e2,  servo_angle)
    print(su)
        #break

    

    # while (key==0):
    #     cv2.waitKey(0)
    #     key=1

cv2.waitKey(0)