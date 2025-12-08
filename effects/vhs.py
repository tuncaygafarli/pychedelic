import cv2 as cv
import random
import sys
import math
import time
import numpy as np

from helpers.normalizers import Normalizer

normalizer = Normalizer()

class VHS:

    def __init__(self):
        self.name = "VHS Effect"

        self.frames = []
        self.processed_frames = []

        self.complexities = []
        self.threshold = None

        self.start_time = time.time()

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
            return self.apply_vhs_complex(frame,)
        else:
            return self.apply_vhs_simple(frame)

    # <-------------------- VHS Scan Lines -------------------->

    def vhs_scan_lines(self, frame):
        dark_lines = frame[::3, :] * 0.2
        dark_lines[:, :, 0] = dark_lines[:, :, 0] * 1.5
        frame[::3, :] = dark_lines
        return frame

    # <-------------------- VHS Color Bleeding -------------------->

    def vhs_color_bleeding(self, frame):
        b, g, r = cv.split(frame)
        h, w = r.shape

        for i in range(h):
            shift = 8 + int(np.sin(i * 0.01) * 4)
            r[i] = np.roll(r[i], shift)

            if shift > 0:
                r[i, :shift] = r[i, shift]

            if i % 3 == 0:
                shift_b = -6 + int(np.cos(i * 0.02) * 3)
                b[i] = np.roll(b[i], shift_b)

            if i % 4 == 0:
                shift_g = 2 + int(np.sin(i * 0.01) * 2)
                g[i] = np.roll(g[i], shift_g)

        return cv.merge([b, g, r])

    # <-------------------- VHS Noise -------------------->

    def vhs_noise(self, frame):
        h, w = frame.shape[:2]

        noise_mask = np.random.random((h, w)) < 0.01  # 1% pixels get noise
        frame[noise_mask] = np.random.randint(0, 128, (np.sum(noise_mask), 3))

        return frame

    # <-------------------- VHS Head Clog -------------------->

    def vhs_head_clog(self, frame):
        current_index = len(self.processed_frames)

        if current_index > 0 and random.random() < 0.8:
            previous_frame = self.processed_frames[current_index - 1]

            mix_ratio = random.uniform(0.3, 0.8)
            frame = cv.addWeighted(frame, 1-mix_ratio, previous_frame, mix_ratio, 0)

        return frame

    # <-------------------- VHS Tape Damage -------------------->

    def vhs_tape_damage(self, frame):
        h, w = frame.shape[:2]

        for _ in range(random.randint(1, 5)):
            glitch_y = random.randint(0, h-10)
            glitch_height = random.randint(1, 20)

            shift_amount = random.randint(-50, 50)
            frame[glitch_y:glitch_y+glitch_height] = np.roll(
                frame[glitch_y:glitch_y+glitch_height], shift_amount, axis=1
            )

        return frame

    # <-------------------- VHS Tape Glitch -------------------->

    def vhs_tape_glitch(self, frame):
        h, w = frame.shape[:2]

        glitch_x = random.randint(0, w-50)
        glitch_y = random.randint(0, h-50)
        glitch_width = random.randint(10, 30)
        glitch_height = random.randint(10, 30)

        r_channel = random.randint(0, 10)
        g_channel = random.randint(0, 10)
        b_channel = random.randint(0, 10)

        frame[glitch_y:glitch_y+glitch_height, glitch_x:glitch_x+glitch_width] = [b_channel, g_channel, r_channel]

        return frame

    # <-------------------- VHS Barrel Distortion -------------------->

    def vhs_barrel_distortion(self, frame, intensity=0.1):
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

    # <-------------------- Dynamic Threshold Functions -------------------->

    def apply_vhs_complex(self, frame):
        frame = self.vhs_scan_lines(frame)
        frame = self.vhs_color_bleeding(frame)
        frame = self.vhs_head_clog(frame)
        frame = self.vhs_barrel_distortion(frame)

        if random.random() < 0.000000000000005:
            frame = self.vhs_tape_damage(frame)
            frame = self.vhs_tape_glitch(frame)

        return frame

    def apply_vhs_simple(self, frame):
        frame = self.vhs_scan_lines(frame)
        frame = self.vhs_color_bleeding(frame)
        frame = self.vhs_barrel_distortion(frame)

        if random.random() < 0.00000000001:
            frame = self.vhs_tape_damage(frame)
            frame = self.vhs_tape_glitch(frame)

        return frame
