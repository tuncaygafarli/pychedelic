import cv2 as cv
import math
import random
import numpy as np
import time

class ColorChaosManipulator:
    def __init__(self):
        self.name = "ColorChaos Effect"

        self.frames = []
        self.processed_frames = []

        self.complexities = []
        self.threshold = None

        self.color_palettes = []
        self.effect_history = []

        self.start_time = time.time()
        
        self._generate_color_palettes()

    def _generate_color_palettes(self):
        self.color_palettes = [
            # Neon palette
            [(0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 255, 0)],
            # Warm palette  
            [(255, 100, 0), (255, 200, 0), (255, 50, 50), (200, 100, 0)],
            # Cool palette
            [(0, 100, 255), (100, 0, 255), (0, 200, 255), (50, 50, 255)],
            # Psychedelic palette
            [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
             for _ in range(4)],
            # Monochrome madness
            [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))] * 4
        ]

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        edges = cv.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
    
        brightness_std = np.std(gray) / 255.0

        complexity = np.log1p(variance) * 0.5 + edge_density * 0.3 + brightness_std * 0.2

        return complexity
    
    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexities.append(complexity)

        if len(self.complexities) > 10 and self.threshold == None:
            self.threshold = np.mean(self.complexities)
            print(f"Current {self.name} threshold has set to " + str(self.threshold))

    def process_current_frame(self, frame, complexity):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame
                     
        if complexity > self.threshold:
            return self._complex_frame_effect(frame, complexity)
        else:
            return self.hue_shift(frame)
        
    def _complex_frame_effect(self, frame, complexity):
        effect_type = random.choice([
            'channel_swap', 'color_blast','psychedelic_master'
        ])

        match effect_type:
            case "channel_swap":
                return self.channel_swap(frame)
            case "color_blast":
                return self.color_blast(frame, complexity)
            case "psychedelic_master":
                return self.psychedelic_master(frame, time.time() - self.start_time)
    
    def channel_swap(self, frame):
        b, g, r = cv.split(frame)
        channels = [b, g, r]
        random.shuffle(channels)
        return cv.merge(channels) 
    
    def color_blast(self, frame, complexity):
        intensity = min(0.3, complexity / (self.threshold * 8))
    
        color = np.array([random.randint(0, 255) for _ in range(3)], dtype=np.uint8)
        
        result = frame.astype(np.float32) * (1 - intensity) + color * intensity
        return result.astype(np.uint8)
    

    # ------------------- Defining Psychedelic concepts from here ------------------- 

    def hue_shift(self, frame):
        shift_amount = int(math.sin(time.time() - self.start_time * 0.1) * 30)

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        hue_channel = hsv[:, :, 0]
        
        hue_channel_int = hue_channel.astype(np.int32)
        new_hue = (hue_channel_int + shift_amount) % 180
        
        hsv[:, :, 0] = new_hue.astype(np.uint8)

        return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    
    def sine_distortion(self, frame, time, wave_strength=10):
        h, w = frame.shape[:2]
    
        y_coords, x_coords = np.indices((h, w)) # study this part when you wake up [ vectorized operations ]
        
        wave_x = np.sin(y_coords * 0.05 + time) * wave_strength
        wave_y = np.cos(x_coords * 0.05 + time) * wave_strength
        
        new_x = np.clip(x_coords + wave_x, 0, w-1).astype(np.int32)
        new_y = np.clip(y_coords + wave_y, 0, h-1).astype(np.int32)
        
        return frame[new_y, new_x]
    
    def rgb_split(self, frame, offset):
        b, g, r = cv.split(frame)

        b_shifted = np.roll(b, offset, axis=1)
        g_shifted = np.roll(g, 0, axis=1)
        r_shifted = np.roll(r, -offset, axis=1)

        return cv.merge([b_shifted, g_shifted, r_shifted])
    
    def channel_shifting(self, frame):
        b, g, r = cv.split(frame)
        h, w = r.shape

        for i in range(h):
            shift = 1024 + int(np.sin(i * 0.03) * 2)
            r[i] = np.roll(r[i], shift)
        
            if i % 3 == 0:
                b[i] = np.roll(b[i], -3)
    
        return cv.merge([b, g, r])
    
    def kaleidoscope(self, frame, num_segments=6):
        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        radius = min(center_x, center_y)
        
        y, x = np.ogrid[:h, :w]
        
        dx = x - center_x
        dy = y - center_y
        r = np.sqrt(dx**2 + dy**2)
        theta = np.arctan2(dy, dx) * 180 / np.pi  
        theta = (theta + 360) % 360 
        
        circle_mask = r <= radius
        
        angle_step = 360.0 / num_segments
        normalized_theta = theta % angle_step
        
        source_theta = np.where(normalized_theta <= angle_step / 2, 
                            normalized_theta, 
                            angle_step - normalized_theta)
        
        source_theta = source_theta + (theta // angle_step) * angle_step
        
        source_theta_rad = source_theta * np.pi / 180
        source_x = (r * np.cos(source_theta_rad) + center_x).astype(int)
        source_y = (r * np.sin(source_theta_rad) + center_y).astype(int)
        
        source_x = np.clip(source_x, 0, w-1)
        source_y = np.clip(source_y, 0, h-1)
        
        result = np.zeros_like(frame)
        result[circle_mask] = frame[source_y[circle_mask], source_x[circle_mask]]
        
        return result
    
    def psychedelic_master(self, frame, time_counter):
        result = frame.copy()

        result = self.hue_shift(result) 
        
        wave_strength = 5 + 3 * math.sin(time_counter * 0.03) 
        result = self.sine_distortion(result, time_counter * 0.5)
        
        split_amount = int(2 + math.sin(time_counter * 0.2) * 3) 
        result = self.rgb_split(result, split_amount)

        if random.random() < 0.1:
            result = self.channel_shifting(result)
        
        if int(time_counter) % 120 == 0: 
            segments = random.choice([4, 6, 8])
            result = self.kaleidoscope(result, segments)
        
        return result