import cv2 as cv
import numpy as np
import time
import math
import random

class Calibrator:
    def __init__(self):
        self.frames = []
        self.processed_frames = []
        self.complexities = []
        self.threshold = None
        self.start_time = time.time()

    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexities.append(complexity)

        if len(self.complexities) > 10 and self.threshold == None:
            self.threshold = np.mean(self.complexities)
            print("Current Calibrator threshold has set to " + str(self.threshold))

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        return np.log1p(variance)

    def process_current_frame(self, frame):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 

        self.processed_frames.append(frame)  
        complexity = self.calculate_complexity(frame)
        
        if complexity > self.threshold:
            return self._complex_frame_effect(frame, complexity)
        else:
            return self._simple_frame_effect(frame, complexity)

    def _complex_frame_effect(self, frame, complexity):
        edges = cv.Canny(frame, 50, 150)

        h, w = edges.shape[:2]

        edges_rgb = cv.cvtColor(edges, cv.COLOR_GRAY2RGB)
        r_channel = random.randint(0, 255)
        g_channel = random.randint(0, 255)
        b_channel = random.randint(0, 255)

        edges_rgb[edges > 0] = [r_channel, g_channel, b_channel]

        edges_bgr = cv.cvtColor(edges_rgb, cv.COLOR_RGB2BGR)
        return cv.addWeighted(frame, 0.5, edges_bgr, 0.5, 0)
    
    def _simple_frame_effect(self, frame, complexity):
        blurred = cv.GaussianBlur(frame, (5, 5), 0)
        edges = cv.Canny(blurred, 50, 150)

        edges_bgr = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
        return cv.addWeighted(frame, 0.5, edges_bgr, 0.5, 0)