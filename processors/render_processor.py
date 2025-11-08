import cv2 as cv
import numpy as np


class RenderProcessor:

    def __init__(self):
        self.frames = []

    def renderFrames(self, frames, output_path, fps):
        if not frames:
            print("❌ No frames to export!")
            return False

        height, width = frames[0].shape[:2]
        
        fourcc = cv.VideoWriter_fourcc(*'avc1')
        out = cv.VideoWriter(output_path, fourcc, fps, (width, height))

        out.set(cv.VIDEOWRITER_PROP_QUALITY, 80)
        
        print(f"📹 Exporting {len(frames)} frames to {output_path}...")
        
        for i, frame in enumerate(frames):
            out.write(frame)
            if i % 30 == 0: 
                print(f"📦 Frame {i}/{len(frames)}")
        
        out.release()
        return True