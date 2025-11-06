import cv2 as cv
import argparse
import time
import subprocess
import os
import sys
from datetime import datetime

# ------------------- Importing effects from here -------------------
from effects.tracker import Tracker
from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.vhs import VHS

from effects.effect_manager import EffectManager

# ------------------- Importing functions from here -------------------
from processors.render_processor import RenderProcessor

def renderVideo(args):
    ASSETS_PATH = 'assets/'
    FILENAME = "video_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".mp4"

    entries = os.listdir(ASSETS_PATH)
    files = [entry for entry in entries if os.path.isfile(os.path.join(ASSETS_PATH, entry))]
    print("Files to be processed in assets folder : " + str(files))

    VIDEO_NAME_IO = input(str("Enter video name to process : "))

    capture = cv.VideoCapture(ASSETS_PATH + VIDEO_NAME_IO + ".mp4")

    # ------------------- Initialize effects from here -------------------
    tracker = Tracker()
    cc_manipulator = ColorChaosManipulator()
    vhs = VHS()

    effectManager = EffectManager()

    # ------------------- Initialize processors from here -------------------
    renderProcessor = RenderProcessor()

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
            if "Tracker" in args.effects:
                effectManager.set_effect("tracker")
            
            elif "ColorChaos" in args.effects:
                effectManager.set_effect("color_chaos")

            elif "VHS" in args.effects:
                effectManager.set_effect("vhs")
        else:
            print("Undefined argument.")
            break
        
        active_effect = effectManager.get_active_effect()

        complexity = active_effect.calculate_complexity(frame)
        active_effect.add_frame(frame)

        processed_frame = active_effect.process_current_frame(frame, complexity)
        active_effect.processed_frames.append(processed_frame)

    capture.release()

    if active_effect.processed_frames:
        total_time = time.time() - start_time
        print(f"✅ Processed {len(active_effect.processed_frames)} frames in {total_time:.2f}s")
        print(f"📹 Exporting at {len(active_effect.processed_frames)/total_time:.1f} fps...")
        renderProcessor.renderFrames(active_effect.processed_frames, "build/" + FILENAME, fps_cv)
        print("🎬 Video exported: " + FILENAME)
    else:
        print("❌ No frames processed!")

    print(f"🎉 Done! Open {FILENAME} to see your masterpiece!")
