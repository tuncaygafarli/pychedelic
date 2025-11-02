import cv2 as cv
import numpy as np
import time
import math
import simpleaudio as sa

VIDEO_PATH = 'assets/video_1.mp4'
AUDIO_FILE = 'assets/worldwide.wav'

capture = cv.VideoCapture(VIDEO_PATH)

class FrameManipulator:
    def __init__(self):
        self.frames = []
        self.manipulated_frames = []
        self.complexity = []
        self.threshold = None
        self.start_time = time.time()
    
    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexity.append(complexity)

        if len(self.complexity) > 10 and self.threshold is None:
            self.threshold = np.median(self.complexity)

    def calculate_complexity(self, frame):
        small = cv.resize(frame, (160, 90))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return np.var(gray)

    def process_current_frame(self, frame):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 
            
        complexity = self.calculate_complexity(frame)
        
        if complexity > self.threshold:
            return self._apply_effect_a(frame, complexity)
        else:
            return self._apply_effect_b(frame, complexity)

    def _apply_effect_a(self, frame, complexity):
        edges = cv.Canny(frame, 50, 150)
        edges_bgr = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
        return cv.addWeighted(frame, 0.5, edges_bgr, 0.5, 0)

    def _apply_effect_b(self, frame, complexity):
        stylized = cv.stylization(frame, sigma_s=500, sigma_r=0.8) 
        return stylized


# Functions

def play_audio(audio_file):
    wave_obj = sa.WaveObject.from_wave_file(AUDIO_FILE)
    play_obj = wave_obj.play()

def save_60fps_video(manipulator, output_path="output_60fps.mp4"):
    if not manipulator.manipulated_frames:
        print("No processed frames to save!")
        return
    
    height, width = manipulator.manipulated_frames[0].shape[:2]
    
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(output_path, fourcc, 60.0, (width, height))
    
    for frame in manipulator.processed_frames:
        out.write(frame)
    out.release()
    print(f"✅ 60fps video saved: {output_path}")

manipulator = FrameManipulator()

apply_calibration = str(input("Apply calibration? Y or N : "))

play_audio(AUDIO_FILE)

save_60fps_video(manipulator, "osamason")

while True:
    isTrue, frame = capture.read()  
    elapsed_time = time.time() - manipulator.start_time
    fps_cv = capture.get(cv.CAP_PROP_FPS)
    fps = len(manipulator.frames) // elapsed_time if elapsed_time > 0 else 0
    complexity = manipulator.calculate_complexity(frame)

    if not isTrue: 
        break
    
    if apply_calibration == "Y" or apply_calibration == "y":
        if manipulator.threshold is not None :
            cv.putText(frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if complexity > manipulator.threshold :
                cv.putText(frame, "CALIBRATED FRAME", (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else :
                cv.putText(frame, "UNPROCESSED FRAME", (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        manipulator.add_frame(frame)
        processed_frame = manipulator.process_current_frame(frame)
        cv.imshow("PROCESSED VIDEO WITH IMAGE CALIBRATION", processed_frame)

    elif apply_calibration == "N" or apply_calibration == "n":
        cv.putText(frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv.imshow("NORMAL VIDEO", frame)
        manipulator.add_frame(frame)
    else :
        print("Undefined argument.")
        break;
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()
