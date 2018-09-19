import math
import numpy as np
import more_itertools as mit

#	create a funtion to calculate the solid angle of a region. The function takes 
# 	an angle from the origin in degrees and returns the solid angle in square degrees of that area
def solid_angle(theta, type = "ster"):

	theta = math.radians(theta)

	#solid angle formula
	d_omega = 2*np.pi*(1-np.cos(theta))

	if (type == "ster"):
		return(d_omega)	
	if (type == "deg"):
		return(d_omega*(180/(np.pi))**2)
	else:
		return d_omega

#	solid_angle_strip is a function which calculates the solid angle of a strip of sky.
#	It takes in a scalar value dec1 which is the declination in degrees of the top vertical
#	extent desired of the strip, scalar value dec2 which is the declination in degrees of
# 	the bottom vertical extent of the strip, and scalar value extent which is the horizontal 
#	extent of the strip in degrees. If the horizontal extent is not given then it is assumed 
#	that the entire strip of the sphere is desired. absolute is a boolean value which can be 
#	changed if the user does not wish to find only the magnitude of the solid angle.
#	The function uses the function solid_angle and will work for any given declinations.
#	The function returns the solid angle of that strip.
def solid_angle_strip(dec1, dec2, extent = 360, absolute = True, type = "ster"):

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

	if (type=="ster"):
		return(d_omega)
	if (type == "deg"):	
		return(d_omega*(180/(np.pi))**2)
	else:
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

###	Finds the angular separation between two points.
###	Fairly self documenting.
def find_angular_separation(origin_RA, origin_DEC, point_RA, point_DEC):
	import astropy.units as u
	from astropy.coordinates import SkyCoord

	origin_coord = SkyCoord(origin_RA*u.deg, origin_DEC*u.deg)
	point_coord = SkyCoord(point_RA*u.deg, point_DEC*u.deg)


	return origin_coord.separation(point_coord)



#	poisson_prob(num_events,background) gives the probability as given by a Poisson distribution of 
#	finding num_events events given a constant independent background rate of background events in 
#	a specified area or time interval. 
#	The function takes in parameter num_events, the scalar value of the number of events which one wants 
#	to find the probability of occuring, and background, the constant rate of background events which 
#	occur independently of the space or time interval.
#	The function returns a scalar value the probability for each given value of num_events events occuring.
def poisson_prob(num_events,background):
	
	P_prob = ((background**num_events)/(math.factorial(num_events)))*np.exp(-background)

	return P_prob


#	A function that calculates the poisson probability for finding a number of events GREATER THAN or
#	EQUAL TO a given value Num_events. It will use the function poisson_prob() and sum over numbers up
#	to Num_events and will subtract these from one.
def summed_poisson_prob(Num_events, background):

	Prob = sum([poisson_prob(s, background) for s in range(Num_events)])

	summed_P_prob = 1 - Prob	

	return summed_P_prob		



#	Create 1257 randomised 'event times' in MJD which fit in the range of the
#	first measuring day and the last measuring day. It takes in the start date
#	in MJD of neutrino measurements at IceCube and the end date of measurements 
#	relevant to the data set.

def random_event_time(measuring_start, measuring_end):
	import random

	randomTime = random.uniform(measuring_start, measuring_end)

	return randomTime	



#	A function to find the liklihood
def liklihood(collection,all_neutrinos, inc = 0.1, log = True):

	N = collection.total_num_points
	Ts = 1/(collection.width)
	Tb = 1/(collection.total_time)
	maxL = math.log(10**-300)
	maxns = 0

	for ns in mit.numeric_range(0,N,inc):
	
		sum_of_logs = 0
		sum_of_logs_leftover = (N - len(collection.points))*math.log((1-ns/N)*Tb)

		product = 1
		for p in collection.points:
			sum_of_logs += math.log((ns/N)*p.weight*Ts + (1-ns/N)*Tb)

		if (log == False):
			L = math.exp(sum_of_logs + sum_of_logs_leftover)
		else:
			L = sum_of_logs + sum_of_logs_leftover

		if(L > maxL):
			maxL = L
			maxns = ns
	collection.liklihood = maxL
	collection.ns = maxns


#	Function to calculate a collection's test statistic
def test_stat(collection,all_neutrinos, log = True):

	Tw = collection.width
	if (log == False):
		L = math.log(collection.liklihood)
	else:
		L = collection.liklihood
	T = collection.total_time
	N = len(all_neutrinos)
	collection.TS = 2*(math.log(Tw) + L - (N+1)*math.log(T))			
