import cv2 as cv
import numpy as np
import time
import math
import random
from colorama import Fore, Back, Style, init

from processors.face_detection import FaceDetector
from effects.color_chaos import ColorChaos

faceDetector = FaceDetector()
color_chaos = ColorChaos()

class FacialArtifacts:

    def __init__(self):
        self.name = None

        self.frames = []
        self.processed_frames = []

        self.complexities = []
        self.threshold = None

        self.start_time = time.time()

        self.stored_image_path = None

    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexities.append(complexity)

        if len(self.complexities) > 10 and len(self.complexities) % 10 == 0 or self.threshold == None:
            self.threshold = np.mean(self.complexities)
            print(Fore.YELLOW + f"Current {self.name} threshold has set to " + Fore.GREEN + Style.BRIGHT + str(self.threshold))

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        edges = cv.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size

        brightness_std = np.std(gray) / 255.0

        complexity = np.log1p(variance) * 0.5 + edge_density * 0.3 + brightness_std * 0.2

        return complexity

    def blur_face(self, frame):
        self.name = "Face blurring effect"
        faces = faceDetector.detect_face(frame)
        result_frame = frame.copy()

        for (x,y,h,w) in faces:
            result_frame[y:y+h, x:x+w] = cv.blur(result_frame[y:y+h, x:x+w], ((20, 80)))

        return result_frame

    def blur_eye(self, frame):
        self.name = "Eye blurring effect"
        eyes = faceDetector.detect_eyes(frame)
        result_frame = frame.copy()

        for (x,y,h,w) in eyes:
            result_frame[y:y+h, x:x+w] = cv.blur(result_frame[y:y+h, x:x+w], ((20, 80)))

        return result_frame

    def rgb_split(self, frame):
        b, g, r = cv.split(frame)
        g_shift = math.floor(5 * np.sin((self.start_time - time.time()) * 0.01 ))

        shift = 10
        b_shifted = np.roll(b, shift, axis=1)
        g_shifted = np.roll(g, g_shift, axis=1)
        r_shifted = np.roll(r, -shift, axis=1)

        frame = cv.merge([b_shifted, g_shifted, r_shifted])
        return frame

    def scan_face(self, frame):
        faces = faceDetector.detect_face(frame)
        result_frame = frame.copy()

        for (x, y, h, w) in faces:
            face_region = result_frame[y:y+h, x:x+w]

            processed_face = self.rgb_split(face_region)

            result_frame[y:y+h, x:x+w] = processed_face

        return result_frame

    def psychedelic_face_shift(self, frame):
        self.name = "Psychedelic face shift effect"
        faces = faceDetector.detect_face(frame)
        result_frame = frame.copy()

        for (x, y, h, w) in faces:
            shift_amount = 3 + 5 * np.sin(time.time() - self.start_time * 0.01)
            result_frame[y:y+h, x:x+w] = result_frame[y:y+h, x:x+w] * shift_amount

            result_frame[y:y+h, x:x+w] = np.roll(result_frame[y:y+h, x:x+w], shift_amount, axis = 1)

        return result_frame

    def psychedelic_eye_shift(self, frame):
        self.name = "Psychedelic eye shift effect"
        eyes = faceDetector.detect_eyes(frame)
        result_frame = frame.copy()

        for (x, y, h, w) in eyes:
            shift_amount = 3 + 5 * np.sin(time.time() - self.start_time * 0.01)
            result_frame[y:y+h, x:x+w] = result_frame[y:y+h, x:x+w] * shift_amount

            result_frame[y:y+h, x:x+w] = np.roll(result_frame[y:y+h, x:x+w], shift_amount, axis = 1)

        return result_frame

    def mark_face(self, frame):
        faces = faceDetector.detect_face(frame)
        result_frame = frame.copy()

        for (x,y,h,w) in faces:
            text_x = x + w // 2
            text_y = y - 10

            cv.rectangle(result_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(result_frame, "Human", (text_x, text_y),
                cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        return result_frame

    def face_filter(self, frame):
        faces = faceDetector.detect_face(frame)
        result_frame = frame.copy()

        if self.stored_image_path is None:
            self.stored_image_path = input("Enter image name to combine with: ")

        for (x,y,h,w) in faces:
            try :
                extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']

                for ext in extensions:
                    img_path = f"assets/{self.stored_image_path}{ext}"
                    img = cv.imread(img_path)
                    if img is not None:
                        break

                if img is None:
                    print(f"Error: Could not load image {self.stored_image_path} with any common extension")
                    continue

                img_resized = cv.resize(img, (w, h))

                region = result_frame[y:y+h, x:x+w]
                blended_region = cv.addWeighted(region, 0, img_resized, 1, 0)

                result_frame[y:y+h, x:x+w] = blended_region

            except Exception as e:
                print(f"Error applying face filter: {e}")
                continue

        return result_frame

    def detect_smile(self, frame):
        smile = faceDetector.detect_smile(frame)
        result_frame = frame.copy()

        for (x, y, h, w) in smile:
            smile_area = smile[y:y+h, x:x+w]
            cv.rectangle(result_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return result_frame

    def process_current_frame(self, frame, complexity):
        frame = self.blur_face(frame)
        frame = self.blur_eye(frame)
        frame = self.psychedelic_face_shift(frame)
        frame = self.psychedelic_eye_shift(frame)

        return frame
