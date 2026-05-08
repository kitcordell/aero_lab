from dataclasses import dataclass
import numpy as np

@dataclass
class Wing:
    span: float          # b
    root_chord: float    # c_r
    taper_ratio: float   # c_tip / c_root
    alpha_root: float    # geometric AoA at root, radians
    twist: float         # linear washout at tip, radians
    alpha_L0: float      # zero-lift AoA from thin airfoil theory, radians
    a0: float = 2 * np.pi  # section lift curve slope


def local_chord(y,wing):
    

    
