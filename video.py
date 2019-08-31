#!/usr/bin/env
import cv2


if __name__ == "__main__":
    # find the webcam
    capture = cv2.VideoCapture(0)
    w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # video recorder
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter("output.avi", fourcc, 25, (w, h))

    # record video
    while (capture.isOpened()):
        ret, frame = capture.read()
        if ret:
            video_writer.write(frame)
            #cv2.imshow('Video Stream', frame)

        else:
            break

    capture.release()
    video_writer.release()
    #cv2.destroyAllWindows()
