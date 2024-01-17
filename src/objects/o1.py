import random

import numpy as np
from copy import deepcopy

import P as P
from src.gen_trig_fun import *
from src.objects.abstract import AbstractObject, AbstractSSS

class O1C(AbstractObject, AbstractSSS):

    def __init__(_s, o1_id, pic, o0):
        AbstractObject.__init__(_s)
        _s.id = o1_id
        _s.o0 = o0  # parent
        _s.pic = pic  # the png
        _s.gi = deepcopy(o0.gi.o1_gi)  # OBS!

        AbstractSSS.__init__(_s, o0, o1_id)

        _s.O2 = {}
        _s.alphas = None

        '''OBSSSS!!!!'''
        if _s.o0.id in ['projectiles', 'clouds']:
            # _s.gi['init_frames'] = [deepcopy(_s.gi['init_frames'][int(_s.id[-1])])]
            # init_frames_all = deepcopy(_s.gi['init_frames'])

            # OBS DOWN AND LEFT OFFSETS DONE IN FINISH_INFO CUZ THEY ARE DYNAMIC.
            _s.XY = None  # dyn_gen
            _s.rot = None   # dyn_gen
            _s.cmap = None  # dyn_gen

            init_frames = []
            for i in range(P.NUM_INIT_FRAMES_CLOUD):  # OBS OBS
                if len(_s.o0.gi.o1_init_frames) < 1:
                    pass
                else:
                    random.shuffle(_s.o0.gi.o1_init_frames)
                    init_frames.append(_s.o0.gi.o1_init_frames.pop())  # OBS no copy cuz they're used by all
                    init_frames.sort()
                    _s.gi['init_frames'] = init_frames

        elif _s.o0.id == 'waves':
            # _s.gi['init_frames'] = [deepcopy(_s.gi['init_frames'][int(_s.id[-1])])]
            _s.gi['init_frames'] = [_s.o0.gi.o1_init_frames[0]]  # same for all
            id_int = int(_s.id)  # OBS

            # DOWN OFFSET:
            _s.gi['ld'][0] += _s.o0.gi.o1_left_offsets[id_int]
            _s.gi['ld'][1] += _s.o0.gi.o1_down_offsets[id_int]
            _s.gi['steepness'] = _s.o0.gi.o1_steepnessess[id_int] #+ np.random.randint(low=0, high=50, size=1)[0]
            _s.gi['o1_left_start'] = _s.o0.gi.o1_left_starts[id_int] #+ np.random.randint(low=0, high=50, size=1)[0]

        # elif _s.o0.id == 'clouds':
        #     _s.gi['init_frames'] = [_s.o0.gi.o1_init_frames[0]]


        adf = 5

    def gen_scale_vector(_s):

        scale_ss = []
        return scale_ss

    def dyn_gen(_s):

        """
        Basically everything moved from init to here.
        This can only be called when init frames are synced between
        """

        _s.finish_info()

    def finish_info(_s):
        """Separated from _init_ bcs extra things may need to be finished in viewer."""

        _s.alphas = np.ones(shape=(_s.gi['frames_tot']))

        if _s.o0.id == 'projectiles':

            id_int = int(_s.id[-1])  # OBS. Used by o1_down_offsets
            # _s.gi['ld'][1] += _s.o0.gi.o1_down_offsets[id_int]  # NOT GOOD. dont change parameters

            '''30_ xys and thetas based on direction'''
            XY = np.zeros(shape=(_s.gi['frames_tot'], 2))
            # XY[:, 1] = _s.gi['ld'][1]  # y never changes

            rand_0 = np.random.choice([-1, 1])
            rand_1 = np.random.randint(low=1, high=6, size=1)[0]

            X = rand_0 * np.sin(np.linspace(0, rand_1 * np.pi, num=len(XY)))
            rot = rand_0 * 0.5 * np.cos(np.linspace(0, rand_1 * np.pi, num=len(XY)))
            XY[:, 0] = _s.gi['ld'][0] + X * np.random.randint(low=5, high=30, size=1)[0]
            XY[:, 1] = _s.gi['ld'][1] + _s.o0.gi.o1_down_offsets[id_int] - np.sin(np.linspace(0, 0.5 * np.pi, num=len(XY))) * 700
            # if np.min(XY[:, 1]) < 0:
            #     raise Exception("o2 going out of frame")
            _s.XY = XY

            _s.rot = rot
            _s.cmap = random.choice(['afmhot', 'Wistia', 'cool', 'hsv', 'summer'])
            # _s.cmap = random.choice(['hsv'])

            _s.alphas = gen_alpha(_s, _type='o1_projectiles')

        elif _s.o0.id == 'clouds':

            # id_int = int(_s.id[-1])  # OBS. Used by o1_down_offsets
            # _s.gi['ld'][1] += _s.o0.gi.o1_down_offsets[id_int]  # NOT GOOD. dont change parameters

            '''30_ xys and thetas based on direction'''
            XY = np.zeros(shape=(_s.gi['frames_tot'], 2))
            # XY[:, 1] = _s.gi['ld'][1]  # y never changes

            X = np.linspace(0, 300, num=len(XY))
            Y = np.linspace(0, 100, num=len(XY))

            left_offset = np.random.randint(low=0, high=100, size=1)[0]
            down_offset = np.random.randint(low=0, high=50, size=1)[0]
            XY[:, 0] = _s.gi['ld'][0] + X + left_offset
            XY[:, 1] = _s.gi['ld'][1] - Y + down_offset
            _s.XY = XY

            rot = np.linspace(0, 0.2 * np.pi, num=len(XY))
            _s.rot = rot

            _s.scale = np.linspace(0.5, 1, num=len(XY))

            # _s.alphas = np.full(shape=(len(XY),), fill_value=1)
            _s.alphas = gen_alpha(_s, _type='o1_clouds')

    def set_frame_stop_to_sp_max(_s):
        """Loop through sps and set max to frame_stop"""

        _max = 0
        for sp_id, sp in _s.sps.items():
            if sp.frame_ss[1] > _max:
                _max = sp.frame_ss[1]

        _s.frame_ss[1] = deepcopy(_max) + 5