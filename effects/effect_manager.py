import cv2 as cv
import numpy as np

# ------------------- Import effects from here -------------------

from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.tracker import Tracker
from effects.vhs import VHS
from effects.night_vision import NightVision
from effects.facial_artifacts import FacialArtifacts

class EffectManager:

    def __init__(self):
        self.effects = {
            "tracker" : Tracker(),
            "color_chaos" : ColorChaosManipulator(),
            "vhs" : VHS(),
            "night_vision" : NightVision(),
            "facial_artifacts" : FacialArtifacts()
        }

        self.active_effect = None
        self.effect_history = []

    def set_effect(self, effect_name):
        if effect_name in self.effects:
            self.active_effect = self.effects[effect_name]
            self.effect_history.append(self.effects[effect_name])

            return True
        else:
            print("Couldn't find effect!")
            return False
    
    def get_active_effect(self):
        return self.active_effect
    
    def get_effect(self, effect_name):
        effect = self.effects[effect_name]
        return effect