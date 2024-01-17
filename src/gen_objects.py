import os
import json
import numpy as np
from src.load_pics import load_pics
from src.genesis import _genesis
import P as P
from src.objects.o0 import O0C
from src.objects.o1 import O1C
from src.objects.o2 import O2C


class GenObjects:

    """
    OBS this time it's only the background that is being ax.shown here. The other ax objects are added and
    deleted within the animation loop to save CPU-time.
    Each pic is tied to exactly 1 class instance and that class instance takes info from either o0 parent
    or other.
    """

    def __init__(_s):
        _s.pics = load_pics()
        _s.gis = _genesis()
        _s.PATH_IMAGES = './pictures/processed/'
        # _s.ch = ch

    def gen_backgr(_s, ax0, axs0, axs1):

        # if P.ARS == 0:  # shouldnt matter whether added to axs0 or axs1
        axs1.append(ax0.imshow(_s.pics['backgr_d'], zorder=1, alpha=1))  # index 0
        # else:
        # axs1.append(ax0.imshow(_s.pics['backgr_ars'], zorder=2, alpha=1))  # index 1

        ax0.axis([0, P.MAP_DIMS[0], P.MAP_DIMS[1], 0])
            # ax.axis([-30, 254, 133, -30])
            # ax.axis([0, 214, 0, 181])
            # ax.axis([0, 214, 181, 0])
            # ax.axis([0, 571, 0, 500])
        # else:
        #     ax.axis([0, 1280, 0, 720])
        # ax.invert_yaxis()  # ONLY IF SHIPS?
        # ax.grid()
        ax0.axis('off')  # TURN ON FOR FINAL

    def gen_O0(_s):
        """
        Base objects (ships but they may not always be ships).
        """
        O0 = {}
        for o0_id in P.O0_TO_SHOW:  # number_id
            o0_gi = _s.gis[o0_id]
            O0[o0_id] = O0C(pic=None, gi=o0_gi)  # No pic CURRENTLY

        return O0

    def gen_O1(_s, O0):

        """O1"""
        for o0_id, o0 in O0.items():
            # if 'O1' in o0.gi.child_names:
            O1_pics = _s.pics['O0'][o0_id]['O1']  # OBS THEY ARE DUPLICATED
            # sp_id_int = 0  # since there may be multiple f
            for pic_key, pic in O1_pics.items():
                # pic_enumer = pic_key.split('_')
                # pic_enumer = int(pic_enumer[-1])
                o1 = O1C(o1_id=pic_key, pic=pic, o0=o0)  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?

                '''THIS WILL PROBABLY DEPEND ON WAVE OR PROJECTILE'''
                if o1.o0.id == 'projectiles':
                    num_o2_per_o1 = P.NUM_PROJ_O2_PER_O1
                elif o1.o0.id == 'waves':
                    num_o2_per_o1 = P.NUM_WAVE_O2_PER_O1
                else:
                    num_o2_per_o1 = 0

                for i in range(num_o2_per_o1):
                    o2 = O2C(o0, i, o1)
                    o0.O2[o2.id] = o2
                    o1.O2[o2.id] = o2  # why not use both
                    # sp_id_int += 1

                o0.O1[pic_key] = o1

        return O0
