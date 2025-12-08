"""
Pychedelic - Image and Video Effects Processing Library
"""

__version__ = "1.0.0"
__author__ = "Tuncay Gafarli"
__license__ = "MIT"

# Core exports
from effects.effect_manager import EffectManager

# Convenience imports
from . import effects
from . import processors
from . import utils

__all__ = [
    'EffectManager',
    'effects',
    'processors',
    'utils'
]