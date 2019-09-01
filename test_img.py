import cv2
import numpy as np 
from Detectors.YoloOpencvDetector import YoloOpencvDetetor
from Detectors import Utils 

# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3.cfg", "./Detectors/YOLO/yolov3_320.weights")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3.cfg", "./Detectors/YOLO/yolov3.weights")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3_tiny.cfg", "./Detectors/YOLO/yolov3_tiny.weights")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov2-voc.cfg", "./Detectors/YOLO/yolov2-voc.weights")
# detector = YoloOpencvDetetor("./Detectors/YOLO/yolov2-tiny.cfg", "./Detectors/YOLO/yolov2-tiny.weights")
# cap = cv2.VideoCapture("/home/vasily/Downloads/DJI_0002.MP4")


detector = YoloOpencvDetetor("./Detectors/YOLO/yolov3_cfg.cfg", "./Detectors/YOLO/yolov3_cfg_8800.weights", CLASSESPath="../datasets/small_danon/names.names")

# cap = cv2.VideoCapture(0)
# out = cv2.VideoWriter()
# fourcc = cv2.VideoWriter_fourcc(*'XVID')

# out = cv2.VideoWriter('output_3.avi',fourcc, 20.0, (1920,1080))
frame_i = 0
# img_paths = """/home/vasily/Projects/datasets/arduino_raspberry_metro/yolo/image086.jpg
# /home/vasily/Projects/datasets/arduino_raspberry_metro/yolo/image013.jpg
# /home/vasily/Projects/datasets/arduino_raspberry_metro/yolo/image044.jpg
# /home/vasily/Projects/datasets/arduino_raspberry_metro/yolo/image084.jpg
# /home/vasily/Projects/datasets/arduino
# _raspberry_metro/yolo/image004.jpg
# /home/vasily/Projects/datasets/arduino_raspberry_metro/yolo/image023.jpg
# /home/vasily/Projects/datasets/arduino_raspberry_metro/yolo/image033.jpg
# """
img_paths = """../datasets/p/IMG_7024.JPG
/home/vasily/Projects/datasets/small_danon/small_yolo/IMG_6993.jpg
/home/vasily/Projects/datasets/small_danon/small_yolo/IMG_6992.jpg
/home/vasily/Projects/datasets/small_danon/small_yolo/IMG_6991.jpg
/home/vasily/Projects/datasets/small_danon/small_yolo/IMG_6989.jpg
/home/vasily/Projects/datasets/small_danon/small_yolo/IMG_6999.jpg
/home/vasily/Projects/datasets/small_danon/small_yolo/IMG_6990.jpg
/home/vasily/Projects/datasets/small_danon/small_yolo/IMG_6998.jpg
"""

img_paths = img_paths.split("\n")
for i in img_paths:
    if len(i) > 3:
        
        frame = cv2.imread(i)
        print(frame.shape)
        # frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
        # frame = cv2.resize(frame, (416, 416))
        boxes, classIDs, confidences = detector.detect(frame, s=(416, 416), conf=0.3, thresh=0.3)
        print(len(boxes))
        frame = Utils.draw_boxes(frame, boxes, classIDs, confidences, detector.CLASSES, COLORS=detector.COLORS)
        # out.write(frame)
        frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow("frame", frame)
        # cv2.imshow("frame", )
        cv2.waitKey(0)
# while True:
#     ret, frame = cap.read()
#     if ret == False:
#         break
#     if frame_i % 5 == 0:

        
#         # frame = cv2.resize(frame, (0, 0), fx=0.7, fy=0.7)
#         # boxes, classIDs, confidences = detector.detect(frame, s=(160, 160))
#         boxes, classIDs, confidences = detector.detect(frame, s=(320, 320), conf=0.05, thresh=0.05)
#         # boxes, classIDs, confidences = detector.detect(frame, s=(416, 416))
#         # boxes, classIDs, confidences = detector.detect(frame, s=(608, 608))
#         # boxes, classIDs, confidences = detector.detect(frame, s=(700, 700))
#         frame = Utils.draw_boxes(frame, boxes, classIDs, confidences, detector.CLASSES, COLORS=detector.COLORS)
#         out.write(frame)
#         cv2.imshow("frame", frame)
        
#     if cv2.waitKey(1) == ord('q'):
#         break
#     frame_i +=1 
# cap.release()
# out.release()