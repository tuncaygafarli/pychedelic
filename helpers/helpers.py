import math
import numpy as np

class Helpers:

    """
    Defining some mathematical foundations from here 
    to easily calculate complexities
    """

    def __init__(self):
        self.base_weber = {
            'luminance': 0.08,
            'contrast': 0.10,
            'color': 0.15,
            'texture': 0.20,
            'edges': 0.12
        }

    def sigmoid_normalize(self, x, center=8.0, steepness=1.0):
        """
        Maps any number to 0-1 range
        center: where the output is 0.5
        steepness: how quickly it transitions
        """

        return 1 / (1 + np.exp(-steepness * (x - center)))
    
    def modulate_weber(self, base, complexity):
        modulation = 1 + 3 * complexity
        return base * modulation
    
    def perceptual_sigmoid(self, x, center, base, complexity):
        """
        Weber-Fechner: ∆I/I = constant
        Adapts sigmoid for perceptual scaling
        """

        log_x = np.log1p(x)
        log_center = np.log1p(center)

        weber_fraction = self.modulate_weber(self.base_weber[base], complexity)

        base_steepness = 8.0
        steepness = base_steepness / (1 + 10 * weber_fraction)
        
        return 1 / (1 + np.exp(-steepness * (log_x - log_center)))