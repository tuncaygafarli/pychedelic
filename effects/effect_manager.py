import cv2 as cv
import numpy as np

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
            "tracker" : Tracker(),
            "color_chaos" : ColorChaosManipulator(),
            "vhs" : VHS(),
            "night_vision" : NightVision(),
            "facial_artifacts" : FacialArtifacts(),
            "chromatic_aberration" : ChromaticAberration(),
            "grunge" : Grunge(),
            "none" : NoneEffect()
        }

        self.effects_functions = {
            "Tracker" : [],
            "ColorChaos" : [
                "channel_swap","color_blast","hue_shift","sine_distortion","rgb_split","channel_shifting","kaleidoscope"
                ],
            "VHS" : [
                "vhs_scan_lines","vhs_color_bleeding","vhs_noise","vhs_head_clog","vhs_tape_damage","vhs_tape_glitch","vhs_barrel_distortion"
                ],
            "FacialArtifacts" : [
                "mark_face","blur_face","blur_eyes","psychedelic_face_shift","psychedelic_eye_shift","face_filter"
                ],
            "NightVision" : [
                "night_vision_overlay","night_vision_scan_lines","night_vision_barrel_distortion"
                ],
            "Grunge" : [
                "grunge_bleach_bypass","emo_bloom_effect","washed_emo_layers","burnify"
                ],
            "ChromaticAberration" : []
        }

        self.active_functions = [
            "channel_swap","color_blast","hue_shift","sine_distortion","rgb_split","channel_shifting","kaleidoscope",

            "blur_face","blur_eyes","psychedelic_face_shift","psychedelic_eye_shift","mark_face","face_filter",

            "vhs_scan_lines","vhs_color_bleeding","vhs_noise","vhs_head_clog","vhs_tape_damage","vhs_tape_glitch","vhs_barrel_distortion",

            "night_vision_overlay","night_vision_scan_lines","night_vision_barrel_distortion",

            "grunge_bleach_bypass","emo_bloom_effect","washed_emo_layers","burnify"
        ]

        self.active_effect = None
        self.active_effect_function = None
        self.effect_history = []
        self.effect_functions_history = []
        self.toggled = True

    def set_effect(self, effect_name):
        if effect_name in self.effects:
            self.active_effect = self.effects[effect_name]
            self.effect_history.append(self.effects[effect_name])

            return True
        else:
            print("Couldn't find effect!")
            return False
        
    def process_frame(self, frame, complexity, args):
        if not self.active_effect:
            return frame
            
        result = frame.copy()
        
        if args.functions:
            for func_name in args.functions:
                try:
                    if func_name not in self.effect_functions_history:
                        self.effect_functions_history.append(func_name)
                    method = getattr(self.active_effect, func_name)
                    result = method(result)
                    #print(f"Called {func_name}()")
                except AttributeError:
                    print(f"{func_name}() not found in {self.active_effect.__class__.__name__}")
                except Exception as e:
                    print(f"Error in {func_name}: {e}")
        else:
            if hasattr(self.active_effect, 'process_current_frame'):
                result = self.active_effect.process_current_frame(result, complexity)
        
        return result
    
    def get_active_effect(self):
        return self.active_effect
    
    def get_effect(self, effect_name):
        effect = self.effects[effect_name]
        return effect