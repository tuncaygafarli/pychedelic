import cv2 as cv
import numpy as np
import time
import math
import random
import sys
import os 
from colorama import Fore, Back, Style, init

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.normalizers import Normalizer

normalizer = Normalizer()

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
        
        if complexity > self.threshold:
            return self.grunge_master_complex(frame, complexity)
        else:   
            return self.grunge_master_simple(frame, complexity)

    def grunge_bleach_bypass(self, frame):
        # High contrast + reduced saturation
        lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
        lab[:, :, 0] = cv.equalizeHist(lab[:, :, 0])
        frame = cv.cvtColor(lab, cv.COLOR_LAB2BGR)
    
        # Wash out colors
        frame = cv.addWeighted(frame, 0.8, 
                          np.full_like(frame, 25), 0.2, 0) 
    
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
    
    def dreamify(self, frame, intensity=5):
        result = frame.copy()
        h, w = result.shape[:2]
        
        warm_tint = np.array([0.6, 0.8, 1.0])
        result = result.astype(np.float32)
        result[:,:,0] *= warm_tint[0]  # Less blue
        result[:,:,1] *= warm_tint[1]  # Moderate green
        result[:,:,2] *= warm_tint[2]  # More red
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        result = cv.GaussianBlur(result, (intensity, intensity), 3)
        
        vignette = np.ones((h, w), dtype=np.float32)
        X, Y = np.ogrid[:h, :w]
        center_x, center_y = h/2, w/2
        radius = np.sqrt(center_x**2 + center_y**2)
        dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        vignette = 0.6 + 0.4 * (1 - (dist / radius)**2)
        vignette = np.clip(vignette, 0.4, 1)
        
        for i in range(3):
            result[:,:,i] = (result[:,:,i] * vignette).astype(np.uint8)
        
        noise = np.random.randn(h, w, 3) * intensity
        result = result.astype(np.float32) + noise
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return result

    def grunge_master_complex(self, frame, complexity):
        normalized_complexity = normalizer.perceptual_sigmoid(complexity, len(self.frames) // 2, 'texture', complexity)
        raw_intensity = int(random.randint(1, 3) * normalized_complexity * 5)
        intensity = max(1, min(10, raw_intensity))

        if intensity % 2 == 0:
            intensity += 1

        frame = self.grunge_bleach_bypass(frame)
        frame = self.washed_emo_layers(frame)
        frame = self.emo_bloom_effect(frame)
        frame = self.dreamify(frame, intensity)

        return frame
    
    def grunge_master_simple(self, frame, complexity):
        normalized_complexity = normalizer.sigmoid_normalize(complexity)
        raw_intensity = int(random.randint(1, 3) * normalized_complexity * 5)
        intensity = max(1, min(10, raw_intensity))

        if intensity % 2 == 0:
            intensity += 1
        
        frame = self.grunge_bleach_bypass(frame)
        frame = self.washed_emo_layers(frame)
        frame = self.emo_bloom_effect(frame)
        frame = self.dreamify(frame, intensity)

        return frame