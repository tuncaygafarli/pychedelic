import cv2 as cv
import argparse
import time
import subprocess
import sys
import os
from datetime import datetime

from modules.module_manager import ModuleManager

def listModules(args):
    ModuleManager = ModuleManager()

    for effect, functions in ModuleManager.effects_functions.items():
        print(f"{effect}")