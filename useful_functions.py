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
#	It takes in a scalar value theta1 which is the angle in degrees from vertical to 
# 	the top of the strip, scalar value theta2 which is the angle in degrees from
# 	vertical to the bottom of the strip, and scalar value extent which is the extent 
# 	of the strip in degrees.
#	The function uses the function solid_angle
#	The function returns the solid angle of that strip.
def solid_angle_strip(theta1, theta2, extent, abs = True):
	import numpy as np
	import math

	d_omega = (solid_angle(theta2) - solid_angle(theta1))*(extent/360)
	if(abs):
		d_omega = math.abs(d_omega)

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
###	Note, the angles are the inner/outer. The order doesn't matter.
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