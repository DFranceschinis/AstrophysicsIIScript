#!/usr/bin/python3

import AstroScript
from useful_functions import *
import windowsearch as ws
import MatchedData as MD

###	These are classes meant to fake data points for functions. May or may not be useful.
###	These can be used in the same manner as the real points, just make sure the internal 
###	members and methods have the same names.


###	This will fake neutrinos.
###	It will take any data you give it and save it under what you need.
class fake_neutrino(object):

	def __init__(self, MJD = 0, RA = 0, DEC = 0, UNC = 0, ENERGY = 0, weight = 0, separation = 0, calc_sep = False, origin_dec = AstroScript.ORIGIN_DEC,
			origin_ra = AstroScript.ORIGIN_RA):
		self.MJD = MJD
		self.RA  = RA
		self.DEC = DEC
		self.UNC = UNC
		self.ENERGY = ENERGY
		self.weight = weight
		if (calc_sep):
			self.separation = find_angular_separation(origin_ra, origin_dec, self.RA, self.DEC)
		else:
			self.separation = separation


###	This will fake a measure period

class fake_measure_period(object):
	def __init__(self, start = 0, end = 0, density = 0, error = 0, line = ''):
		self.line = line
		self.start = start
		self.end  = end
		self.density = density
		self.error  = error	


###	This will fake a collection

class fake_Collection(object):
	def __init__(self, points = None, start_time = 0, end_time = 0, width = 0, total_num_points = 0, total_time = 0, likilihood = 0, ns = 0, TS = 0, p_value = 0):
		self.start_time = start_time
		self.end_time = end_time

		if (width == 0):
			self.width = end_time - start_time
		else:
			self.width = width

		self.midTime = start_time + (self.width / 2)
		self.points = points
		self.total_num_points = total_num_points
		self.total_time = total_time
		self.likilihood = likilihood
		self.ns = ns
		self.TS = TS
		self.p_value = p_value


	def debug(self, *args, **kwargs):
		for key, value in kwargs.items():
			if value != False:
				print(key, ":", getattr(self,key))

