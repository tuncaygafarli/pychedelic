import cv2 as cv
import numpy as np
import inspect
import sys
import os

# ------------------- Import effects from here -------------------

from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.tracker import Tracker
from effects.vhs import VHS
from effects.night_vision import NightVision
from effects.facial_artifacts import FacialArtifacts
from effects.chromatic_aberration import ChromaticAberration
from effects.none_effect import NoneEffect
from effects.grunge import Grunge

class EffectManager:

    def __init__(self):
        self.effects = {
            "Tracker" : Tracker(),
            "ColorChaos" : ColorChaosManipulator(),
            "VHS" : VHS(),
            "NightVision" : NightVision(),
            "FacialArtifacts" : FacialArtifacts(),
            "ChromaticAberration" : ChromaticAberration(),
            "Grunge" : Grunge(),
            "None" : NoneEffect()
        }

        self.effects_functions = {}
        self.active_effect = None
        self.active_effect_function = None
        self.effect_history = []
        self.effect_functions_history = []
        self.toggled = True

        for effect_name, effect_instance in self.effects.items():
            methods = inspect.getmembers(effect_instance, predicate=inspect.ismethod)

            method_names = [
                method[0] for method in methods
                if not method[0].startswith('_') and not method[0].endswith('__') and not method[0].startswith("add") and not method[0].startswith("process") and not method[0].startswith("calculate") and not method[0].startswith("apply")
            ]

            self.effects_functions[effect_name] = method_names


    def set_effect(self, effect_name):
        if effect_name in self.effects:
            self.active_effect = self.effects[effect_name]
            self.effect_history.append(self.effects[effect_name])

            return True
        else:
            print(f"Couldn't find effect matching: {effect_name}!")
            print(f"Available effects are: {list(self.effects.keys())}")
            return False

    def process_frame(self, frame, complexity, args):
        if not self.active_effect or self.toggled == False:
            return frame

        result = frame.copy()

        if args.functions:
            for func_name in args.functions:
                try:
                    if func_name not in self.effect_functions_history:
                        self.effect_functions_history.append(func_name)
                    method = getattr(self.active_effect, func_name)
                    result = method(result)
                except AttributeError:
                    print(f"{func_name}() not found in {self.active_effect.__class__.__name__}")
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    line_number = exc_traceback.tb_lineno
                    filename = exc_traceback.tb_frame.f_code.co_filename

                    print(f"Error => {exc_type} : {e} in file {os.path.basename(filename)} : line number {line_number}")
        else:
            if hasattr(self.active_effect, 'process_current_frame'):
                result = self.active_effect.process_current_frame(result, complexity)

        return result

    def get_active_effect(self):
        return self.active_effect

    def get_effect(self, effect_name):
        effect = self.effects[effect_name]
        return effect
