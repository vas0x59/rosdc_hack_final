import cv2
import dlib
import numpy as np
import cv2 as cv
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model
# # model = load_model('sv3.keras')
# from tensorflow.keras.models import model_from_json
# f = open('my_model_a.json', 'r')
# json_string = f.readline()
# f.close()
# model = model_from_json(json_string)
# model.load_weights('my_model_weights.h5')

model_detector = dlib.simple_object_detector("1567321639signs_2018.svm")

cam=cv2.VideoCapture(2)
labels = ['pedestrain', 'stop']
# def predict_label(image):
#     image = cv2.resize(image, (38, 38))
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     image = img_to_array(image)
#     image = np.expand_dims(image, axis=0)
#     image = np.array(image, dtype="float") / 255.0
#     pre = model.predict(image)[0]
#     i_max = 0
#     for i in range(len(pre)):
#         if pre[i_max] < pre[i]:
#             i_max = i
#     return labels[i_max]

while (1):
    ret,frame=cam.read()
    frame = cv2.resize(frame, (360, 200))
    boxes = model_detector(frame)
    for box in boxes:
        print (box)
        (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
        crop = frame[y:yb, x:xb].copy()
        # label = predict_label(crop)
        # print(label)
        cv2.imshow("crop", crop)
        cv2.rectangle(frame, (x, y), (xb, yb), (0, 0, 255), 2)

    cv2.imshow("Frame",frame)

    key = cv2.waitKey(1)
    if cv2.waitKey(1)==ord('q'):
        break
