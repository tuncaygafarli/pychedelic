import cv2 as cv
import time
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

from modules.module_manager import ModuleManager
from utils.console_logger import ConsoleLogger

from processors.render_processor import RenderProcessor

def is_window_open(window_name):
    try:
        status = cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE)
        return status > 0
    except:
        return False

def webcamFilter(args):
    moduleManager = ModuleManager()
    logger = ConsoleLogger()

    capture = cv.VideoCapture(0)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    # <--------------------- moduleManager setting effect from here --------------------->

    if hasattr(args, "modules"):
        moduleManager.set_module(args.modules[0])
    else:
        print(Fore.RED + Style.BRIGHT + "Undefined argument.")
        return False
    
    cv.namedWindow('Video Feed', cv.WINDOW_NORMAL)
    while True:
        ret, frame = capture.read()

        if not ret:
            break

        active_module = moduleManager.get_active_module()

        complexity = active_module.calculate_complexity(frame)
        active_module.add_frame(frame)
        processed_frame = moduleManager.process_frame(frame, complexity, args)

        elapsed_time = time.time() - active_module.start_time
        fps_cv = capture.get(cv.CAP_PROP_FPS)
        fps = len(active_module.frames) // elapsed_time if elapsed_time > 0 else 0

        if args.debug:
            logger.info(f"Current {active_module.name} threshold has set to " + Fore.GREEN + Style.BRIGHT + str(active_module.threshold))

            cv.putText(processed_frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv.putText(processed_frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv.putText(processed_frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            if active_module.threshold is not None:
                cv.putText(processed_frame, "THRESHOLD : " + str(round(active_module.threshold, 2)), (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                if complexity > active_module.threshold:
                    cv.putText(processed_frame, "CALIBRATED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                else:
                    cv.putText(processed_frame, "UNPROCESSED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv.putText(processed_frame, f"EFFECT: {moduleManager.effect_history[-1].name}", (50, 350), 
                cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        
        if is_window_open("Video Feed"):
            cv.imshow("Video Feed", cv.flip(processed_frame, 1))
        else :
            logger.terminate("Terminated the video process.")
            break

        key = cv.waitKey(10) & 0xFF
        if key == ord('q'):
            if args.debug:
                logger.terminate("Q key detected!")
            break
        
        if key == ord('s'):
            moduleManager.toggled = not moduleManager.toggled
            continue
        if key == ord('d'):
            args.debug = not args.debug
            continue

    cv.destroyAllWindows()