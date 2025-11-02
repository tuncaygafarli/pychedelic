import cv2 as cv
import numpy as np
import time
import math
import random
import simpleaudio as sa

class Calibrator:
    def __init__(self):
        self.frames = []
        self.manipulated_frames = []
        self.complexity = []
        self.threshold = None
        self.start_time = time.time()
        self.effect_history = []
        self.color_palettes = []

    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexity.append(complexity)

        if len(self.complexity) > 10 and self.threshold is None:
            self.threshold = np.median(self.complexity)
            print(f"🎯 Complexity threshold set: {self.threshold:.2f}")

    def calculate_complexity(self, frame):
        small = cv.resize(frame, (160, 90))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return np.var(gray)

    def process_current_frame(self, frame):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 
            
        complexity = self.calculate_complexity(frame)
        
        if complexity > self.threshold:
            return self._complex_frame_effect(frame, complexity)
        else:
            return self._simple_frame_effect(frame, complexity)

    def _complex_frame_effect(self, frame, complexity):
        edges = cv.Canny(frame, 50, 150)
        edges_bgr = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
        return cv.addWeighted(frame, 0.5, edges_bgr, 0.5, 0)
    
    def _simple_frame_effect(self, frame, complexity):
        stylized = cv.stylization(frame, sigma_s=100, sigma_r=0.8) 
        return stylized
