import cv2 as cv
import argparse
import time
import subprocess
import sys
import os
from datetime import datetime

from effects.effect_manager import EffectManager


def realtimeManipulation(args):
    ASSETS_PATH = 'assets/'

    effectManager = EffectManager()

    entries = os.listdir(ASSETS_PATH)
    files = [entry for entry in entries if os.path.isfile(os.path.join(ASSETS_PATH, entry))]
    print("Files to be processed in assets folder : " + str(files))

    # I/O
    VIDEO_NAME_IO= str(input("Choose the video to process : "))
    VIDEO_PATH = ASSETS_PATH + VIDEO_NAME_IO + ".mp4"

    capture = cv.VideoCapture(VIDEO_PATH)
    output_frames = []
    FRAME_ORDER = 0

    # <--------------------- EffectManager setting effect from here --------------------->

    if hasattr(args, "effects"):
        effectManager.set_effect(args.effects[0])
    else:
        print("Undefined argument.")
        return -1
        
    # <--------------------- Script loop from here --------------------->
    #      
    while True:
        ret, frame = capture.read()

        if not ret:
            capture.set(cv.CAP_PROP_POS_FRAMES, 0)
            continue

        active_effect = effectManager.get_active_effect()

        complexity = active_effect.calculate_complexity(frame)
        active_effect.add_frame(frame)

        processed_frame = effectManager.process_frame(frame, complexity, args)

        elapsed_time = time.time() - active_effect.start_time
        fps_cv = capture.get(cv.CAP_PROP_FPS)
        fps = len(active_effect.frames) // elapsed_time if elapsed_time > 0 else 0


        # <--------------------- Debugging text from here --------------------->
        
        if args.debug:
            cv.putText(processed_frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(processed_frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(processed_frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if active_effect.threshold is not None:
                cv.putText(processed_frame, "THRESHOLD : " + str(round(active_effect.threshold, 2)), (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if complexity > active_effect.threshold:
                    cv.putText(processed_frame, "CALIBRATED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv.putText(processed_frame, "UNPROCESSED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv.putText(processed_frame, f"EFFECT: {effectManager.effect_history[-1].name}", (50, 350), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
        cv.imshow("PROCESSED VIDEO", processed_frame)

        key = cv.waitKey(10) & 0xFF

        if key == ord('q'):
            print("Q key detected!")
            break
        if key == ord('s'):
            effectManager.toggled = not effectManager.toggled
            continue
        if key == ord('d'):
            args.debug = not args.debug
            continue

    cv.destroyAllWindows()
        