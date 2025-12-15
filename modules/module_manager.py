import cv2 as cv
import numpy as np
import inspect
import sys
import os
from colorama import Fore, Back, Style, init

# ------------------- Import modules from here -------------------

from modules.color_chaos import ColorChaos
from modules.tracker import Tracker
from modules.vhs import VHS
from modules.night_vision import NightVision
from modules.facial_artifacts import FacialArtifacts
from modules.chromatic_aberration import ChromaticAberration
from modules.none import NoneModule
from modules.grunge import Grunge

class ModuleManager:

    def __init__(self):
        self.modules = {
            "Tracker" : Tracker(),
            "ColorChaos" : ColorChaos(),
            "VHS" : VHS(),
            "NightVision" : NightVision(),
            "FacialArtifacts" : FacialArtifacts(),
            "ChromaticAberration" : ChromaticAberration(),
            "Grunge" : Grunge(),
            "None" : NoneModule()
        }

        self.modules_functions = {}
        self.active_module = None
        self.active_module_effect = None
        self.module_history = []
        self.module_effects_history = []
        self.toggled = True

        for module_name, module_instance in self.modules.items():
            methods = inspect.getmembers(module_instance, predicate=inspect.ismethod)

            method_names = [
                method[0] for method in methods
                if not method[0].startswith('_') and not method[0].endswith('__') and not method[0].startswith("add") and not method[0].startswith("process") and not method[0].startswith("calculate") and not method[0].startswith("apply")
            ]

            self.modules_functions[module_name] = method_names


    def set_module(self, module_name):
        if module_name in self.modules:
            self.active_module = self.modules[module_name]
            self.module_history.append(self.modules[module_name])

            return True
        else:
            print(f"Couldn't find module matching: {module_name}!")
            print(f"Available modules are: {list(self.modules.keys())}")
            return False

    def process_frame(self, frame, complexity, args):
        if not self.active_module or self.toggled == False:
            return frame

        result = frame.copy()

        if args.effects:
            for effect_name in args.effects:
                try:
                    if effect_name not in self.module_effects_history:
                        self.module_effects_history.append(effect_name)
                    method = getattr(self.active_module, effect_name)
                    result = method(result)
                except AttributeError:
                    print(f"{effect_name}() not found in {self.active_module.__class__.__name__}")
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    line_number = exc_traceback.tb_lineno
                    filename = exc_traceback.tb_frame.f_code.co_filename

                    print(f"Error => {exc_type} : {e} in file {os.path.basename(filename)} : line number {line_number}")
        else:
            if hasattr(self.active_module, 'process_current_frame'):
                result = self.active_module.process_current_frame(result, complexity)

        return result

    def get_active_module(self):
        return self.active_module

    def get_module(self, module_name):
        module = self.modules[module_name]
        return module
