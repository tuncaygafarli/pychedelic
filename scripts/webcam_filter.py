import cv2 as cv
import argparse
import time
import subprocess
import sys
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

from effects.effect_manager import EffectManager
from utils.console_logger import ConsoleLogger

from processors.render_processor import RenderProcessor

def is_window_open(window_name):
    try:
        status = cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE)
        return status > 0
    except:
        return False

def webcamFilter(args):
    effectManager = EffectManager()
    logger = ConsoleLogger()

    capture = cv.VideoCapture(0)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    # <--------------------- EffectManager setting effect from here --------------------->

    if hasattr(args, "effects"):
        effectManager.set_effect(args.effects[0])
    else:
        print(Fore.RED + Style.BRIGHT + "Undefined argument.")
        return False
    
    cv.namedWindow('Video Feed', cv.WINDOW_NORMAL)
    while True:
        ret, frame = capture.read()

        if not ret:
            break

        active_effect = effectManager.get_active_effect()

        complexity = active_effect.calculate_complexity(frame)
        active_effect.add_frame(frame)
        processed_frame = effectManager.process_frame(frame, complexity, args)

        elapsed_time = time.time() - active_effect.start_time
        fps_cv = capture.get(cv.CAP_PROP_FPS)
        fps = len(active_effect.frames) // elapsed_time if elapsed_time > 0 else 0

        if args.debug:
            logger.info("Current {active_effect.name} threshold has set to " + Fore.GREEN + Style.BRIGHT + str(active_effect.threshold))

            cv.putText(processed_frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv.putText(processed_frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv.putText(processed_frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            if active_effect.threshold is not None:
                cv.putText(processed_frame, "THRESHOLD : " + str(round(active_effect.threshold, 2)), (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                if complexity > active_effect.threshold:
                    cv.putText(processed_frame, "CALIBRATED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                else:
                    cv.putText(processed_frame, "UNPROCESSED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv.putText(processed_frame, f"EFFECT: {effectManager.effect_history[-1].name}", (50, 350), 
                cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        
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