from time import sleep
import os
import cv2
import math
import numpy as np

class RegLine:
    def __init__(self, img_size = [200, 360]):
        self.img_size = img_size
        self.points = []
        # self.src = np.float32([[20, 200],
        #           [350, 200],
        #           [275, 120],
        #           [85, 120]])
        # self.src = np.float32([[10, 200],
        #           [350, 200],
        #           [275, 120],
        #           [85, 120]])
        # self.src = np.float32([[0, 200],
        #           [360, 200],
        #           [310, 120],
        #           [50, 120]])
        self.src = np.float32([[0, 200],
                  [360, 200],
                  [310, 120],
                  [50, 120]])
        # self.src = np.float32([[0, 299],
        #            [399, 299],
        #            [320, 200],
        #            [80, 200]])

        self.src_draw=np.array(self.src,dtype=np.int32)

        self.dst = np.float32([[0, img_size[0]],
                        [img_size[1], img_size[0]],
                        [img_size[1], 0],
                        [0, 0]])
    def thresh(self, img):
        
        resized = img.copy()
        r_channel=resized[:,:,2]
        binary=np.zeros_like(r_channel)
        binary[(r_channel>180)]=1
        #if show==True:("r_channel",binary)
        
        hls=cv2.cvtColor(resized,cv2.COLOR_BGR2HLS)
        s_channel = resized[:, :, 2]
        binary2 = np.zeros_like(s_channel)
        binary2[(s_channel > 180)] = 1

        allBinary= np.zeros_like(binary)
        allBinary[((binary==1)|(binary2==1))]=255
        
        # th3 = cv2.adaptiveThreshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #     cv2.THRESH_BINARY_INV,5,2)
        return allBinary
    def wrap(self, img):
        M = cv2.getPerspectiveTransform(self.src, self.dst)
        warped = cv2.warpPerspective(img, M, (self.img_size[1],self.img_size[0]), flags=cv2.INTER_LINEAR)
        return warped

    def reg_line(self, img, show=False):
        allBinary = cv2.resize(img.copy(), (self.img_size[1], self.img_size[0]))
        # if show==True:
        #     cv2.imshow("allBinary",allBinary)

        # r_channel=resized[:,:,2]
        # binary=np.zeros_like(r_channel)
        # binary[(r_channel>200)]=1
        # #if show==True:("r_channel",binary)

        # hls=cv2.cvtColor(resized,cv2.COLOR_BGR2HLS)
        # s_channel = resized[:, :, 2]
        # binary2 = np.zeros_like(s_channel)
        # binary2[(r_channel > 160)] = 1

        # allBinary= np.zeros_like(binary)
        # allBinary[((binary==1)|(binary2==1))]=255
        if show==True:
            cv2.imshow("binary",allBinary)



        allBinary_visual=allBinary.copy()
        cv2.polylines(allBinary_visual,[self.src_draw],True,255)
        if show==True:
            cv2.imshow("polygon", allBinary_visual)

        # M = cv2.getPerspectiveTransform(self.src, self.dst)
        warped = self.wrap(allBinary)
        # warped = 
        # warped = cv2.adaptiveThreshold(cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #     cv2.THRESH_BINARY_INV,5,2)
        warped = self.thresh(warped)
        warped = cv2.medianBlur(warped, 3)
        hist = np.sum(perspective[warped.shape[0] // 2:, :], axis=0)
        mid = hist.shape[0] // 2
        left = np.argmax(hist[:mid])
        right = np.argmax(hist[mid:]) + mid
        if left <= 10 and right - mid <= 10:
            right = 399

        # if d:
            # cv.line(perspective, (left, 0), (left, 300), 50, 2)
            # cv.line(perspective, (right, 0), (right, 300), 50, 2)
            # cv.line(perspective, ((left + right) // 2, 0), ((left + right) // 2, 300), 110, 3)

            # cv.imshow('lines', perspective)
        if show==True:
            cv2.imshow("CenterLine",out_img)
        err2 = (left + right) // 2
        err = 0
        if err < -80 or err > 80:
            err = 0
            err2 = 0
        return err, err2, out_img