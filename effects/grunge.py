import cv2 as cv
import numpy as np
import time
import math
import random
import sys
import os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from effects.vhs import VHS

vhs = VHS()

class Grunge:
    def __init__(self):
        self.name = "Grunge Effect"

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
        
        if complexity > self.threshold:
            return self.grunge_master(frame)
        else:   
            return self.grunge_master(frame)

    def grunge_bleach_bypass(self, frame):
        # High contrast + reduced saturation
        lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
        lab[:, :, 0] = cv.equalizeHist(lab[:, :, 0])
        frame = cv.cvtColor(lab, cv.COLOR_LAB2BGR)
    
        # Wash out colors
        frame = cv.addWeighted(frame, 0.8, 
                          np.full_like(frame, 30), 0.2, 0) 
    
        return frame
    
    def emo_bloom_effect(self, frame):
        bright_mask = cv.inRange(frame, (150, 150, 150), (255, 255, 255))
        
        bloom = cv.GaussianBlur(frame, (35, 35), 0)
        
        result = cv.addWeighted(frame, 0.7, bloom, 0.4, 0)
        
        hsv = cv.cvtColor(result, cv.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
        result = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        
        return result
    
    def washed_emo_layers(self, frame):
        b, g, r = cv.split(frame)
        
        r = np.clip(r.astype(np.float32) * 0.7, 0, 255)
        
        b = cv.GaussianBlur(b, (5, 5), 0)
        b_noise = np.random.normal(0, 15, b.shape).astype(np.float32)
        b = np.clip(b.astype(np.float32) * 0.9 + b_noise, 0, 255)
        
        g = np.clip(g.astype(np.float32) * 0.7, 0, 255)
        
        frame = cv.merge([b.astype(np.uint8), g.astype(np.uint8), r.astype(np.uint8)])
        
        frame = cv.convertScaleAbs(frame, alpha=1.1, beta=10)
        
        return frame
    
    def burnify(self, frame):
        b, g, r = cv.split(frame)

        b_manipulated = np.where(b < 128, np.clip(5 * np.sin((time.time() - self.start_time) * 0.05), 0, 100), np.clip(5 * np.cos((time.time() - self.start_time) * 0.05), 155, 255))
        g_manipulated = np.where(g < 128, np.clip(5 * np.sin((time.time() - self.start_time) * 0.05), 0, 100), np.clip(5 * np.cos((time.time() - self.start_time) * 0.05), 155, 255))
        r_manipulated = np.where(r < 128, np.clip(5 * np.sin((time.time() - self.start_time) * 0.05), 0, 100), np.clip(5 * np.cos((time.time() - self.start_time) * 0.05), 155, 255))

        return cv.merge([b_manipulated.astype(np.uint8), g_manipulated.astype(np.uint8), r_manipulated.astype(np.uint8)])
    
    def grunge_master(self, frame):
        frame = self.grunge_bleach_bypass(frame)
        frame = self.washed_emo_layers(frame)
        frame = self.emo_bloom_effect(frame)

        return frame