import cv2 as cv
import numpy
import time

class FateDetector:
    
    def __init__(self):
        self.frames = []
        self.start_time = time.time()
        self.face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect(self, frame):
        faces = self.face_cascade.detectMultiScale(frame, 1.1, 10, minSize=(60, 60))

        return faces