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
            self.threshold = np.mean(self.complexities)
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
            return self._vhs_scan_lines(frame)
        

    def _vhs_scan_lines(self, frame):
        dark_lines = frame[::2, :] * 0.2
        dark_lines[:, :, 0] = dark_lines[:, :, 0] * 1.5
        frame[::2, :] = dark_lines
        return frame

    def _vhs_color_bleeding(self, frame):
        b, g, r = cv.split(frame)
        h, w = r.shape

        for i in range(h):
            shift = 5 + int(np.sin(i * 0.01) * 2)
            r[i] = np.roll(r[i], shift)
        
            if i % 3 == 0:
                b[i] = np.roll(b[i], -2)
    
        return cv.merge([b, g, r])
    
    def _vhs_noise(self, frame):
        h, w = frame.shape[:2]
        
        random_height = random.randint(0, h-1)
        random_width = random.randint(0, w-1)

        radius = random.randint(2, 8)

        # applying the gaussian method from here

        for i in range(max(0, random_height - radius), min(h, random_height+radius)):
            for j in range(max(0, random_width - radius), min(w, random_width+radius)):

                distance = math.sqrt((i - random_height)**2 + (j - random_width)**2)
                probability = max(0, 1 - distance/5)

                if random.random() < probability:
                    frame[i, j] = np.random.randint(0, 255, 3)

        return frame
        
    def _vhs_glitch(self, frame):
        h, w = frame.shape[:2]

        for i in range(h):
            r_channel = random.randint(0, 255)
            g_channel = random.randint(0, 255)
            b_channel = random.randint(0, 255)

            for j in range(w):
                frame[i, j] = [r_channel, g_channel, b_channel]

        return frame
    
    def _vhs_head_clog(self, frame):
        current_index = len(self.processed_frames)
    
        if current_index > 0 and random.random() < 0.8:
            previous_frame = self.processed_frames[current_index - 1]
            
            mix_ratio = random.uniform(0.3, 0.8)
            frame = cv.addWeighted(frame, 1-mix_ratio, previous_frame, mix_ratio, 0)
        
        return frame

    def _apply_vhs(self, frame):
        frame = self._vhs_scan_lines(frame)
        frame = self._vhs_color_bleeding(frame)
        frame = self._vhs_noise(frame)
        frame = self._vhs_head_clog(frame)

        return frame  