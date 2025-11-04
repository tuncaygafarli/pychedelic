import cv2 as cv
import random
import sys
import math
import time
import numpy as np

class VHS:
    
    def __init__(self):
        self.frames = []
        self.processed_frames = []

        self.complexities = []
        self.threshold = None

        self.start_time = time.time()

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        return np.log1p(variance)
    
    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexities.append(complexity)

        if len(self.complexities) > 10 and self.threshold == None:
            self.threshold = np.median(self.complexities)
            print("Current VHS threshold has set to " + str(self.threshold))

    def process_current_frame(self, frame, complexity):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 
             
        complexity = self.calculate_complexity(frame)
        self.processed_frames.append(frame)  
        
        if complexity > self.threshold:
            return self._apply_vhs(frame)
        else:
            return self._color_bleeding(frame)
        

    def _scan_lines(self, frame):
        dark_lines = frame[::2, :] * 0.2
        dark_lines[:, :, 0] = dark_lines[:, :, 0] * 1.5
        frame[::2, :] = dark_lines
        return frame

    def _color_bleeding(self, frame):
        b, g, r = cv.split(frame)
        h, w = r.shape

        for i in range(h):
            shift = 5 + int(np.sin(i * 0.01) * 2)
            r[i] = np.roll(r[i], shift)
        
            if i % 3 == 0:
                b[i] = np.roll(b[i], -3)
    
        return cv.merge([b, g, r])

    def _apply_vhs(self, frame):
        frame = self._scan_lines(frame)
        frame = self._color_bleeding(frame)
        return frame  