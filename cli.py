import cv2 as cv
import argparse
import time
import os
import sys
from datetime import datetime

from modules.tracker import Tracker
from modules.color_chaos import ColorChaos
from processors.render_processor import RenderProcessor

from scripts.video_renderer import videoRenderer
from scripts.realtime_filter import realtimeFilter
from scripts.webcam_filter import webcamFilter
from scripts.module_lister import listModules
from scripts.effect_lister import listEffects
from scripts.configure import Configure

configure = Configure()

# ---------------------- Argument parser implementation below here ----------------------

def main():
    parser = argparse.ArgumentParser(description="OpenCV Visual Artifacts - Transform your videos with psychedelic effects and mathematical transformations!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        python main.py -mode webcam --effects Tracker          Live webcam psychedelic effects
        python main.py -mode rtm --effects ColorChaos       Process video files with visual artifacts
    
        Features:
    • Real-time complexity analysis
    • Dynamic effect triggering  
    • Psychedelic color transformations
    • Mathematical frame distortions
        """)

    parser.add_argument(
        "-mode", "--mode", 
        type=str,
        choices=['render','live','webcam'],
        help="Sets the mode to specified argument"
    )

    parser.add_argument(
        "-modules", "--modules", 
        nargs='+',
        choices=['Tracker','ColorChaos', 'VHS',"NightVision",'FacialArtifacts','FaceBlur','EyeBlur','ChromaticAberration','Grunge','None'], 
        help="Chooses modules to be applied"
    )

    parser.add_argument(
        "-effects", "--effects",
        nargs='*', 
        help="Specific effects to apply (e.g., face_blur psychedelic_eye_shift)"
    )

    parser.add_argument(
            '--configure', 
            nargs=2, 
            metavar=('KEY', 'VALUE'),
            help='Configure a specific setting (e.g., --configure assets_video assets/video)'
    )

    parser.add_argument(
        "--init", 
        action = "store_true", 
        help="Initialize essential config files."
    )

    parser.add_argument(
        "-list", "--list", 
        type=str,
        choices=["modules","effects"],
        help="Lists the given argument"
    )

    parser.add_argument(
        "--debug", 
        action = "store_true", 
        help="Enable debug mode for RTM"
    )

    args = parser.parse_args()

    if hasattr(args, "mode") and args.mode == "live":
        realtimeFilter(args)
    elif hasattr(args, "mode") and args.mode == "render":
        videoRenderer(args)
    elif hasattr(args, "mode") and args.mode == "webcam":
        webcamFilter(args)
    elif hasattr(args, "list") and args.list == "modules":
        listModules(args)
    elif hasattr(args, "list") and args.list == "effects":
        listEffects(args)
    elif args.init:
        configure.init()

    elif args.configure:
        key, value = args.configure
        config = configure.load_config()

        if key == "assets_video":
            if 'assets' not in config:
                config['assets'] = {}
            
            config['assets']['assets_video'] = value
            
            configure.save_config(config)
            print(f"✅ Configuration updated!")

    else :
        print("Undefined argument!")

if __name__ == "__main__":
    main()