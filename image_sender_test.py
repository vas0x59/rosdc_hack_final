import cv2
from opencv_image_transfer.ImgSender import Sender

sender = Sender("tcp://0.0.0.0:1258")

sender.open()

cap = cv2.VideoCapture(0)

i = 0

while True:
    re, image = cap.read()
    if i == 3:
        sender.send_img(image)
        i = 0
    i+=1
    # cv2.waitKey(1)