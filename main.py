import cv2 as cv
import argparse
import time
import subprocess
import sys
from datetime import datetime

from effects.calibrator import Calibrator
from effects.color_chaos_manipulator import ColorChaosManipulator


# ---------------------- Argument parser implementation below here ----------------------


parser = argparse.ArgumentParser(description="🎨 OpenCV Visual Artifacts - Transform your videos with psychedelic effects and mathematical transformations! 🌈✨",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
🌟 Examples:
  python main.py -rtm enable          🎥 Live webcam psychedelic effects
  python main.py -render enable       🎬 Process video files with visual artifacts
  
🎯 Features:
  • Real-time complexity analysis
  • Dynamic effect triggering  
  • Psychedelic color transformations
  • Mathematical frame distortions
    """)

parser.add_argument(
    "-rtm", "--realtime", 
    type=str,
    choices=['enable'],
    help="🎥 Enable realtime manipulation mode (webcam required)"
)

parser.add_argument(
    "-render", "--render", 
    type=str,
    choices=['enable'], 
    help="🎬 Render video files with visual artifacts"
)

args = parser.parse_args()

# ---------------------- Definitions of effects below here ----------------------

calibrator = Calibrator()
cc_manipulator = ColorChaosManipulator()

# ---------------------- Implementations of tests below here ----------------------

def realtimeManipulation():
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


def renderVideo():
    ASSETS_PATH = '../assets/'
    AUDIO_FILE = 'assets/worldwide.wav'
    FILENAME = "video_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".mp4"
    VIDEO_NAME_IO = input(str("Enter video name to process : "))

    capture = cv.VideoCapture(ASSETS_PATH + VIDEO_NAME_IO + ".mp4")
    calibrator = Calibrator()
    cc_manipulator = ColorChaosManipulator()

    apply_calibration = str(input("Apply calibration? Y or N : "))

    output_frames = []

    print("⚡ Processing frames at MAXIMUM SPEED (no display)...")

    frame_count = 0
    start_time = time.time()

    while True:
        isTrue, frame = capture.read()  
        fps_cv = capture.get(cv.CAP_PROP_FPS)

        if not isTrue: 
            break
        
        frame_count += 1
        
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            print(f"📊 Processed {frame_count} frames ({fps:.1f} fps)")
        
        complexity = cc_manipulator.calculate_complexity(frame)
        
        if apply_calibration == "Y" or apply_calibration == "y":
            calibrator.add_frame(frame)
            processed_calibrator_frame = calibrator.process_current_frame(frame)
            cc_manipulator.add_frame(processed_calibrator_frame)
            processed_cc_manipulator_frame = cc_manipulator.process_current_frame(processed_calibrator_frame, complexity)
            output_frames.append(processed_cc_manipulator_frame)
            
        elif apply_calibration == "N" or apply_calibration == "n":
            cc_manipulator.add_frame(frame)
            output_frames.append(frame)
            
        else:
            print("Undefined argument.")
            break

    capture.release()

    if output_frames:
        total_time = time.time() - start_time
        print(f"✅ Processed {len(output_frames)} frames in {total_time:.2f}s")
        print(f"📹 Exporting at {len(output_frames)/total_time:.1f} fps...")
        export_video_global(output_frames, "../build/" + FILENAME, fps_cv)
        print("🎬 Video exported: " + FILENAME)
    else:
        print("❌ No frames processed!")

    print(f"🎉 Done! Open {FILENAME} to see your masterpiece!")

# ---------------------- Parsing args below here ----------------------

if args.rtm == "enable":
    realtimeManipulation()
elif args.render == "enable":
    renderVideo()
else :
    print("Undefined argument!")