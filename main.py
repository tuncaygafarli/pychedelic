import cv2 as cv
import argparse
import time
import subprocess
import sys
from datetime import datetime

from effects.tracker import Tracker
from effects.color_chaos_manipulator import ColorChaosManipulator
from processors.render_processor import RenderProcessor

from scripts.renderVideo import renderVideo
from scripts.realtimeManipulation import realtimeManipulation
from scripts.webcamManipulation import webcamManipulation

# ---------------------- Argument parser implementation below here ----------------------


parser = argparse.ArgumentParser(description="OpenCV Visual Artifacts - Transform your videos with psychedelic effects and mathematical transformations! 🌈✨",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
🌟 Examples:
  python main.py -rtm enable          Live webcam psychedelic effects
  python main.py -render enable       Process video files with visual artifacts
  
    Features:
  • Real-time complexity analysis
  • Dynamic effect triggering  
  • Psychedelic color transformations
  • Mathematical frame distortions
    """)

parser.add_argument(
    "-rtm", "--realtime", 
    type=str,
    choices=['enable'],
    help="Enable realtime manipulation mode (webcam required)"
)

parser.add_argument(
    "-render", "--render", 
    type=str,
    choices=['enable'], 
    help="Render video files with visual artifacts"
)

parser.add_argument(
    "-webcam", "--webcam", 
    type=str,
    choices=['enable'], 
    help="Show webcam with visual artifacts"
)

parser.add_argument(
    "-effects", "--effects", 
    nargs='+',
    choices=['Tracker','ColorChaos', 'VHS',"NightVision","FacialArtifacts"], 
    help="Choose effects to be applied"
)

args = parser.parse_args()

if hasattr(args, "realtime") and args.realtime == "enable":
    realtimeManipulation(args)
elif hasattr(args, "render") and args.render == "enable":
    renderVideo(args)
elif hasattr(args, "webcam") and args.webcam == "enable":
    webcamManipulation(args)
else :
    print("Undefined argument!")