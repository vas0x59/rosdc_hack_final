import cv2
import threading
import time
import numpy as np
import zmq


class Sender:
    def __init__(self, url, image_size=(240, 320, 3)):
        self.running = False
        self.image_size = image_size
        # self.timeout = timeout
        # self.image = np.zeros(self.image_size, np.uint8)
        self.timeouted = False
        self.url = url
        # self.t = threading.Thread(target=self.__receiver_thread)
        # self.t.daemon = True
        self.l_t = -1

    def open(self):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind(self.url)

    def send_img(self, image: np.array):
        
        image_b = image.copy()
        image_b = cv2.resize(image_b, (self.image_size[1], self.image_size[0]))
        # image_b.reshape((0, 1))
        # image_b = np.reshape(image_b, (0, 1))
        byte_array = image_b.tobytes()
        self.publisher.send(byte_array)
        # image_b.
    def close(self):
        self.publisher.close()
        self.context.destroy()