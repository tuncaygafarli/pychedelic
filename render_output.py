import cv2 as cv
import numpy as np
import time
from datetime import datetime

# Import classes
from effects.calibrator import Calibrator
from effects.color_chaos_manipulator import ColorChaosManipulator
from functions.export_video import export_video_global

VIDEO_PATH = 'assets/video_1_trimmed.mp4'
AUDIO_FILE = 'assets/worldwide.wav'
FILENAME = "video_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".mp4"

capture = cv.VideoCapture(VIDEO_PATH)
calibrator = Calibrator()
cc_manipulator = ColorChaosManipulator()

apply_calibration = str(input("Apply calibration? Y or N : "))

#play_audio(AUDIO_FILE)
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
    
    # Progress update every 30 frames
    if frame_count % 30 == 0:
        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0
        print(f"📊 Processed {frame_count} frames ({fps:.1f} fps)")
    
    complexity = calibrator.calculate_complexity(frame)
    
    if apply_calibration == "Y" or apply_calibration == "y":
        calibrator.add_frame(frame)
        processed_frame = calibrator.process_current_frame(frame)
        output_frames.append(processed_frame)
        
    elif apply_calibration == "N" or apply_calibration == "n":
        calibrator.add_frame(frame)
        output_frames.append(frame)
        
    else:
        print("Undefined argument.")
        break

capture.release()

if output_frames:
    total_time = time.time() - start_time
    print(f"✅ Processed {len(output_frames)} frames in {total_time:.2f}s")
    print(f"📹 Exporting at {len(output_frames)/total_time:.1f} fps...")
    export_video_global(output_frames, "build/" + FILENAME, fps_cv)
    print("🎬 Video exported: " + FILENAME)
else:
    print("❌ No frames processed!")

print(f"🎉 Done! Open {FILENAME} to see your masterpiece!")