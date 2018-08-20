#create a funtion to calculate the solid angle of a region. The function takes 
# an angle from the origin in degrees and returns the solid angle of that area
def solid_angle(theta):
	import numpy as np 
	import math

	theta = math.radians(theta)

	#solid angle formula
	d_omega = 2*np.pi*(1-np.cos(theta))

	return(d_omega)	

#solid_angle_strip is a function which calculates the solid angle of a strip of sky.
#It takes in a scalar value theta1 which is the angle in degrees from vertical to 
# the top of the strip, scalar value theta2 which is the angle in degrees from
# vertical to the bottom of the strip, and scalar value extent which is the extent 
# of the strip in degrees.
#The function uses the function solid_angle
#The function returns the solid angle of that strip.
def solid_angle_strip(theta1, theta2, extent, abs=True)
	import numpy as np
	import math

	d_omega = (solid_angle(theta2) - solid_angle(theta1))*(extent/360)
	if(abs):
		d_omega = math.abs(d_omega)

	return(d_omega)