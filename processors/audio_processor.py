import cv2 as cv
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft

class AudioProcessor:

    def __init__(self, audio_path, sample_rate=44100, buffer_size=1024):
        self.audio_path = audio_path

        self.tempo = 0
        self.beat_timestamps = []
        self.energy_history = []

        self.sample_rate = sample_rate
        self.buffer_size = buffer_size

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

    def analyze_spectrum(self, frame, audio):
        sample_rate, audio_data = wavfile.read(audio)
        self.sample_rate = sample_rate

        n = len(audio_data)

        audio_freq = fft(audio_data)
        audio_freq = audio_freq[0:int(np.ceil((n + 1) / 2.0))]

        magnitude_freq = np.abs(audio_freq)
        magnitude_freq = magnitude_freq / float(n)

        print(magnitude_freq)
