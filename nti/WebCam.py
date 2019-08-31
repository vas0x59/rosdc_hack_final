from threading import Thread
import cv2
# import imutils

class WebCam:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		self.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
		self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed,fr) = self.stream.read()
			img_size = [200, 360]
			fr = cv2.resize(fr, (img_size[1], img_size[0]))
			self.frame = fr

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True