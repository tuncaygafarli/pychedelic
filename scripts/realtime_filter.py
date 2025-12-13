import cv2 as cv
import argparse
import time
import sys
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

from effects.effect_manager import EffectManager
from utils.console_logger import ConsoleLogger

init(autoreset=True)

def is_window_open(window_name):
    try:
        status = cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE)
        return status > 0
    except:
        return False

def realtimeFilter(args):
    # ------------------- Initialize managers from here -------------------

    effectManager = EffectManager()

    # ------------------- Initialize utils from here -------------------

    logger = ConsoleLogger()

    # ------------------- Initialize file from here -------------------
    ASSETS_PATH = 'assets/video/'

    entries = os.listdir(ASSETS_PATH)
    files = [entry for entry in entries if os.path.isfile(os.path.join(ASSETS_PATH, entry))]
    logger.info("Files to be processed in assets folder : " + str(files))

    # I/O
    VIDEO_NAME_IO= str(input(Fore.BLUE + "Choose the video to process : "))
    
    if(VIDEO_NAME_IO + ".mp4" not in files):
        logger.error(f"Couldn't find the associated file '{VIDEO_NAME_IO}'. Please check the name, or configure proper assets path.")
        return False
    else :
        VIDEO_PATH = ASSETS_PATH + VIDEO_NAME_IO + ".mp4"
        logger.success(f"File found. Processing: {VIDEO_PATH}")

    capture = cv.VideoCapture(VIDEO_PATH)

    if not capture.isOpened():
        logger.error(f"Failed to open video file: {VIDEO_PATH}")
        return False
    
    width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))

    # <--------------------- EffectManager setting effect from here --------------------->

    if hasattr(args, "effects"):
        effectManager.set_effect(args.effects[0])
    else:
        print("Undefined argument.")
        return -1
        
    cv.namedWindow('Video Feed', cv.WINDOW_NORMAL)
    cv.resizeWindow('Video Feed', width, height)
    
    # <--------------------- Script loop from here --------------------->

    while True:
        ret, frame = capture.read()

        if not ret:
            capture.set(cv.CAP_PROP_POS_FRAMES, 0)
            continue

        active_effect = effectManager.get_active_effect()

        complexity = active_effect.calculate_complexity(frame)
        active_effect.add_frame(frame)

        if args.debug:
            logger.info("Current {active_effect.name} threshold has set to " + Fore.GREEN + Style.BRIGHT + str(active_effect.threshold))

        processed_frame = effectManager.process_frame(frame, complexity, args)

        elapsed_time = time.time() - active_effect.start_time
        fps_cv = capture.get(cv.CAP_PROP_FPS)
        fps = len(active_effect.frames) // elapsed_time if elapsed_time > 0 else 0

        # <--------------------- Debugging text from here --------------------->
        
        if args.debug:
            cv.putText(processed_frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (10, 50), 
                cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(processed_frame, "FPS : " + str(round(fps_cv, 2)), (10, 100), 
                cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(processed_frame, "COMPLEXITY : " + str(round(complexity, 2)), (10, 150), 
                cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if active_effect.threshold is not None:
                cv.putText(processed_frame, "THRESHOLD : " + str(round(active_effect.threshold, 2)), (10, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if complexity > active_effect.threshold:
                    cv.putText(processed_frame, "CALIBRATED FRAME", (10, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    cv.putText(processed_frame, "UNPROCESSED FRAME", (10, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
            cv.putText(processed_frame, f"EFFECT: {effectManager.effect_history[-1].name}", (10, 350), 
                cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if is_window_open("Video Feed"):
            cv.imshow("Video Feed", processed_frame)
        else :
            if args.debug:
                logger.terminate("Terminated the video process.")
            break

        key = cv.waitKey(10) & 0xFF
        if key == ord('q'):
            if args.debug:
                logger.terminate("Q key detected!")
            break
        if key == ord('s'):
            effectManager.toggled = not effectManager.toggled
            continue
        if key == ord('d'):
            args.debug = not args.debug
            continue

    cv.destroyAllWindows()