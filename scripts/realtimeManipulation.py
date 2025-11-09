import cv2 as cv
import argparse
import time
import subprocess
import sys
import os
from datetime import datetime

from effects.tracker import Tracker
from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.vhs import VHS

from effects.effect_manager import EffectManager

from processors.render_processor import RenderProcessor

def realtimeManipulation(args):
    ASSETS_PATH = 'assets/'

    # Effects
    tracker = Tracker()
    cc_manipulator = ColorChaosManipulator()
    vhs = VHS()

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

    if hasattr(args, "effects"):
        if "Tracker" in args.effects:
            effectManager.set_effect("tracker")
        elif "ColorChaos" in args.effects:
            effectManager.set_effect("color_chaos")
        elif "VHS" in args.effects:
            effectManager.set_effect("vhs")
        elif "NightVision" in args.effects:
            effectManager.set_effect("night_vision")
        elif "FacialArtifacts" in args.effects:
            effectManager.set_effect("facial_artifacts")
        elif "ChromaticAberration" in args.effects:
            effectManager.set_effect("chromatic_aberration")
        else:
            print("No effect specified!")
            return
        
    while True:
        ret, frame = capture.read()

        if not ret:
            break

        active_effect = effectManager.get_active_effect()

        complexity = active_effect.calculate_complexity(frame)
        active_effect.add_frame(frame)

        processed_frame = active_effect.process_current_frame(frame, complexity)

        elapsed_time = time.time() - active_effect.start_time
        fps_cv = capture.get(cv.CAP_PROP_FPS)
        fps = len(active_effect.frames) // elapsed_time if elapsed_time > 0 else 0

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

        #print("Processed frame number " + str(FRAME_ORDER))
        cv.imshow("PROCESSED VIDEO", processed_frame)
        FRAME_ORDER += 1

        key = cv.waitKey(10) & 0xFF
        if key == ord('q'):
            print("Q key detected!")
            break

    cv.destroyAllWindows()
        