import cv2 as cv
import argparse
import time
import subprocess
import sys
from datetime import datetime

# ------------------- Importing effects from here -------------------
from effects.calibrator import Calibrator
from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.vhs import VHS

# ------------------- Importing functions from here -------------------
from functions.render_processor import renderProcessor

def renderVideo(args):
    ASSETS_PATH = 'assets/'
    FILENAME = "video_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".mp4"
    VIDEO_NAME_IO = input(str("Enter video name to process : "))

    capture = cv.VideoCapture(ASSETS_PATH + VIDEO_NAME_IO + ".mp4")

    calibrator = Calibrator()
    cc_manipulator = ColorChaosManipulator()
    vhs = VHS()

    output_frames = []

    print("⚡ Processing frames at MAXIMUM SPEED (no display)...")

    frame_count = 0
    start_time = time.time()

    while True:
        isTrue, frame = capture.read()  
        fps_cv = capture.get(cv.CAP_PROP_FPS)
        max_frames = int (fps_cv * 30)

        if not isTrue or frame_count >= max_frames: 
            break
        
        frame_count += 1
        
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            print(f"📊 Processed {frame_count} frames ({fps:.1f} fps)")
        
        if hasattr(args, "effects"):
            if "Calibrator" in args.effects:
                complexity = calibrator.calculate_complexity(frame)

                calibrator.add_frame(frame)
                processed_calibrator_frame = calibrator.process_current_frame(frame)
                output_frames.append(processed_calibrator_frame)
            
            elif "ColorChaosManipulator" in args.effects:
                complexity = cc_manipulator.calculate_complexity(frame)

                cc_manipulator.add_frame(frame)
                processed_cc_manipulator_frame = cc_manipulator.process_current_frame(frame, complexity)
                output_frames.append(processed_cc_manipulator_frame)

            elif "VHS" in args.effects:
                complexity = vhs.calculate_complexity(frame)

                vhs.add_frame(frame)
                processed_vhs_frame = vhs.process_current_frame(frame, complexity)
                output_frames.append(processed_vhs_frame)
        else:
            print("Undefined argument.")
            break

    capture.release()

    if output_frames:
        total_time = time.time() - start_time
        print(f"✅ Processed {len(output_frames)} frames in {total_time:.2f}s")
        print(f"📹 Exporting at {len(output_frames)/total_time:.1f} fps...")
        renderProcessor(output_frames, "build/" + FILENAME, fps_cv)
        print("🎬 Video exported: " + FILENAME)
    else:
        print("❌ No frames processed!")

    print(f"🎉 Done! Open {FILENAME} to see your masterpiece!")
