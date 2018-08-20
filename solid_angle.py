#create a funtion to calculate the solid angle of a region. The function takes 
# an angle from the origin in degrees and returns the solid angle of that area
def solidAngle(theta):
	import numpy as np
	import math 

	theta = math.radians(theta)

	#solid angle formula
	d_omega = 2*np.pi*(1-np.cos(theta))

	return(d_omega)	
