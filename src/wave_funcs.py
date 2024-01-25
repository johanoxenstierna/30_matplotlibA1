
import numpy as np
import copy
import matplotlib.pyplot as plt
from src.trig_functions import min_max_normalization
import random


def gerstner_wave(gi):

	"""
	Per particle! o2
	"""

	lam = 1.5  # np.pi / 2 - 0.07  # pi is divided by this, WAVELENGTH
	lam = 200  # np.pi / 2 - 0.07  # pi is divided by this, WAVELENGTH, VERY SENSITIVE
	k = 2 * np.pi / lam  # wavenumber
	c = 0.5
	# c = -np.sqrt(9.8 / k)
	steepness_abs = gi['steepness']

	left_start = gi['o1_left_start']

	frames_tot = gi['frames_tot']

	d = np.array([1, 1])
	# d = random.choice([np.array([0.3, 0.7]), np.array([0.4, 0.6])])

	# X = np.zeros((num_frames,))
	xy = np.zeros((frames_tot, 2))
	dxy = np.zeros((frames_tot, 3))

	'''Shifting is irrelevant here, because its done in o2 finish_info'''
	a = gi['ld'][0]  #- 4000  # OBS THIS IS 600
	z = gi['ld'][1]  #- 400  (formerly this was called y, but its just left_offset and y is the output done below)

	alphas = np.zeros(shape=(len(xy),))
	for w in range(2):  # NUM WAVES

		if w == 0:  # OBS ADDIND WAVES LEADS TO WAVE INTERFERENCE!!!
			d = np.array([1, 0])
			steepness_abs = 0.5
			c = 0.02  # prop to FPS EVEN MORE  from 0.2 at 20 FPS to. NEXT: Incr frames_tot for o2 AND o1
		elif w == 1:
			d = np.array([0.5, 1])
			steepness_abs = 0.3
			c = 0.06  # from 0.6 -> 0.06
		# else:
		# 	d = np.array([0.5, 0])
		# 	steepness = gi['steepness']

		stn = steepness_abs / k

		for i in range(0, frames_tot):  # could probably be replaced with np or atleast list compr

			f = k * np.dot(d, np.array([a, z])) - c * i  # uses x origin?

			xy[i, 0] += stn * np.cos(f)
			xy[i, 1] += stn * np.sin(f)

			dxy[i, 0] += 1 - stn * np.sin(f)
			dxy[i, 1] += stn * np.cos(f)  # THIS ONE WAS PROBABLY WRONGLY FLIPPED EARLIER.
			dxy[i, 2] += (stn * np.cos(f)) / (1 - stn * np.sin(f))  # gradient

	dxy[:, 0] = min_max_normalization(dxy[:, 0], y_range=[0.01, 2 * np.pi])
	dxy[:, 1] = min_max_normalization(dxy[:, 1], y_range=[0.01, 2 * np.pi])
	dxy[:, 2] = min_max_normalization(dxy[:, 2], y_range=[-0.99, 0.99])

	# alphas = np.full(shape=(len(dxy),), fill_value=left_start / np.pi)  # left_start ONLY affects o1
	# alphas = np.linspace(start=0.01, stop=0.99, num=frames_tot)

	'''NEED TO SHIFT BY LEFT START SOMEHOW'''
	alphas = xy[:, 0] + xy[:, 1] + dxy[:, 1]   # left_start ONLY affects o1
	alphas = min_max_normalization(alphas, y_range=[0.1, 0.5])

	return xy, alphas


def shift_wave(xy_t, origin=None, gi=None):
	"""
	OBS N6 = its hardcoded for sp
	shifts it to desired xy
	y is flipped because 0 y is at top and if flip_it=True
	"""

	xy = copy.deepcopy(xy_t)

	'''x'''
	xy[:, 0] += origin[0]  # OBS THIS ORIGIN MAY BE BOTH LEFT AND RIGHT OF 640

	'''
	y: Move. y_shift_r_f_d is MORE shifting downward (i.e. positive), but only the latter portion 
	of frames is shown.
	'''
	xy[:, 1] += origin[1]

	return xy


if __name__ == '__main__':  # cant be done in trig funcs main cuz circular import
	fig = plt.figure(figsize=(10, 5))
	gi = {}
	gi['ld'] = [0, 0]
	gi['steepness'] = 150
	gi['frames_tot'] = 300
	xy, alphas = gerstner_wave(gi=gi)

	ax1 = plt.plot(alphas)
	# ax1 = plt.plot(xy[:, 0])
	ax2 = plt.plot(xy[:, 1])  # obs flipped!!!
	plt.show()



# OLD WAVE


	# Y = np.zeros((num_frames,))
	# X[0] = 500
	# xy[0, :] = [600, 400]
	# inp_x = np.arange(0, num_frames)
	# inp_x = np.arange(0, num_frames)
	# for i in range(len(xy) - 1):
	# 	# X[i] = get_x(i, 50, 10)
	# 	# X[i + 1] = get_x(X[i], 10, i)
	# 	xy[i + 1, 0] = get_x(xy[i, 0], xy[i, 1], i)
	# 	xy[i + 1, 1] = get_y(xy[i, 0], xy[i, 1], i)
	#
	# 	aa = 5
	#
	# A = np.arange(0, 100)  # X
	# B = np.arange(0, 100)  # Y

	# if gi == None:
	# 	xy = None
	# 	return None, X
	# else:
	# 	xy = np.zeros((gi['frames_tot'], 2))  # MIDPOINT
	# 	xy[:, 0] = X
		# xy[:, 1] = 400
	#
	# lam = 100
	# k = 2 * np.pi / lam
	# c = 100
	#
	# # x = np.zeros(shape=(len(xy),))
	# a = np.arange(200, 400)
	# b = np.arange(400, 600)
	# # t = np.arange(0, 200)
	# # t = np.full(shape=(200,), fill_value=1)
	# t = np.arange(0, frames_tot)
	#
	# # f = k * (p.x - _Speed * _Time.y)
	# #
	# # x = a + (np.exp(k * b) / k) * np.sin(k * (a + c * t))
	# # y = b - (np.exp(k * b) / k) * np.cos(k * (a + c * t))
	#
	# # f = k * (p.x - _Speed * _Time.y)
	# # y = 10 * np.sin(k * (a))
	# y = 10 * np.sin(k * (a - c * t))
	# # x = np.sin(k * (a + c * t))
	# # y = -np.cos(k * (a + c * t))
	#
	# xy[:, 0] = a
	# xy[:, 1] = y

	# if gi != None: