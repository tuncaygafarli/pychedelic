import cv2 as cv
import argparse
import time
import subprocess
import sys
from datetime import datetime

from effects.tracker import Tracker
from effects.color_chaos import ColorChaos
from processors.render_processor import RenderProcessor

from scripts.video_renderer import videoRenderer
from scripts.realtime_filter import realtimeFilter
from scripts.webcam_filter import webcamFilter
from scripts.effect_lister import listEffects
from scripts.function_lister import listFunctions

# ---------------------- Argument parser implementation below here ----------------------


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
    "-effects", "--effects", 
    nargs='+',
    choices=['Tracker','ColorChaos', 'VHS',"NightVision",'FacialArtifacts','FaceBlur','EyeBlur','ChromaticAberration','Grunge','None'], 
    help="Chooses effects to be applied"
)

parser.add_argument(
    "-functions", "--functions",
    nargs='*', 
    help="Specific functions to call (e.g., face_blur psychedelic_eye_shift)"
)

parser.add_argument(
    "-list", "--list", 
    type=str,
    choices=["effects","functions"],
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
elif hasattr(args, "list") and args.list == "effects":
    listEffects(args)
elif hasattr(args, "list") and args.list == "functions":
    listFunctions(args)
else :
    print("Undefined argument!")