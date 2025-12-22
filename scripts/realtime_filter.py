import cv2 as cv
import time
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

from modules.module_manager import ModuleManager

from processors.audio_processor import AudioProcessor

from scripts.configure import Configure

from utils.console_logger import ConsoleLogger

audioproc = AudioProcessor()
init(autoreset=True)

def is_window_open(window_name, audio_dump):
    try:
        status = cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE)
        return status > 0
    except:
        audioproc.delete_temp_audio(audio_dump)
        return False

def realtimeFilter(args):
    # ------------------- Initialize managers / file configurations from here -------------------

    moduleManager = ModuleManager()
    configure = Configure()
    config = configure.load_config()
    
    ASSETS_PATH = config["assets"]["assets_videos"]

    # ------------------- Initialize utils from here -------------------

    logger = ConsoleLogger()

    # ------------------- Initialize I/O from here -------------------

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

    audio_dump = audioproc.dump_tempfile(VIDEO_PATH)
    audioproc.play_audio(audio_dump)

    capture = cv.VideoCapture(VIDEO_PATH)

    if not capture.isOpened():
        logger.error(f"Failed to open video file: {VIDEO_PATH}")
        return False

    width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))

    # <--------------------- moduleManager setting effect from here --------------------->

    if hasattr(args, "modules"):
        moduleManager.set_module(args.modules[0])
    else:
        print("Undefined argument.")
        return -1

    cv.namedWindow('Video Feed', cv.WINDOW_NORMAL)
    cv.resizeWindow('Video Feed', width, height)

    # <--------------------- Script loop from here --------------------->

    while True:
        ret, frame = capture.read()

        if not ret:
            logger.info("Stream ended or failed to read frame.")
            if capture.get(cv.CAP_PROP_POS_FRAMES) > 0:
                capture.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break

        active_module = moduleManager.get_active_module()

        complexity = active_module.calculate_complexity(frame)
        active_module.add_frame(frame)
        processed_frame = moduleManager.process_frame(frame, complexity, args)

        elapsed_time = time.time() - active_module.start_time
        fps_cv = capture.get(cv.CAP_PROP_FPS)
        fps = len(active_module.frames) // elapsed_time if elapsed_time > 0 else 0

        # <--------------------- Debugging text from here --------------------->

        if args.debug:
            logger.info(f"Current {active_module.name} threshold has set to " + Fore.GREEN + Style.BRIGHT + str(active_module.threshold))

            cv.putText(processed_frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (10, 50),
                cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(processed_frame, "FPS : " + str(round(fps_cv, 2)), (10, 100),
                cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(processed_frame, "COMPLEXITY : " + str(round(complexity, 2)), (10, 150),
                cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if active_module.threshold is not None:
                cv.putText(processed_frame, "THRESHOLD : " + str(round(active_module.threshold, 2)), (10, 200),
                    cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if complexity > active_module.threshold:
                    cv.putText(processed_frame, "CALIBRATED FRAME", (10, 300),
                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    cv.putText(processed_frame, "UNPROCESSED FRAME", (10, 300),
                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv.putText(processed_frame, f"EFFECT: {moduleManager.module_history[-1].name}", (10, 350),
                cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if is_window_open("Video Feed", audio_dump):
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
            moduleManager.toggled = not moduleManager.toggled
            continue
        if key == ord('d'):
            args.debug = not args.debug
            continue

    cv.destroyAllWindows()

    audioproc.delete_temp_audio(audio_dump)