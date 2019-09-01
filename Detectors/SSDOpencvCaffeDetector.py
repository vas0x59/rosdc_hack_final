import numpy as np
import time
import cv2
import os
import time

class SSDOpencvDetetor:
    def __init__(self, cfg, wh, CLASSESPath= "./coco.names"):
        self.net = cv2.dnn.readNetFromDarknet(cfg, wh) # "./yolov3-tiny.cfg" "./yolov3-tiny.weights"
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # CLASSESPath = "./coco.names"
        self.CLASSES = open(CLASSESPath).read().strip().split("\n")
        # np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.CLASSES), 3),
            dtype="uint8")


    def detect(self, image, conf=0.4, thresh=0.4, s=(320, 320)):
        (H, W) = image.shape[:2]
        st_t = time.time()
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, s, #416 416
            swapRB=True, crop=False)
        self.net.setInput(blob)
        # start = time.time()
        layerOutputs = self.net.forward(self.ln)
        print("forward_t: ", time.time() - st_t)
        # st_t = time.time()
        boxes = []
        confidences = []
        classIDs = []
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
        
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > conf:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    
                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
        
                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf, thresh)
        bx = []
        cids = [] 
        confs = []
        # print("post_proc_t: ", time.time() - st_t)
        # st_t = time.time()
        if len(idxs) > 0:
            for i in idxs.flatten():
                bx.append(boxes[i])
                cids.append(classIDs[i])
                confs.append(confidences[i])
        # print("sort_t: ", round(time.time() - st_t, 3))
        return bx, cids, confs
