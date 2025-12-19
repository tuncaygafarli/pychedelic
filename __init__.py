"""
Pychedelic - Image and Video Effects Processing Library
"""

__version__ = "1.0.0"
__author__ = "Tuncay Gafarli"
__license__ = "GNU GENERAL PUBLIC LICENSE, Version 3"

# Core exports
from modules.module_manager import ModuleManager

# Convenience imports
from . import modules
from . import processors
from . import utils

__all__ = [
    'ModuleManager',
    'modules',
    'processors',
    'utils'
]