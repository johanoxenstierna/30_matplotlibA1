from src.gen_extent_triangles import *
from src.objects.abstract import AbstractObject
import P as P
# from projectiles.src.gen_colors import gen_colors
# import copy
import numpy as np

import random


class O0C(AbstractObject):

    def __init__(_s, pic, gi):
        super().__init__()
        _s.id = gi.id
        _s.gi = gi  # IMPORTANT replaces _s.gi = ship_info
        _s.pic = pic  # NOT SCALED
        _s.O1 = {}
        _s.O2 = {}  # only used by some insts