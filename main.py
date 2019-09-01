import cv2 
from PID import PID
from reg_line1 import RegLine
from RASPI import RASPI
import time
import numpy as np
from WebCam import WebCam
servo_pid = PID(0.3, 0, 1)
# servo_pid = PID(0.3, 0, 0.0)
servo_center = 97
servo_p_array = [servo_center for i in range(20)]
servo_angle = servo_center
servo_angle_p = servo_angle
S_SPEED = 1550

rpi = RASPI(init=True)

rpi.calibrate()
rpi.set_servo(servo_angle)
# rpi.set_motor(1550)

running = True
way = [0, 0, 1, -1, 0]
# cap = cv2.VideoCapture(0)
vs = WebCam(0)
vs.start()
if vs.stream.isOpened() == False:
    print("Cannot open input video")
    exit()

img_size = [200, 360]  # Размеры изображения с которым мы работаем

rl = RegLine(img_size)
rpi.set_motor(S_SPEED)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter("time_" + str(int(time.time())) + "output.avi", fourcc, 25, (img_size[1],img_size[0]))

def stop():
    rpi.set_motor(1450)
    time.sleep(0.4)
    rpi.set_motor(1500)
    time.sleep(3.6)

def go_forward():
    print("forward")
    
    # rpi.set_servo((sum(servo_p_array) / len(servo_p_array))*0.3 + servo_center*0.7)
    rpi.set_servo(servo_center)
    rpi.set_motor(S_SPEED)
    time.sleep(3.8)
    st_t = time.time()
    # for i in range(30):
    #     frame = vs.read()
    # while (time.time() - st_t) < 5000:
    #     frame = vs.read()
    #     video_writer.write(frame)
    #     # if ret==False:
    #     #     print("End of video")
    #     #     cap.release()
    #     #     cap = cv2.VideoCapture(r"test_videos/output1280.avi")
    #     #     ret, frame = cap.read()
    #     frame = cv2.resize(frame, (img_size[1], img_size[0]))
    #     th = rl.thresh(frame)
    #     crop = th[img_size[0]//10*5:img_size[0]//10*6, img_size[1]//10*0:img_size[1]//10*2].copy()
    #     su = np.sum(crop[:, :])
    #     print("fsum:", su)
    #     if (su > 10000):
    #         break
    

def go_right():
    print("right")
    rpi.set_servo(servo_center)
    rpi.set_motor(S_SPEED)
    # wait_enc(3)
    time.sleep(1)
    rpi.set_servo(servo_center-16)
    rpi.set_motor(S_SPEED)
    # wait_enc(3)
    time.sleep(0.8)
    st_t = time.time()
    while (time.time() - st_t) < 2000:
        frame = vs.read()
        video_writer.write(frame)
        # if ret==False:
        #     print("End of video")
        #     cap.release()
        #     cap = cv2.VideoCapture(r"test_videos/output1280.avi")
        #     ret, frame = cap.read()
        frame = cv2.resize(frame, (img_size[1], img_size[0]))
        th = rl.thresh(frame)
        crop = th[img_size[0]//10*5:img_size[0], img_size[1]//10*0:img_size[1]//10*3].copy()
        su = np.sum(crop[:, :])
        print("rsum:", su)
        time.sleep(0.01)
        if (su > 8000):
            break
    time.sleep(1)
    rpi.set_servo(servo_center)

def go_left():
    print("left")
    rpi.set_servo(servo_center)
    rpi.set_motor(S_SPEED)
    # wait_enc(3)
    time.sleep(1.3)
    print('ll')
    rpi.set_servo(servo_center+12)
    rpi.set_motor(S_SPEED)
    # wait_enc(3)
    time.sleep(2.7)
    st_t = time.time()
    # while (time.time() - st_t) < 10000:
    #     frame = vs.read()
    #     video_writer.write(frame)
    #     # if ret==False:
    #     #     print("End of video")
    #     #     cap.release()
    #     #     cap = cv2.VideoCapture(r"test_videos/output1280.avi")
    #     #     ret, frame = cap.read()
    #     frame = cv2.resize(frame, (img_size[1], img_size[0]))
    #     th = rl.thresh(frame)
    #     crop = th[img_size[0]//10*5:img_size[0]//10*6, img_size[1]//10*0:img_size[1]//10*3].copy()
    #     su = np.sum(crop[:, :])
    #     print("lsum:", su)
    #     if (su > 8000):
    #         break
    #     time.sleep(0.01)
    time.sleep(0.5)
    rpi.set_servo(servo_center)

def cross(v):
    if v == 0:
        go_forward()
        # pass
    elif v == -1:
        go_left()
        # pass
    elif v == 1:
        go_right()
qwe2 = 0
while running:
    try:
        # ret, frame = cap.read()
        frame = vs.read()
        # if ret==False:
        #     print("End of video")
        #     cap.release()
        #     cap = cv2.VideoCapture(r"test_videos/output1280.avi")
        #     ret, frame = cap.read()
        frame = cv2.resize(frame, (img_size[1], img_size[0]))
        th = rl.thresh(frame)

        e, e2, out_img = rl.reg_line(frame, show=False)
        
        # servo_angle = servo_center+servo_pid.calc(e*0.728 + e2*0.3)    # 0.27
        # servo_angle = servo_center+servo_pid.calc(e*0.725 + e2*0.33)
        # servo_angle = servo_center+servo_pid.calc(e*0.76 + e2*0.33)
        crop = th[img_size[0]//10*6:img_size[0], img_size[1]//10*4:img_size[1]//10*6].copy()
        su = np.sum(crop[:, :])
        print("sum:", su)
        if (su > 255400) and qwe2 != len(way):
            
            print("stop")
            
            stop()
            # cross 
            cross(way[qwe2])
            rpi.set_motor(S_SPEED)
            qwe2 +=1
        if (e == 0) and (e2 == 0):
            servo_angle = servo_angle_p
        else:
            servo_angle = servo_center+servo_pid.calc(e*0.78 + e2*0.38)
        servo_angle = servo_angle*0.9 + servo_angle_p*0.1
        
        # print("err: ", e, e2, servo_angle)
        # print(servo_angle)
        # cv2.waitKey(1)

        rpi.set_servo(servo_angle)
        servo_p_array =  [servo_angle] + servo_p_array[:-1]
        servo_angle_p = servo_angle
        video_writer.write(frame)
    except KeyboardInterrupt:
        rpi.set_motor(1500)
        break
# cap.release()
vs.stop()
video_writer.release()