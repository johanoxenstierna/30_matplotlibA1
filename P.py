
'''These are dimensions for backr pic. Has a huge impact on cpu-time'''
MAP_DIMS = (1280, 720)  #(233, 141)small  # NEEDED FOR ASSERTIONS
# MAP_DIMS = (2560, 1440)  #(233, 141)small
# MAP_DIMS = (3840, 2160)  #(233, 141)small

FRAMES_START = 0
FRAMES_STOP = 2000

FRAMES_TOT = FRAMES_STOP - FRAMES_START

# A (what to animate) ========
# A_O2 = 1
# A_O1 = 1

NUM_O1_PROJS = 3  # this is multiplied with num pics
NUM_PROJ_O2_PER_O1 = 20  # used by 0, 5, 6  can be reduced for big bug

NUM_O1_WAVES = 5  # 15  # these two give xz wave mesh extent
NUM_WAVE_O2_PER_O1 = 15  #30  # 20 HAS IMPACT ON WAVE

NUM_O1_CLOUDS = 20  # 20  # per pic  720 (called x in the name)
NUM_INIT_FRAMES_CLOUD = 5

O0_TO_SHOW = ['projectiles']
# O0_TO_SHOW = ['waves']
# O0_TO_SHOW = ['clouds']
# O0_TO_SHOW = ['projectiles', 'waves', 'clouds']
