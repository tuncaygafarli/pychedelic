import cv2 as cv
import numpy as np
import time
import math
import random
import sys
import os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class NoneEffect:
    def __init__(self):
        self.name = "None Effect"

        self.frames = []
        self.processed_frames = []

        self.complexities = []
        self.threshold = None

        self.start_time = time.time()

    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexities.append(complexity)

        if len(self.complexities) > 10 and len(self.complexities) % 10 == 0 or self.threshold == None:
            self.threshold = np.mean(self.complexities)
            print(f"Current {self.name} threshold has set to " + str(self.threshold))

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        edges = cv.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
    
        brightness_std = np.std(gray) / 255.0

        complexity = np.log1p(variance) * 0.5 + edge_density * 0.3 + brightness_std * 0.2

        return complexity

    def process_current_frame(self, frame, complexity):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 
        
        return frame