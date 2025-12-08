import cv2 as cv
import argparse
import time
import subprocess
import sys
import os
from datetime import datetime

from effects.tracker import Tracker
from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.vhs import VHS

from effects.effect_manager import EffectManager

from processors.render_processor import RenderProcessor

def listEffects(args):
    effectManager = EffectManager()

    for effect, functions in effectManager.effects_functions.items():
        print(f"{effect}")
    
        