"""GERSTNER"""

import copy

# from sh_info.shInfoAbstract import ShInfoAbstract
import P as P
import random
import numpy as np
from scipy import stats

class Waves_info:
    """
    The class instance itself is the container for all the info,
    for the parent o0 they are
    """

    def __init__(_s):

        _s.id = 'waves'  # Gerstner
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        _s.zorder = 95

        _s.o1_init_frames = [2]
        _s.o1_left_offsets = np.linspace(-0, 0, num=P.NUM_O1_WAVES)  # highest one most to left
        _s.o1_left_starts = np.linspace(2 * np.pi, 0.01, num=P.NUM_O1_WAVES)  # highest vs lowest one period diff
        _s.o1_down_offsets = np.linspace(0, 200, num=P.NUM_O1_WAVES)
        _s.o1_steepnessess = np.linspace(0.5, 0.51, num=P.NUM_O1_WAVES)  # OBS ONLY BETWEEN 0 and 1

        _s.o1_gi = _s.gen_o1_gi()
        _s.o2_gi = _s.gen_o2_gi()

    def gen_o1_gi(_s):
        """
        This has to be provided because the fs are generated w.r.t. sh.
        This is like the constructor input for F class
        """

        o1_gi = {
            'init_frames': None,
            'frames_tot': P.FRAMES_STOP - 25,
            'frame_ss': None,
            'ld': [1200, 400],  # left-down
            'left_offsets': None,
            'zorder': 5
        }

        '''OFFSETS FOR O2
        THIS GIVES LD FOR O2!!!
        '''
        o1_gi['left_offsets'] = np.linspace(-400, -0, num=P.NUM_WAVE_O2_PER_O1)  # USED PER 02

        return o1_gi

    def gen_o2_gi(_s):
        """
        UPDATE: THESE ARE NO LONGER CHILDREN OF F,
        THEIR INIT FRAMES CAN BE SET BY F THOUGH.
        """
        o2_gi = {
            'alpha_y_range': [1, 1],
            'init_frames': None,  # ONLY FOR THIS TYPE
            'frames_tot': 1200,  # MUST BE LOWER THAN SP.FRAMES_TOT. MAYBE NOT. INVOLVED IN BUG  OBS
            'v_loc': 50, 'v_scale': 4,  # 50 THIS IS HOW HIGH THEY GO (not how far down)
            'ld': [None, None],  # left-down
            'up_down': 'up',
            'zorder': 1000
        }

        return o2_gi
