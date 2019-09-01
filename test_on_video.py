import cv2
import numpy as np 
from reg_line1 import *
rl = RegLine()

cap  = cv2.VideoCapture("./video/new/time_1559139557output.avi")


ret = True

while ret:
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv2.resize(frame, (360, 200))
    cv2.imshow("frame", frame)
    th = rl.thresh(frame)
    # th3 = cv2.adaptiveThreshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,\
    #         cv2.THRESH_BINARY_INV,5,2)
    # cv2.imshow("th", th)
    e, e2, _= rl.reg_line(frame, show=True)
    print(e, e2)
    if cv2.waitKey(38) == ord('q'):
        break


cv2.destroyAllWindows()
cap.release()