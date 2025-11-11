import cv2 as cv
import numpy as np
import time
import math
import random

from processors.face_detection import FateDetector
from effects.color_chaos_manipulator import ColorChaosManipulator

faceDetector = FateDetector()
color_chaos = ColorChaosManipulator()

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

        if len(self.complexities) > 10 and self.threshold == None:
            self.threshold = np.mean(self.complexities)
            print("Current FacialArtifact threshold has set to " + str(self.threshold))

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        return np.log1p(variance)

    def blur_face(self, frame):
        self.name = "Face blur effect"
        faces = faceDetector.detect_face(frame)
        result_frame = frame.copy()

        for (x,y,h,w) in faces:    
            result_frame[y:y+h, x:x+w] = cv.blur(result_frame[y:y+h, x:x+w], ((20, 80)))

        return result_frame
    
    def blur_eye(self, frame):
        self.name = "Eye blur effect"
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
            cv.rectangle(result_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

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
        
    
    def process_current_frame(self, frame, complexity):
        frame = self.blur_face(frame)
        frame = self.blur_eye(frame)
        frame = self.psychedelic_face_shift(frame)
        frame = self.psychedelic_eye_shift(frame)

        return frame

    