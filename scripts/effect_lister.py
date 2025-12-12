import cv2 as cv
import argparse
import time
import subprocess
import sys
import os
from datetime import datetime

from effects.effect_manager import EffectManager

def listEffects(args):
    effectManager = EffectManager()

    for effect, functions in effectManager.effects_functions.items():
        print(f"{effect}")
    
        