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