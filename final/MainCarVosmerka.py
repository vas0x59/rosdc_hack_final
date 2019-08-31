import cv2 as cv
import numpy as np
from servo import *
from func import *
#import threading
#import dlib
# import socket
# import struct
# import pickle


def constrain(val, minv, maxv):
    return min(maxv, max(minv, val))

KP = 0.22
KI = 0
KD = 0.17
last = 0
integral = 0

# constants
SIZE = (400, 300)

RECT = np.float32([[0, 299],
                   [399, 299],
                   [399, 0],
                   [0, 0]])

TRAP = np.float32([[0, 299],
                   [399, 299],
                   [320, 200],
                   [80, 200]])
TRAPINT = np.array(TRAP, dtype=np.int32)

cap = cv.VideoCapture(0)

pi, ESC, STEER = setup_gpio()
control(pi, ESC, 1500, STEER, 90)
time.sleep(1)
timeout = 0
l = 1
r = 0

povor = 0
totl = 1

pid=0

while True:
    try:
        ret, frame = cap.read()
        totl = frame.copy()
        # print(totl)
        # print('totl ready')
        img = cv.resize(frame, SIZE)
        binary = binarize(img)

        perspective = trans_perspective(binary, TRAP, RECT, SIZE)

        left, right = find_left_right(perspective)
        err = 0 - ((left + right) // 2 - 200)
        if abs(right - left) < 100:
            err = last
        # print(err)
        pid = KP * err + KD * (err - last) + KI * integral
        last = err
        integral += err
        integral = constrain(integral, -10, 10)

        control(pi, ESC, 1550, STEER, 90 + pid)
        time.sleep(0.01)

        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     break
    except KeyboardInterrupt:
        control(pi, ESC, 1500, STEER, 90)
        break

# cv.destroyAllWindows()
cap.release()
