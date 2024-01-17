"""
Matplotlib animation of projectiles, waves and clouds
"""

import numpy as np
import random
random.seed(7)  # ONLY HERE
np.random.seed(7)  # ONLY HERE
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src import gen_objects
from src.ani_helpers import *
import P as P

WRITE = 0
FPS = 80

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, bitrate=3600)

fig, ax_b = plt.subplots(figsize=(10, 6))

axs0 = []
axs1 = []

g = gen_objects.GenObjects()
g.gen_backgr(ax_b, axs0, axs1)

O0 = g.gen_O0()
O0 = g.gen_O1(O0)

brkpoint = ''
'''VIEWER ==========================================='''


def init():
    return axs0 + axs1


def animate(i):

    prints = "i: " + str(i) + "  len_axs0: " + str(len(axs0)) + "  len_axs1: " + str(len(axs1))

    for o0_id, o0 in O0.items():

        for o1_id, o1 in o0.O1.items():  # this loop is super fast

            if i in o1.gi['init_frames']:

                if o1.drawn == 0:
                    prints += "  adding f"
                    exceeds_frame_max, how_many = o1.check_frame_max(i, o1.gi['frames_tot'])
                    if exceeds_frame_max == True:
                        print("EXCEEDS MAX. This means objects at end of animation will go faster. \n")
                        o1.gi['frames_tot'] = how_many

                    o1.dyn_gen()
                    o1.drawn = 1  # this variable can serve multiple purposes (see below, and in set_clock)
                    o1.set_frame_ss(i, o1.gi['frames_tot'])  # uses AbstractSSS

                    ''' EVIL BUG HERE. An o1 cannot be allowed to init new O2 children if old children
                    are still being drawn!!! THIS MEANS o1 FRAMES_TOT MUST > O2 FRAMES TOT
                    UPDATE: Try releasing o1 once max frame stop of its sps reached. '''

                    for o2_key, o2 in o1.O2.items():  # THEY ARE ONLY INITED HERE
                        '''YES KEEP THIS: there are thousands of sp and pre-storing xy for all is a bit crazy.'''
                        o2.dyn_gen(i)
                        prints += "  adding o2"
                        o2.set_frame_ss(o2.init_frame, o2.gi['frames_tot'])

                    # o1.set_frame_stop_to_sp_max()  # really good but not now.
                else:
                    prints += "  no free f"
                adf = 5

        for o1_id, o1 in o0.O1.items():  # this is where most of the CPU time goes

            if o1.drawn != 0:  # Its not just boolean!
                o1.set_clock(i)

                drawBool, index_removed = o1.ani_update_step(ax_b, axs0, axs1)
                if drawBool == 0:  # dont draw
                    continue
                elif drawBool == 1:  # continue drawing
                    set_O1(o1, ax_b, axs0)
                elif drawBool == 2:  # remove
                    prints += "  removing o1"
                    decrement_all_index_axs0(index_removed, O0)
                for o2_id, o2 in o1.O2.items():  # CHILD OF f
                    assert(o2.o1 != None)
                    if o2.init_frame == i:
                        o2.drawn = 1
                        # o2.set_frame_ss(i, o2.gi['frames_tot'], dynamic=False)  # MOVED UP
                    if o2.drawn != 0:  # This is the new condition. Hence it doesnt use f here. So f drawn does not have to be true.
                        o2.set_clock(i)
                        drawBoolSP, index_removed = o2.ani_update_step(ax_b, axs0, axs1, o2=True)  # ADDED TO axs
                        if drawBoolSP == 0:
                            continue
                        elif drawBoolSP == 1:
                            '''
                            OBS AXS_0 POPULATED HERE. FOR NEXT PROJECT IT SHOULD NOT BE DONE HERE
                            ??? Where else could it be done?
                            '''
                            set_O2(o2, axs0, axs1, ax_b, i)  # FRAME_SS[1] CAN BE OVERRIDDEN HERE. IF SO, this is the last drawn. NO! moved to pre
                        if drawBoolSP == 2:
                            prints += "  removing o2"
                            decrement_all_index_axs0(index_removed, O0)

    print(prints)

    return axs0 + axs1  # 0 for dynamic objects, 1 for background


sec_vid = ((P.FRAMES_STOP - P.FRAMES_START) / FPS)
min_vid = ((P.FRAMES_STOP - P.FRAMES_START) / FPS) / 60
print("len of vid: " + str(sec_vid) + " s" + "    " + str(min_vid) + " min")

start_t = time.time()
ani = animation.FuncAnimation(fig, animate, frames=range(P.FRAMES_START, P.FRAMES_STOP),
                              blit=True, interval=1, init_func=init,
                              repeat=False)  # interval only affects live ani. blitting seems to make it crash

if WRITE == 0:
    plt.show()
else:
    ani.save('./vids/vid_' + str(WRITE) + '.mp4', writer=writer)

    # ani.save('./vids/vid_' + str(WRITE) + '.mov',
    #          codec="png",
    #          dpi=100,
    #          fps=40,
    #          bitrate=3600)

    # THIS ONE!!!
    # ani.save('./vids/vid_' + str(WRITE) + '.mov',
    #          codec="png",
    #          dpi=100,
    #          fps=FPS,
    #          bitrate=3600,
    #          savefig_kwargs={"transparent": True, "facecolor": "none"})

tot_time = round((time.time() - start_t) / 60, 4)
print("minutes to make animation: " + str(tot_time) + " |  min_gen/min_vid: " + str(tot_time / min_vid))  #
