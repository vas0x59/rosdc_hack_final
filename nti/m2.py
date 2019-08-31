import cv2 
from PID import PID
from RegLine import RegLine
from RASPI import RASPI
import time
import numpy as np
from WebCam import WebCam

servo_pid = PID(0.21, 0, 0)
servo_center = 92.5
servo_angle = servo_center
cross_id = 0
rpi = RASPI(init=True)
sspeed = 1550
rpi.set_servo(servo_angle)
rpi.set_motor(0)
time.sleep(4)
rpi.calibrate()
rpi.set_motor(sspeed)

# cap = cv2.VideoCapture(r"output.avi")
# cap = cv2.VideoCapture(0)
vs = WebCam(0)
vs.start()
# if cap.isOpened() == False:
# print("Cannot open input video")
# exit()

img_size = [200, 360]  # Размеры изображения с которым мы работаем
rpi.start_enc()
def wait_enc(q):
    rpi.zero_enc()
    rpi.read_enc()
    en = 0
    while en < q:
        en = rpi.read_enc()
        print(en)
        time.sleep(0.2)


def stop():
    rpi.set_motor(1450)
    time.sleep(0.6)
    rpi.set_motor(1500)
    time.sleep(3.6)

def go_forward():
    print("forward")
    rpi.set_servo(servo_center)
    rpi.set_motor(sspeed)
    wait_enc(5)

def go_right():
    rpi.set_servo(servo_center-19)
    rpi.set_motor(sspeed)
    wait_enc(3)

def go_left():
    rpi.set_servo(servo_center)
    rpi.set_motor(sspeed)
    # wait_enc(1)
    time.sleep(0.76)
    rpi.set_servo(servo_center+19)
    rpi.set_motor(sspeed)
    wait_enc(3)

def cross(v):
    if v == 0:
        go_forward()
    elif v == -1:
        go_left()
    elif v == 1:
        go_right()

# cross(0)

# time.sleep(3)
rl = RegLine(img_size)


while True:
    # ret, frame = cap.read()
    frame = vs.read()
    # if ret==False:
    #     print("End of video")
    #     cap.release()
    #     cap = cv2.VideoCapture(r"test_videos/output1280.avi")
    #     ret, frame = cap.read()
    frame = cv2.resize(frame, (img_size[1], img_size[0]))
    bin = rl.thresh(frame)

    e, e2 = rl.reg_line(bin, show=False)

    crop = bin[img_size[1]//10*5:img_size[1]//10*6].copy()
    su = np.sum(crop[:, :])
    print("sum:", su)
    if (su > 295065):
        
        print("stop")
        
        stop()
        if cross_id == 1:
            break
        cross(-1)
    servo_angle = servo_center+servo_pid.calc(e*0.725 + e2*0.33)    # 0.27
    # print(servo_angle)
    # cv2.waitKey(1)
    rpi.set_servo(servo_angle)
vs.stop()
rpi.stop_enc()