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
        # _s.extent = "static"
        _s.frame_ss = [0, P.FRAMES_STOP - 50]
        _s.zorder = 95

        # _s.child_names = ['O1']
        _s.o1_init_frames = [2]
        _s.o1_left_offsets = np.linspace(-0, 0, num=P.NUM_O1_WAVES)  # highest one most to left
        _s.o1_left_starts = np.linspace(2 * np.pi, 0.01, num=P.NUM_O1_WAVES)  # highest vs lowest one period diff
        # _s.o1_left_starts = np.linspace(0, 2 * np.pi, num=P.NUM_O1_WAVES)
        _s.o1_down_offsets = np.linspace(0, 200, num=P.NUM_O1_WAVES)
        _s.o1_steepnessess = np.linspace(0.5, 0.51, num=P.NUM_O1_WAVES)  # OBS ONLY BETWEEN 0 and 1

        _s.o1_gi = _s.gen_o1_gi()  # OBS: sp_gi generated in f class. There is no info class for f.
        _s.o2_gi = _s.gen_o2_gi()
        # _s.downs = np.linspace(start=400, stop=600, num=P.NUM_WAVE_O2_PER_O1)

    def gen_o1_gi(_s):
        """
        This has to be provided because the fs are generated w.r.t. sh.
        This is like the constructor input for F class
        """
        # FRAMES_TOT = P.FRAMES_TOT  # MUST BE HIGHTER THAN SP.FRAMES_TOT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

        o1_gi = {
            'init_frames': None,  # New: changed
            'frames_tot': P.FRAMES_STOP - 25,  # only used for init
            'frame_ss': None,  # simpler with this
            'ld': [1200, 400],  # left-down
            'left_offsets': None,  # BELOW [-500, 500] num doesnt matter cuz pos = random.randint(0, 20)
            # 'steepnessess': None,  # BELOW
            # 'steepness': None,
            # 'theta_loc': None,  # set at init from offsets
            # 'theta_offsets': None,  # list(np.linspace(0.3, -0.3, num=NUM_RANDS)), #[0.5, -0.5],
            # 'init_frame_x_offsets': list(np.linspace(20, 0, num=NUM_RANDS - 25, dtype=int)) + list(np.linspace(0, 20, num=NUM_RANDS - 15, dtype=int)),
            'zorder': 5
        }

        '''OFFSETS FOR O2
        THIS GIVES LD FOR O2!!!
        '''
        o1_gi['left_offsets'] = np.linspace(-400, -0, num=P.NUM_WAVE_O2_PER_O1)  # USED PER 02
        # o1_gi['down_offsets'] = np.linspace(0, 200, num=P.NUM_O1_WAVES)  # USED PER O1. SHOULD ACTUALLY BE IN O0 BUT BUT
        # o1_gi['steepnessess'] = np.linspace(50, 10, num=P.NUM_O1_WAVES)  # USED PER O1

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
            # 'theta_scale': 0.01,  # 0.1 unit circle straight up
            # 'sp_len_start_loc': 1, 'sp_len_start_scale': 1,
            # 'sp_len_stop_loc': 2, 'sp_len_stop_scale': 1,  # this only cov  ers uneven terrain
            # 'special': False,
            # 'ld_init': [None, None],  # set by f
            'ld': [None, None],  # left-down
            # 'ld_offset_loc': [0, 0],  # NEW: Assigned when inited
            # 'ld_offset_scale': [50, 3],  # [125, 5]
            'up_down': 'up',
            # 'out_screen': False,
            'zorder': 1000
        }

        return o2_gi
