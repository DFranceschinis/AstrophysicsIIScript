#	create a funtion to calculate the solid angle of a region. The function takes 
# 	an angle from the origin in degrees and returns the solid angle of that area
def solid_angle(theta):
	import numpy as np 
	import math

	theta = math.radians(theta)

	#solid angle formula
	d_omega = 2*np.pi*(1-np.cos(theta))

	return(d_omega)	

#	solid_angle_strip is a function which calculates the solid angle of a strip of sky.
#	It takes in a scalar value dec1 which is the declination in degrees of the top vertical
#	extent desired of the strip, scalar value dec2 which is the declination in degrees of
# 	the bottom vertical extent of the strip, and scalar value extent which is the horizontal 
#	extent of the strip in degrees. If the horizontal extent is not given then it is assumed 
#	that the entire strip of the sphere is desired. absolute is a boolean value which can be 
#	changed if the user does not wish to find only the magnitude of the solid angle.
#	The function uses the function solid_angle and will work for any given declinations.
#	The function returns the solid angle of that strip.
def solid_angle_strip(dec1, dec2, extent = 360, absolute = True):
	import numpy as np
	import math

	formula = np.sign(dec1)*np.sign(dec2)

	dec1 = abs(dec1)
	dec2 = abs(dec2)
	theta1 = 90-dec1
	theta2 = 90-dec2

	if formula == -1:
		d_omega = (4*np.pi - solid_angle(theta1) - solid_angle(theta2))*(extent/360)
	else:	
		d_omega = (solid_angle(theta2) - solid_angle(theta1))*(extent/360)
	if absolute:
		d_omega = abs(d_omega)

	return(d_omega)

###	This will take an origin point and find all the points (pass as list) that are within max_angle of them
###	Returns a list of all the points. Iterate over the list if you want to do stuff with them.
###	Take the length of the list if you want to count them
def find_points_within_angle(origin_RA, origin_DEC, points, max_angle):
	matches = []

	for p in points:
		if find_angular_separation(origin_RA, origin_DEC, p.RA, p.DEC) <= max_angle:
			matches.append(p)

	return matches

###	This will take two angles for the inner and outer edges of the strip and the points
###	This will return a list of the points that are in the region.
###	num_eventsote, the angles are the inner/outer. The order doesn't matter.
def find_points_in_strip(theta1, theta2, points):
	matches = []

	for p in points:
		if (p.DEC >= theta1 and p.DEC <= theta2) or (p.DEC <= theta1 and p.DEC >= theta2):
			matches.append(p)

	return matches

###	This will find any points within a time window.
###	This maybe work with rearranging the points in strip function but oh well
###	This takes a start time, an end time, and the array of points.
def find_points_in_time_window(timestart, timeend, points):
	matches = []

	for p in points:
		if (p.MJD >= timestart) and (p.MJD <= timeend):
			matches.append(p)

	return matches

###	Finds the angular separation between two points.
###	Fairly self documenting.
def find_angular_separation(origin_RA, origin_DEC, point_RA, point_DEC):
	import astropy.units as u
	from astropy.coordinates import SkyCoord

	origin_coord = SkyCoord(origin_RA*u.deg, origin_DEC*u.deg)
	point_coord = SkyCoord(point_RA*u.deg, point_DEC*u.deg)


	return origin_coord.separation(point_coord)

###	This class will allow you to iterate over every time window
###	Instead of returning all the time windows (which would suck),
###	it does each calculation every time you call next
###	You should work with this by making it a variable
### and then looping over the variable
### ex:		windows = Time_window_searcher(start, end, size, points)
###			for win in windows:
###					# Do stuff with the window

class Time_window_searcher(object):
	def __init__(self, time_start, time_end, time_window_size, points):
		self.time_start = float(time_start)
		self.time_end = float(time_end)
		self.time_window_size = float(time_window_size)
		self.points = points

	def __iter__(self):
		###	This doesn't necessarily need to return self, but will for now.
		self.cur_start = self.time_start
		self.cur_end = self.time_start + self.time_window_size
		return self

	def __next__(self):
		if self.cur_start >= self.time_end:
			raise StopIteration
		if self.cur_end >= self.time_end:
			###	This implementation detail is probably best
			self.cur_end = self.time_end

		window = find_points_in_time_window(self.cur_start, self.cur_end, self.points)
		start = self.cur_start
		end = self.cur_end
		self.cur_start, self.cur_end = self.cur_end, self.cur_end + self.time_window_size
		return (window, start, end)


#	poisson_prob(num_events,background) gives the probability as given by a Poisson distribution of 
#	finding num_events events given a constant independent background rate of background events in 
#	a specified area or time interval. 
#	The function takes in parameter num_events, the scalar value of the number of events which one wants 
#	to find the probability of occuring, and background, the constant rate of background events which 
#	occur independently of the space or time interval.
#	The function returns a scalar value the probability for each given value of num_events events occuring.
def poisson_prob(num_events,background):
	import numpy as np
	import math
	
	P_prob = ((background**n)/(math.factorial(n)))*np.exp(-background)

	return P_prob
			


###	Split a list of points into sublists that are split according to time intervals
###	that are described by the event density windows that are processed seperately.
###	It returns a list of tuples. Each of these tuples contains the time window (so you can find the density),
###	and a list of all points in that time window

def event_density_windows(point_list, window_list):
	final_list = list()
	for window in window_list:
		new_list = list()
		for point in point_list:
			if (point.MJD >= window.start and point.MJD <= window.end):
				new_list.append(point)
		final_list.append((window, new_list))
	return final_list


#	Create 1257 randomised 'event times' in MJD which fit in the range of the
#	first measuring day and the last measuring day. It takes in the start date
#	in MJD of neutrino measurements at IceCube and the end date of measurements 
#	relevant to the data set.

def random_event_time(measuring_start, measuring_end):
	import random

	randomTime = random.uniform(measuring_start, measuring_end)

	return randomTime	