import cv2 as cv
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft, ifft, fftfreq
from scipy import signal
import subprocess
import tempfile
import os
import time
import winsound as player
import librosa

from utils.normalizers import Normalizer
from utils.console_logger import ConsoleLogger

normalizer = Normalizer()
logger = ConsoleLogger()

class AudioProcessor:
    def __init__(self, audio_path=None, sample_rate=44100, buffer_size=1024):
        self.audio_path = audio_path

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

        if audio_path != None:   
            self.sample_rate, audio_raw = wavfile.read(audio_path)

            logger.success(f"Loaded audio: {audio_path}")
            logger.info(f"Sample rate: {self.sample_rate} Hz")
            logger.info(f"Shape of loaded data: {audio_raw.shape if hasattr(audio_raw, 'shape') else 'No shape (not array)'}")
            logger.info(f"Original dtype: {audio_raw.dtype}")

            self.audio_data = audio_raw

            if hasattr(self.audio_data, 'shape'):
                if len(self.audio_data.shape) > 1 and self.audio_data.shape[1] > 1:
                    logger.info(f"Initializing stereo audio: shape {self.audio_data.shape}")
                    if self.audio_data.shape[1] == 2:
                        self.audio_data = np.mean(self.audio_data, axis=1)
                    else:
                        self.audio_data = self.audio_data[:, 0]
                else:
                    logger.info(f"Audio is mono: shape {self.audio_data.shape}")
            else:
                logger.warn("Audio data doesn't have shape attribute")

            # normalizing value between -1 and 1 for safe processing to prevent numerical overflow
            max_val = np.max(np.abs(self.audio_data))
            if max_val > 0:
                self.audio_data = self.audio_data.astype(np.float32) / max_val
        else :
            self.sample_rate=44100
            logger.info("Initializing with video audio.")

    def dump_tempfile(self, video_path):
        temp_dir = tempfile.gettempdir()
        audio_output_path = os.path.join(temp_dir, f"temp_audio_{int(time.time())}.wav")
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vn',
                '-acodec', 'pcm_s16le',
                '-ar', str(self.sample_rate),
                '-ac', '2',
                '-y',
                audio_output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)

            logger.success(f"Audio extracted to: {audio_output_path}")
            return audio_output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to extract audio: {e}")
            return None
        except FileNotFoundError:
            logger.error("ffmpeg not found. Please install ffmpeg.")
            return None

    def play_audio(self, audio_file_path):
        try:
            player.PlaySound(
                audio_file_path, 
                player.SND_FILENAME | player.SND_ASYNC | player.SND_NODEFAULT
            )
            
            logger.success(f"Audio playback started: {os.path.basename(audio_file_path)}")
            return True
        
        except Exception as e:
            logger.error(f"winsound failed: {e}")
        
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
