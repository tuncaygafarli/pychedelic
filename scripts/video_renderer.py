import cv2 as cv
import time
import os
import sys
from datetime import datetime
from colorama import Fore, Back, Style, init

from modules.module_manager import ModuleManager

from scripts.configure import Configure

from processors.audio_processor import AudioProcessor

from utils.console_logger import ConsoleLogger

audioproc = AudioProcessor()
init(autoreset=True)

# ------------------- Importing functions from here -------------------

from processors.render_processor import RenderProcessor

def videoRenderer(args):
    
    # ------------------- Initialize managers from here -------------------

    moduleManager = ModuleManager()
    configure = Configure()
    config = configure.load_config()    
    ASSETS_PATH = config["assets"]["assets_videos"]

    # ------------------- Initialize processors from here -------------------

    renderProcessor = RenderProcessor()

    # ------------------- Initialize utils from here -------------------

    logger = ConsoleLogger()

    # ------------------- Initialize I/O from here -------------------

    FILENAME = "video_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".mp4"

    entries = os.listdir(ASSETS_PATH)
    files = [entry for entry in entries if os.path.isfile(os.path.join(ASSETS_PATH, entry))]
    logger.info("Files to be processed in assets folder : " + str(files))

    VIDEO_NAME_IO = input(str(Fore.BLUE + "Enter video name to process : "))

    if(VIDEO_NAME_IO + ".mp4" not in files):
        logger.error(f"Couldn't find the associated file '{VIDEO_NAME_IO}'. Please check the name, or configure proper assets path.")
        return False
    else :
        VIDEO_PATH = ASSETS_PATH + VIDEO_NAME_IO + ".mp4"
        print(Fore.GREEN + f"File found. Processing: {VIDEO_PATH}")

    capture = cv.VideoCapture(ASSETS_PATH + VIDEO_NAME_IO + ".mp4")

    if hasattr(args, "modules"):
        moduleManager.set_module(args.modules[0])
    else:
        logger.warn("No effects specified, using 'None' effect.")
        moduleManager.module_history.append("None")

    logger.info("⚡ Processing frames at MAXIMUM SPEED (no display)...")

    frame_count = 0

    while True:
        isTrue, frame = capture.read()  

        fps_cv = capture.get(cv.CAP_PROP_FPS)
        max_frames = int (fps_cv * 60)

        if not isTrue or frame_count >= max_frames: 
            break
        
        frame_count += 1
        
        if frame_count % 30 == 0:
            elapsed = time.time() - active_module.start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            logger.info(f"📊 Processed {frame_count} frames ({fps:.1f} fps)")
        
        try :
            active_module = moduleManager.get_active_module()
            elapsed_time = time.time() - active_module.start_time

            complexity = active_module.calculate_complexity(frame)
            active_module.add_frame(frame)

            processed_frame = moduleManager.process_frame(frame, complexity, args)
            active_module.processed_frames.append(processed_frame)
        except Exception as error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            line_number = exc_traceback.tb_lineno
            filename = exc_traceback.tb_frame.f_code.co_filename

            logger.error(f"{error} in file {os.path.basename(filename)} : line number {line_number}")
            

        # <--------------------- Debugging text from here --------------------->
        
        if args.debug:
            cv.putText(processed_frame, "TIME PASSED : " + str(round(elapsed_time, 2)) + " SECONDS", (50, 50), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(processed_frame, "FPS : " + str(round(fps_cv, 2)), (50, 100), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(processed_frame, "COMPLEXITY : " + str(round(complexity, 2)), (50, 150), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if active_module.threshold is not None:
                cv.putText(processed_frame, "THRESHOLD : " + str(round(active_module.threshold, 2)), (50, 200), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if complexity > active_module.threshold:
                    cv.putText(processed_frame, "CALIBRATED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv.putText(processed_frame, "UNPROCESSED FRAME", (50, 300), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv.putText(processed_frame, f"EFFECT: {moduleManager.module_history[-1].name}", (50, 350), 
                cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)  

    capture.release()

    if active_module.processed_frames:
        total_time = time.time() - active_module.start_time
        logger.info(f"✅ Processed {len(active_module.processed_frames)} frames in {total_time:.2f}s")
        logger.info(f"📹 Exporting at {len(active_module.processed_frames)/total_time:.1f} fps...")
        renderProcessor.renderFrames(active_module.processed_frames, "build/" + FILENAME, fps_cv)
        logger.success("🎬 Video exported: " + FILENAME)
    else:
        logger.error("❌ No frames processed!")

    logger.success(f"🎉 Done! Open {FILENAME} to see your masterpiece!")