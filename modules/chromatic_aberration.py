import cv2 as cv
import numpy as np
import time
import math
import random
import sys
import os 
from colorama import Fore, Back, Style, init

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ChromaticAberration:
    def __init__(self):
        self.name = "ChromeAberration Effect"

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
        
        return self._complex_frame_effect(frame, complexity, intensity = 0.1)

    def _complex_frame_effect(self, frame, complexity, intensity):
        h, w = frame.shape[:2]
    
        j, i = np.meshgrid(np.arange(w), np.arange(h))
        x = (j - w/2) / (w/2)
        y = (i - h/2) / (h/2)
        
        r = np.sqrt(x**2 + y**2)

        safe_r = np.maximum(r, 0.001)
        radial_x = x / safe_r 
        radial_y = y / safe_r 
        
        b_shift = intensity * 2.0 * r**2
        g_shift = intensity * 0.3 * r**2 
        r_shift = intensity * -1.5 * r**2 
        
        x_b = x + b_shift * radial_x
        y_b = y + b_shift * radial_y
        
        x_g = x + g_shift * radial_x
        y_g = y + g_shift * radial_y
        
        x_r = x + r_shift * radial_x  
        y_r = y + r_shift * radial_y
        
        map_x_b = (x_b * (w/2)) + w/2
        map_y_b = (y_b * (h/2)) + h/2
        
        map_x_g = (x_g * (w/2)) + w/2
        map_y_g = (y_g * (h/2)) + h/2
        
        map_x_r = (x_r * (w/2)) + w/2
        map_y_r = (y_r * (h/2)) + h/2
        
        b, g, r = cv.split(frame)
        
        b_shifted = cv.remap(b, map_x_b.astype(np.float32), map_y_b.astype(np.float32), cv.INTER_LINEAR)
        g_shifted = cv.remap(g, map_x_g.astype(np.float32), map_y_g.astype(np.float32), cv.INTER_LINEAR)  
        r_shifted = cv.remap(r, map_x_r.astype(np.float32), map_y_r.astype(np.float32), cv.INTER_LINEAR)
        
        return cv.merge([b_shifted, g_shifted, r_shifted])
    
    def _simple_frame_effect(self, frame, complexity, intensity):
        h, w = frame.shape[:2]
    
        j, i = np.meshgrid(np.arange(w), np.arange(h))
        x = (j - w/2) / (w/2)
        y = (i - h/2) / (h/2)
        
        r = np.sqrt(x**2 + y**2)
        
        safe_r = np.maximum(r, 0.001)
        radial_x = x / safe_r 
        radial_y = y / safe_r 
        
        b_shift = intensity * 2.0 * r**2
        g_shift = intensity * 0.3 * r**2 
        r_shift = intensity * -1.5 * r**2 
        
        x_b = x + b_shift * radial_x
        y_b = y + b_shift * radial_y
        
        x_g = x + g_shift * radial_x
        y_g = y + g_shift * radial_y
        
        x_r = x + r_shift * radial_x  
        y_r = y + r_shift * radial_y
        
        map_x_b = (x_b * (w/2)) + w/2
        map_y_b = (y_b * (h/2)) + h/2
        
        map_x_g = (x_g * (w/2)) + w/2
        map_y_g = (y_g * (h/2)) + h/2
        
        map_x_r = (x_r * (w/2)) + w/2
        map_y_r = (y_r * (h/2)) + h/2
        
        b, g, r = cv.split(frame)
        
        b_shifted = cv.remap(b, map_x_b.astype(np.float32), map_y_b.astype(np.float32), cv.INTER_LINEAR)
        g_shifted = cv.remap(g, map_x_g.astype(np.float32), map_y_g.astype(np.float32), cv.INTER_LINEAR)  
        r_shifted = cv.remap(r, map_x_r.astype(np.float32), map_y_r.astype(np.float32), cv.INTER_LINEAR)
        
        return cv.merge([b_shifted, g_shifted, r_shifted])