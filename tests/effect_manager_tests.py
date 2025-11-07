import cv2 as cv
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from effects.effect_manager import EffectManager

effectManager = EffectManager()

print(effectManager.get_effect("vhs").name)