import cv2 as cv
import numpy as np
import time
import os 
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import classes

from effects.tracker import Calibrator
from effects.color_chaos_manipulator import ColorChaosManipulator

from processors.render_processor import RenderProcessor

ASSETS_PATH = 'assets/'
AUDIO_FILE = 'assets/worldwide.wav'

# Functions
calibrator = Calibrator()
cc_manipulator = ColorChaosManipulator()

# I/O
VIDEO_NAME_IO= str(input("Choose the video to process : "))
VIDEO_PATH = ASSETS_PATH + VIDEO_NAME_IO + ".mp4"
apply_calibration = str(input("Apply calibration? Y or N : "))

capture = cv.VideoCapture(VIDEO_PATH)
output_frames = []
FRAME_ORDER = 0

while True:
    isTrue, frame = capture.read()  
    elapsed_time = time.time() - cc_manipulator.start_time
    fps_cv = capture.get(cv.CAP_PROP_FPS)
    fps = len(cc_manipulator.frames) // elapsed_time if elapsed_time > 0 else 0
    complexity = cc_manipulator.calculate_complexity(frame)
    
    if not isTrue: 
        break
    
    if apply_calibration == "Y" or apply_calibration == "y":
        if cc_manipulator.threshold is not None :
            cv.putText(frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if complexity > cc_manipulator.threshold :
                cv.putText(frame, "CALIBRATED FRAME", (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else :
                cv.putText(frame, "UNPROCESSED FRAME", (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cc_manipulator.add_frame(frame)
        processed_calibrator_frame = cc_manipulator.process_current_frame(frame, complexity)
        print("Processed frame number " + str(FRAME_ORDER))
        cv.imshow("PROCESSED VIDEO", processed_calibrator_frame)
        FRAME_ORDER += 1

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
        break
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

cv.destroyAllWindows()
