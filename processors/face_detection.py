import cv2 as cv
import time

class FateDetector:
    
    def __init__(self):
        self.frames = []
        self.start_time = time.time()
        self.face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
        self.eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')

    def detect_face(self, frame):
        faces = self.face_cascade.detectMultiScale(frame, 1.1, 10, minSize=(60, 60))

        return faces
    
    def detect_eyes(self, frame):
        eyes = self.eye_cascade.detectMultiScale(frame, 1.1, 10, minSize=(20, 20))

        return eyes