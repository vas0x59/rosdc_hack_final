import cv2
import numpy as np 
from reg_line1 import *
rl = RegLine()

cap  = cv2.VideoCapture("video/output.avi")


ret = True

while ret or (cv2.waitKey(1) != ord('q')):
    ret, frame = cap.read()
    if ret == False:
        break
    # frame = cv2.resize(frame, (360, 200))
    # cv2.imshow("frame", frame)
    # th = rl.thresh(frame)
    # cv2.imshow("th", th)
    # rl.reg_line(th, show=True)
    

cv2.destroyAllWindows()
cap.release()