def save_60fps_video(manipulator, output_path="output_60fps.mp4"):
    if not manipulator.manipulated_frames:
        print("No processed frames to save!")
        return
    
    height, width = manipulator.manipulated_frames[0].shape[:2]
    
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(output_path, fourcc, 60.0, (width, height))
    
    for frame in manipulator.processed_frames:
        out.write(frame)
    out.release()
    print(f"✅ 60fps video saved: {output_path}")