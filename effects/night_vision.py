import cv2 as cv
import numpy as np
import random
import time

class NightVision:
    def __init__(self):
        self.name = "NightVision Effect"

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
            print("Current Tracker threshold has set to " + str(self.threshold))

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        return np.log1p(variance)

    def process_current_frame(self, frame, complexity):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 

        complexity = self.calculate_complexity(frame)
        
        if complexity > self.threshold:
            return self._apply_night_vision_look(frame)
        else:
            return self._artifacts_enabled(frame)

        def _apply_night_vision_look():
            return 0