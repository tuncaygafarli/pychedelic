import cv2 as cv
import numpy as np
import time
from datetime import datetime
import sys
import os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import classes
from modules.tracker import Tracker
from modules.color_chaos import ColorChaosManipulator
from processors.render_processor import RenderProcessor
from modules.module_manager import ModuleManager

ASSETS_PATH = '../assets/'
AUDIO_FILE = 'assets/worldwide.wav'
FILENAME = "video_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".mp4"
VIDEO_NAME_IO = input(str("Enter video name to process : "))

capture = cv.VideoCapture(ASSETS_PATH + VIDEO_NAME_IO + ".mp4")

tracker = Tracker()
cc_manipulator = ColorChaosManipulator()

renderProcessor = RenderProcessor()

ModuleManager = ModuleManager()

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
        tracker.add_frame(frame)
        processed_tracker_frame = tracker.process_current_frame(frame)
        output_frames.append(processed_tracker_frame)
        
    elif apply_calibration == "N" or apply_calibration == "n":
        cc_manipulator.add_frame(frame)
        output_frames.append(frame)
        
    else:
        print("Undefined argument.")
        break
    active_effect = ModuleManager.get_active_effect()

    complexity = active_effect.calculate_complexity(frame)
    active_effect.add_frame(frame)

    processed_frame = ModuleManager.process_frame(frame, complexity)

capture.release()

if output_frames:
    total_time = time.time() - start_time
    print(f"✅ Processed {len(output_frames)} frames in {total_time:.2f}s")
    print(f"📹 Exporting at {len(output_frames)/total_time:.1f} fps...")
    renderProcessor.renderFrames(output_frames, "../build/" + FILENAME, fps_cv)
    print("🎬 Video exported: " + FILENAME)
else:
    print("❌ No frames processed!")

print(f"🎉 Done! Open {FILENAME} to see your masterpiece!")