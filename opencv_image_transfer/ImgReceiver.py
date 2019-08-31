import cv2
import threading
import time
import numpy as np
import zmq

class Receiver:
    def __init__(self, url, image_size = (240, 320, 3), timeout = 2):
        self.running = False
        self.image_size = image_size
        self.timeout = timeout
        self.image = np.zeros(self.image_size, np.uint8)
        self.timeouted = False
        self.url = url
        self.t = threading.Thread(target=self.__receiver_thread)
        self.t.daemon = True
        self.l_t = -1

    def __receiver_thread(self):
        self.l_t = -1
        while self.running:
            image_bytes = self.receiver.recv()
            self.image = np.frombuffer(image_bytes, dtype='uint8').reshape(self.image_size)
            self.l_t = time.time()

    def open(self):
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.SUB)
        self.receiver.connect(self.url)
        self.receiver.setsockopt_string(zmq.SUBSCRIBE, "")
        self.running = True

        self.t.start()
    def close(self):
        self.running = False
        # wait
        self.t.join()
    def read(self):
        # return 
        self.timeouted = (time.time() - self.l_t) > self.timeout
        return (self.running and (not self.timeouted)), self.image
