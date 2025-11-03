import cv2 as cv
import numpy as np
import os

def export_video_global(frames, output_path, fps):
    """🚀 Global function to export ANY list of frames as video"""
    if not frames:
        print("❌ No frames to export!")
        return False

    height, width = frames[0].shape[:2]
    
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"📹 Exporting {len(frames)} frames to {output_path}...")
    
    for i, frame in enumerate(frames):
        out.write(frame)
        if i % 30 == 0: 
            print(f"📦 Frame {i}/{len(frames)}")
    
    out.release()
    print(f"✅ Video exported: {output_path}")
    return True