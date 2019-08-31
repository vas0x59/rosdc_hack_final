import cv2 as cv
import numpy as np
import time
from servo import *

def binarize(img, d=0):
    hls = cv.cvtColor(img, cv.COLOR_BGR2HLS)
    #ishodnaya stroka binaryh = cv.inRange(hls, (0, 0, 30), (255, 255, 255))
    binaryh = cv.inRange(hls, (0, 0, 30), (255, 255, 255))

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    binaryg = cv.inRange(gray, 190, 255)

    binary = cv.bitwise_and(binaryg, binaryh)

    if d:
        cv.imshow('hls', hls)
        cv.imshow('hlsRange', binaryh)
        cv.imshow('grayRange', binaryg)
        cv.imshow('gray', gray)
        cv.imshow('bin', binary)
    # ishodnaya stroka return binary
    return binaryg


def trans_perspective(binary, trap, rect, size, d=0):
    M = cv.getPerspectiveTransform(trap, rect)
    perspective = cv.warpPerspective(binary, M, size, flags=cv.INTER_LINEAR)
    if d:
        cv.imshow('perspective', perspective)
    return perspective


def find_left_right(perspective, d=0):
    hist = np.sum(perspective[perspective.shape[0] // 2:, :], axis=0)
    mid = hist.shape[0] // 2
    left = np.argmax(hist[:mid])
    right = np.argmax(hist[mid:]) + mid
    if left <= 10 and right - mid <= 10:
        right = 399

    if d:
        cv.line(perspective, (left, 0), (left, 300), 50, 2)
        cv.line(perspective, (right, 0), (right, 300), 50, 2)
        cv.line(perspective, ((left + right) // 2, 0), ((left + right) // 2, 300), 110, 3)

        cv.imshow('lines', perspective)

    return left, right

# def detect_stop(perspective):
#     hist = np.sum(perspective[], axis=1)
#     maxStrInd = np.argmax(hist)
#     print (int(hist[maxStrInd]/255))
#     if hist[maxStrInd]/255>190:
#         print ("SL detected. PixselC: "+str(int(hist[maxStrInd]/255)) + "Ind: " + str(maxStrInd))
#         if maxStrInd>150:
#             print("Time to stop")
#             return True
#     return False


