import cv2 as cv
import numpy as np
import time
import math
import random
import simpleaudio as sa

# Import classes

from effects.calibrator import Calibrator
from functions.save_video import save_60fps_video

VIDEO_PATH = 'assets/video_1.mp4'
AUDIO_FILE = 'assets/worldwide.wav'

capture = cv.VideoCapture(VIDEO_PATH)

# Functions

def play_audio(audio_file):
    wave_obj = sa.WaveObject.from_wave_file(AUDIO_FILE)
    play_obj = wave_obj.play()

calibrator = Calibrator()

apply_calibration = str(input("Apply calibration? Y or N : "))

play_audio(AUDIO_FILE)

save_60fps_video(calibrator, "worldwide_60fps.mp4")

while True:
    isTrue, frame = capture.read()  
    elapsed_time = time.time() - calibrator.start_time
    fps_cv = capture.get(cv.CAP_PROP_FPS)
    fps = len(calibrator.frames) // elapsed_time if elapsed_time > 0 else 0
    complexity = calibrator.calculate_complexity(frame)

    if not isTrue: 
        break
    
    if apply_calibration == "Y" or apply_calibration == "y":
        if calibrator.threshold is not None :
            cv.putText(frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if complexity > calibrator.threshold :
                cv.putText(frame, "CALIBRATED FRAME", (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else :
                cv.putText(frame, "UNPROCESSED FRAME", (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        calibrator.add_frame(frame)
        processed_frame = calibrator.process_current_frame(frame)
        cv.imshow("PROCESSED VIDEO WITH IMAGE CALIBRATION", processed_frame)

    elif apply_calibration == "N" or apply_calibration == "n":
        cv.putText(frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        calibrator.add_frame(frame)
        cv.imshow("NORMAL VIDEO", frame)
    else :
        print("Undefined argument.")
        break;
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()
