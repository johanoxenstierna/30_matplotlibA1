
import cv2
import numpy as np
import random
import P
from scipy.stats import multivariate_normal
from src.trig_functions import min_max_normalization
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt

def decrement_all_index_axs0(index_removed, O0, waves=None):
	"""
	Whenever an axs0 is popped from the list, all index_axs0 with higher index will be wrong and
	need to be decremented by 1.
	For now it seems to only work with axs0
	"""

	for o0 in O0.values():
		if o0.index_axs0 != None:
			if o0.index_axs0 > index_removed:
				o0.index_axs0 -= 1
		for o1 in o0.O1.values():
			if o1.index_axs0 != None:
				if o1.index_axs0 > index_removed:
					o1.index_axs0 -= 1

			for o2_key, o2 in o1.O2.items():  # OBS THIS MEANS sps must have same or fewer frames than f
				if o2.index_axs0 != None:
					if o2.index_axs0 > index_removed:
						o2.index_axs0 -= 1

	# '''
	# PAINFUL 30 min BUG HERE
	# DANGER: THIS SEEMS TO MESS UP ABOVE: SOLUTION: ALWAYS HAVE SP AS CHILD OF SR
	# '''
	# for sp_key, sp in sh.sps.items():
	# 	if sp.index_axs0 != None and sp.o1 == None:
	# 		if sp.index_axs0 > index_removed:
	# 			sp.index_axs0 -= 1


def set_O1(o, ax_b, axs0):
	""""""
	if o.o0.id == 'projectiles':
		M = mtransforms.Affine2D(). \
			    rotate(o.rot[o.clock]). \
			    translate(o.XY[o.clock][0], o.XY[o.clock][1]) + ax_b.transData

		# LEGACY:
		# if g_obj.id[0] in ['0', '5']:
		# 	M = mtransforms.Affine2D(). \
		# 			scale(g_obj.scale_vector[g_obj.clock], -g_obj.scale_vector[g_obj.clock]). \
		# 			rotate(g_obj.rotation_v[g_obj.clock]). \
		# 			translate(g_obj.gi['ld'][0], g_obj.gi['ld'][1]) + ax0.transData
		# elif g_obj.id[0] in ['6']:
		# 	try:
		# 		M = mtransforms.Affine2D(). \
		# 				scale(g_obj.scale_vector[g_obj.clock], -g_obj.scale_vector[g_obj.clock]). \
		# 				rotate(g_obj.rotation_v[g_obj.clock]). \
		# 				translate(g_obj.gi['ld'][0] + g_obj.gi['x_mov'][g_obj.clock], g_obj.gi['ld'][1]) + ax0.transData
		# 	except:
		# 		adf = 6
		# elif g_obj.id[0] in ['1']:  # YES, 1 has f shockwave
		# 	M = mtransforms.Affine2D(). \
		# 			scale(g_obj.scale_vector[g_obj.clock], -g_obj.scale_vector[g_obj.clock]). \
		# 			rotate(g_obj.rotation_v[g_obj.clock]). \
		# 			translate(g_obj.gi['ld'][0] + g_obj.gi['x_mov'][g_obj.clock],
		# 					  g_obj.gi['ld'][1] + g_obj.gi['y_mov'][g_obj.clock]) + ax0.transData
		# elif g_obj.id[2:4] == 'sr':
		# 	M = mtransforms.Affine2D(). \
		# 			scale(g_obj.scale_vector[g_obj.clock], -g_obj.scale_vector[g_obj.clock]). \
		# 			rotate(g_obj.rotation_v[g_obj.clock]). \
		# 			translate(g_obj.xy[g_obj.clock][0], g_obj.xy[g_obj.clock][1]) + ax0.transData
		# elif g_obj.id[2] == 'r':
		# 	M = mtransforms.Affine2D(). \
		# 			rotate_around(4, 6, g_obj.rotation_v[g_obj.clock]). \
		# 			scale(g_obj.scale, -g_obj.scale). \
		# 			translate(g_obj.xy[g_obj.clock][0], g_obj.xy[g_obj.clock][1]) + ax0.transData
		# elif g_obj.id[2] == 'l':
		# 	M = mtransforms.Affine2D(). \
		# 			rotate_around(4, 6, g_obj.gi['rad_rot']). \
		# 			scale(g_obj.gi['scale'], -g_obj.gi['scale']). \
		# 			translate(g_obj.gi['ld'][0], g_obj.gi['ld'][1]) + ax0.transData

		o.ax0.set_alpha(o.alphas[o.clock])
	elif o.o0.id == 'clouds':
		M = mtransforms.Affine2D(). \
				scale(o.scale[o.clock]). \
				rotate(o.rot[o.clock]). \
				translate(o.XY[o.clock][0], o.XY[o.clock][1]) + ax_b.transData
		o.ax0.set_alpha(o.alphas[o.clock])
	else:
		return

	o.ax0.set_transform(M)


def set_O2(o2, axs0, axs1, ax_b, ii):

	sp_len_cur = o2.sp_lens[o2.clock]

	if o2.o0.id == 'projectiles':
		if o2.clock < sp_len_cur + 1:  # beginning
			xys_cur = [o2.xy[:o2.clock, 0], o2.xy[:o2.clock, 1]]  # list with 2 cols
		else:
			xys_cur = [o2.xy[o2.clock:o2.clock + sp_len_cur, 0], o2.xy[o2.clock:o2.clock + sp_len_cur, 1]]
	elif o2.o0.id == 'waves':
		if o2.clock < sp_len_cur + 1:  # beginning
			xys_cur = [o2.xy[:o2.clock, 0], o2.xy[:o2.clock, 1]]  # list with 2 cols
		else:
			xys_cur = [o2.xy[o2.clock, 0], o2.xy[o2.clock, 1]]

	# axs0[o2.index_axs0].set_data(xys_cur)  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED
	axs0[o2.index_axs0].set_data(xys_cur)  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED
	plt.setp(axs0[o2.index_axs0], markersize=10)

	if o2.o0.id == 'projectiles':
		axs0[o2.index_axs0].set_color((o2.R[o2.clock], o2.G[o2.clock], o2.B[o2.clock]))
	# axs0[sp.index_axs0].set_color('black')  # OBS
	# try:
	axs0[o2.index_axs0].set_alpha(o2.alphas[o2.clock])
	# except:
	# 	adf = 5




# def add_to_ars(sp, axs0):
#
# 	'''The main point of this is not to achieve any animation speed-up, which it wont, but rather
# 	to make things more sensical.'''
#
# 	'''Here add xy limit condition to see whether the arrow is actually relevant for ars'''
#
# 	aa = 5


