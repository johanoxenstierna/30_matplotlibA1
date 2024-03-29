import os

import numpy as np

import P as P
from matplotlib.pyplot import imread

def load_pics():
    """LOADS BGR
    ch needed to see if smoka_hardcoded is used """

    pics = {}
    pics['O0'] = {}

    if P.MAP_DIMS[0] == 1280:
        pics['backgr_d'] = imread('./pictures/backgr.png')  # 482, 187
    elif P.MAP_DIMS[0] == 2560:
        pics['backgr_d'] = imread('./pictures/backgr_L.png')
    # pics['backgr_ars'] = imread('./pictures/backgr_ars.png')  # 482, 187

    # UNIQUE PICTURES FOR A CERTAIN OBJECT
    PATH = './pictures/'  # LOOPING OVER ALL O FOLDERS
    folder_names0 = P.O0_TO_SHOW
    for folder_name0 in folder_names0:  # shs

        pics['O0'][folder_name0] = {}

        folder_names1 = ['O1']

        for folder_name1 in folder_names1:
            try:
                _, _, file_names = os.walk(PATH + '/' + folder_name0 + '/' + folder_name1).__next__()
            except:
                print(folder_name1 + " does not exist for " + folder_name0)
                continue

            pics['O0'][folder_name0] = {folder_name1: {}}
            for file_name in file_names:
                if folder_name1 == 'O1':
                    pic = imread(PATH + folder_name0 + '/' + folder_name1 + '/' + file_name)  # without .png

                    if folder_name0 == 'projectiles':
                        for i in range(P.NUM_O1_PROJS):
                            pics['O0'][folder_name0][folder_name1][file_name[:-4] + '_' + str(i)] = pic

                    if folder_name0 == 'waves':
                        for i in range(P.NUM_O1_WAVES):
                            pics['O0'][folder_name0][folder_name1][str(i)] = pic

                    if folder_name0 == 'clouds':
                        # pic = np.flipud(pic)
                        for i in range(P.NUM_O1_CLOUDS):
                            pics['O0'][folder_name0][folder_name1][file_name[:-4] + '_' + str(i)] = pic

    return pics
