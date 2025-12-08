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
        if complexity > self.threshold:
            return self.apply_night_vision(frame)
        else:
            return self.apply_night_vision(frame)

    def night_vision_overlay(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (3, 3), 0)
        gray = cv.equalizeHist(gray)

        night_vision = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
    
        night_vision[:, :, 0] = (night_vision[:, :, 0] * 0.2).astype(np.uint8)
        night_vision[:, :, 1] = (night_vision[:, :, 1] * 0.8    ).astype(np.uint8)
        night_vision[:, :, 2] = 0

        h, w = night_vision.shape[:2]
        kernel_x = cv.getGaussianKernel(w, w/3)
        kernel_y = cv.getGaussianKernel(h, h/3)
        kernel = kernel_y * kernel_x.T
        mask = kernel / kernel.max()

        night_vision = night_vision.astype(np.float32)
        night_vision *= mask[..., np.newaxis]
        night_vision = np.clip(night_vision, 0, 255).astype(np.uint8)

        return night_vision
    
    def night_vision_scan_lines(self, frame):
        result_frame = frame.copy().astype(np.float32)

        result_frame[::3, :, 0] *= 1.5
        result_frame[::3, :] *= 0.7
        
        return np.clip(result_frame.astype(np.uint8), 0, 255)
    
    def night_vision_barrel_distortion(self, frame, intensity):
        h, w = frame.shape[:2]

        j, i = np.meshgrid(np.arange(w), np.arange(h))

        x = ( j - w/2 ) / (w/2)
        y = ( i - h/2 ) / (h/2)

        r = np.sqrt(x*x + y*y)
        distortion = 1.0 + intensity * r**2

        x_distorted = x * distortion
        y_distorted = y * distortion

        map_x = (x_distorted * (w/2)) + w/2
        map_y = (y_distorted * (h/2)) + h/2

        return cv.remap(frame, map_x.astype(np.float32), map_y.astype(np.float32), cv.INTER_LINEAR)
    
    def apply_night_vision(self, frame):
        frame = self.night_vision_overlay(frame)
        frame = self.night_vision_barrel_distortion(frame, 0.1)
        #frame = self._scan_lines(frame)

        return frame