import cv2
import numpy as np 
from Detectors.YoloOpencvDetector import YoloOpencvDetetor
from Detectors.SSDOpencvCaffeDetector import SSDOpencvDetetor
from Detectors import Utils 

# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3.cfg", "./Detectors/YOLO/yolov3_320.weights")
detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3_cfg.cfg", "./Detectors/YOLO/yolov3_cfg_8800.weights")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3_tiny_cfg.cfg", "./Detectors/YOLO/yolov3_tiny_cfg_10000.weights")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov2-voc.cfg", "./Detectors/YOLO/yolov2-voc.weights")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov2-tiny.cfg", "./Detectors/YOLO/yolov2-tiny.weights")
# cap = cv2.VideoCapture("/home/vasily/Downloads/DJI_0002.MP4")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3_tiny_cfg.cfg", "./Detectors/YOLO/yolov3_tiny_cfg_8000.weights", CLASSESPath="./Detectors/YOLO/names.names")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3_tiny_cfg.cfg", "./Detectors/YOLO/yolov3_tiny_cfg_300.weights", CLASSESPath="./Detectors/YOLO/names.names")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3_cfg.cfg", "./Detectors/YOLO/yolov3_cfg_8800.weights", CLASSESPath="../datasets/small_danon/names.names")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3_tiny.cfg", "./Detectors/YOLO/yolov3_tiny.weights")
# detector = SSDOpencvDetetor("./Detectors/SSD/MobileNetSSD_deploy.prototxt.txt", "./Detectors/SSD/MobileNetSSD_deploy.caffemodel")
cap = cv2.VideoCapture(0)
# out = cv2.VideoWriter()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_3.avi',fourcc, 20.0, (1920,1080))
frame_i = 0

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    if frame_i % 2  == 0:
        cv2.imshow("in", frame)
        frame = frame[frame.shape[0]//10*4:frame.shape[0]//10*8, frame.shape[1]//10*7:frame.shape[1]]
        # frame = cv2.resize(frame, (0, 0), fx=0.7, fy=0.7)
        # boxes, classIDs, confidences = detector.detect(frame, s=(160, 160))
        boxes, classIDs, confidences = detector.detect(frame, s=(180, 180))
        # boxes, classIDs, confidences = detector.detect(frame, s=(416, 416))
        # boxes, classIDs, confidences = detector.detect(frame, s=(608, 608))
        # boxes, classIDs, confidences = detector.detect(frame, s=(700, 700))
        print(classIDs)
        # frame = Utils.draw_boxes(frame, boxes, classIDs, confidences, detector.CLASSES, COLORS=detector.COLORS)
        out.write(frame)
        cv2.imshow("frame", frame)
        
    if cv2.waitKey(1) == ord('q'):
        break
    frame_i +=1 
cap.release()
out.release()