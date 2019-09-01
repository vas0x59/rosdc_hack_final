import dlib
import os
import cv2
import xml.etree.ElementTree as pars

dir=r"/home/vasily/Documents/signs/train"
images=[]
annots=[]

ImgNameList = os.listdir(dir + "/img")
print (ImgNameList)

for FileName in ImgNameList:
    print (FileName)
    image=cv2.imread(dir+"/img/"+FileName)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    # iamge = cv2.resize(iamge, )
    img_size = [200, 360]
    image = cv2.resize(image, (img_size[1], img_size[0]))
    OnlyFileName=FileName.split(".")[0]
    #print (OnlyFileName)
    e = pars.parse(dir+"/an/"+OnlyFileName+".xml")
    root=e.getroot()

    #object=root.find("object")
    for object in root.findall("object"):
        object=object.find("bndbox")

        x=int(int(object.find("xmin").text)*(360/640))
        y = int(int(object.find("ymin").text)*(200/360))
        x2 = int(int(object.find("xmax").text)*(360/640))
        y2 = int(int(object.find("ymax").text)*(200/360))

        if (x2 - x) / (y2 - y) < 0.7 and (x2 - x) * (y2 - y) > 401:
            images.append(image)
            annots.append([dlib.rectangle(left=x, top=y, right=x2, bottom=y2)])


options = dlib.simple_object_detector_training_options()
options.be_verbose=True
# options.detection_window_size = (20, 35)
detector = dlib.train_simple_object_detector(images, annots, options)
import time
detector.save(str(time.time())+"signs_2018.svm")
print ("Detector Saved")
