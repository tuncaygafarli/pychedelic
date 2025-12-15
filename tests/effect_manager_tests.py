import cv2 as cv
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.module_manager import ModuleManager

ModuleManager = ModuleManager()

print(ModuleManager.get_effect("vhs").name)