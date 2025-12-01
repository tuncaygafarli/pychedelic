import cv2 as cv
import math
import numpy as np
import time

class AudioProcessor:
    
    def __init__(self, audio_path, effect):
        self.audio_path = audio_path

        self.tempo = 0
        self.beat_timestamps = []
        self.energy_history = []

        self.frequency_bands = {
            "bass" : 1.0,
            "mid" : 1.0,
            "high" : 1.0
        }
        self.spectral_centroid = 0

        self.effect_multipliers = {
            'color_blast': 3.0,
            'hue_shift': 1.0, 
            'sine_distortion': 1.0
        }

    def band_multiplication(self, frame, frequency_band, intensity):
            if frequency_band == "bass":
                return np.clip(frame * self.frequency_bands["bass"], 0, 255, None)
        
                

