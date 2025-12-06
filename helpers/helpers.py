import math
import numpy as np

class Helpers:
    def __init__(self):
        pass

    def sigmoid_normalize(self, x, center=8.0, steepness=1.0):
        """
        Maps any number to 0-1 range
        center: where the output is 0.5
        steepness: how quickly it transitions
        """

        return 1 / (1 + np.exp(-steepness * (x - center)))