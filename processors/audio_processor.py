import cv2 as cv
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft, ifft, fftfreq
from scipy import signal
import librosa

from utils.normalizers import Normalizer

normalizer = Normalizer()

class AudioProcessor:
    def __init__(self, audio_path, sample_rate=44100, buffer_size=1024):
        self.audio_path = audio_path

        self.sample_rate, audio_raw = wavfile.read(audio_path)

        print(f"Loaded audio: {audio_path}")
        print(f"Sample rate: {self.sample_rate} Hz")
        print(f"Shape of loaded data: {audio_raw.shape if hasattr(audio_raw, 'shape') else 'No shape (not array)'}")
        print(f"Original dtype: {audio_raw.dtype}")

        self.audio_data = audio_raw

        self.tempo = 0
        self.beat_timestamps = []
        self.energy_history = []

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

        # TODO :  FIX ME ( DONE  )
        if self.audio_data.shape > 1:
            print("Initializing stereo audio : {self.audio_data}")
            self.audio_data = self.audio.data[:len(self.audio_data)//2]

        # normalizing value between -1 and 1 for safe processing to prevent numerical overflow
        max_val = np.max(np.abs(self.audio_data))
        if max_val > 0:
            self.audio_data = self.audio_data.astype(np.float32) / max_val

    def band_multiplication(self, frame, frequency_band, intensity):
            if frequency_band == "bass":
                return np.clip(frame * self.frequency_bands["bass"], 0, 255, None)

    def analyze_freq_content(self):
        n = len(self.audio_data)

        window = signal.windows.hann(n)
        windowed_audio = self.audio_data * window

        ## apply Fourier transitions from here
        audio_fft = fft(windowed_audio)

        frequencies = fftfreq(n, 1/self.sample_rate)[:n//2]
        magnitudes = np.abs(audio_fft[:n//2]) / n

        magnitudes_db = 20 * np.log10(magnitudes + 1e-10)

        return frequencies, magnitudes_db

    def bass_energy(self, frame):
        frequencies, decibels = self.analyze_freq_content()
        intensity = normalizer.sigmoid_normalize(frame)

        return self.band_multiplication(frame, frequencies, intensity)
