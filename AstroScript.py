"""
		Astrophysics II Neutrino Practical Module
		Contributors:   Shayne Doddrell         
						Daniel Franceschinis    
						Kendall Jenner          
						Muskan Pathak           
						Gary Hill               

		This is the module that encompasses all the code that will be used for the practical. 
		If this document becomes unwieldy, it can be split into multiple files.
		If managing this project becomes unwieldy, it can be maintained on github.
		Don't be afraid to study this document. You might learn some python!

		I recommend editing this document using sublime text!
			https://www.sublimetext.com/3



		This can be run using the following processes.
		Make sure that this script is in the same folder as the files downloaded from this source
			https://icecube.wisc.edu/science/data/TXS0506_point_source

		If you're using the terminal. Make sure that you are in the correct directory, by typing:
			cd [DIR]
		where [DIR] is the directory that you've placed the script and the downloaded files

		There are two ways you can run the script. The first way will just produce the plots straight up.
		The second way is useful if you wish to be able to play with the data and work with the script rather than
		just generate the plots.

		First way: type into your terminal: 
			python AstroScript				[If it doesn't work, you might need to type python3 instead, and you
												might also need to type AstroScript.py instead, depends on the system.]

		Second Way: Type into your terminal the following:
			python                          [This will open up python for you, giving you some information,
												It should say python 3.x. If it says python 2.7,
												exit using quit() and type python3 instead]
			import AstroScript              [This will import the module]
			AstroScript.run()               [This will actually do all the running]
		That should work.


		If you're using IDLE. Run these commands.
			import sys
			sys.path.append("[DIR]")

		[DIR] needs to be the path where your files are located. If you're on windows, there will be
		slashes as part of your directory, ex: \Astrophysics II\Practical\Group, these need replaced with
		double slashes, ex: \\Astrophysics II\\Practical\\Group.
		Don't forget the quotes!

		Once that is done. Run these commands:
			import AstroScript
			AstroScript.run()



		If you can't get this all working, email me or complain to me in person [Daniel].


###

		Things to do:
			Play with the plotting to make the data look prettier.
			Start writing functions for analysing the data containers (ex: for the )


###

"""
### Useful functions that we will regularly use go in this file. This is mainly for organisational purposes.

from useful_functions import *
import datetime	
import astropy
from astropy.time import Time

### Set up the location of the files. Make sure the files are in the same directory as this script.

import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

###

### Set up the files to be processed and used as data.

NAMES = []
NAMES.append("events_IC40.txt")
NAMES.append("events_IC59.txt")
NAMES.append("events_IC79.txt")
NAMES.append("events_IC86a.txt")
NAMES.append("events_IC86b.txt")
NAMES.append("events_IC86c.txt")

### Contain the coordinates for the proposed source

ORIGIN_RA = 77.3582
ORIGIN_DEC = 5.69314

MAX_SEP = 0
TOTAL_AREA = 0

### Class for the data points

class neutrino(object):

	def __init__(self, MJD, RA, DEC, UNC, ENERGY):
		global MAX_SEP
		self.MJD = MJD
		self.RA = RA
		self.DEC = DEC
		self.UNC = UNC
		self.ENERGY = ENERGY
		self.separation = find_angular_separation(ORIGIN_RA, ORIGIN_DEC, self.RA, self.DEC)
		if self.separation > MAX_SEP:
			MAX_SEP = self.separation

	# def __repr__(self):
	#     return ''.join("Neutrino Data Point: ","\tMJD: ",self.MJD,"\tRA: ",self.RA,"\tDEC",self.DEC,"\tUNC",self.UNC,"ENERGY: ",self.log10)

#	class to hold the information of each of the measuring periods of IceCube
class measure_period(object):

	def __init__(self,line):
		

		self.line = line
		name, st_yr, st_mth, st_day, end_yr, end_mth, end_day, density, _, error = line.strip().split()
		st_date = st_yr+st_mth+st_day
		end_date = end_yr+end_mth+end_day
		start  = datetime.datetime.strptime(st_date, '%Y%b%d')
		end = datetime.datetime.strptime(end_date, '%Y%b%d')
		self.start = Time(start, format='datetime').mjd
		self.end = Time(end, format='datetime').mjd
		self.density = float(density)
		self.error = (float(error[:-1]))/100

### Data Containers that are used to store the data that is processed.

NEUTRINOS = []
PERIODS = []
RANDNEUTRINOS = []

###

def process_all_files():
	""" This function will do all the data processing.
	"""
	global RANDNEUTRINOS

	#   Note, this function is local to this function, thus it won't have a name conflict with other functions.

	#   Clean up previous runs
	print(RANDNEUTRINOS)
	NEUTRINOS.clear()
	PERIODS.clear()
	RANDNEUTRINOS.clear()

	def process(mylist, lines, number):
		for i in lines:
			mylist.append(float((i.split())[number]))

	def process_the_file(name):
		FILE = open(os.path.join(__location__,"data", name), 'r')
		header = FILE.readline()
		for i in FILE:
			M,R,D,U,l = i.strip().split()
			NEUTRINOS.append(neutrino(float(M),float(R),float(D),float(U),float(l)))
			RANDNEUTRINOS.append(neutrino(None,float(R),float(D),float(U),float(l)))
		
	FILE = open(os.path.join(__location__,"data/list_of_samples.txt")).readlines()
	firstLine = FILE.pop(0)
	for line in FILE:

		PERIODS.append(measure_period(line))

	for file in NAMES:
		process_the_file(file)

	global TOTAL_AREA	
	TOTAL_AREA = solid_angle(MAX_SEP.value,type="deg")

	#	Create a random time array to use for the randomised neutrino events
	randomTimes = randomised_times()
	print(len(randomTimes))
	print(len(RANDNEUTRINOS))

	#	Replace the None value in RANDNEUTRINOS with the randomised times 
	for i in range(len(RANDNEUTRINOS)):
		if(RANDNEUTRINOS[i].MJD == None):
			RANDNEUTRINOS[i].MJD = randomTimes[i]
		else:
			print("uh oh")	

def plot():
	
	import matplotlib.pyplot as plt

	MJD = [neut.MJD for neut in NEUTRINOS]
	EN = [neut.ENERGY for neut in NEUTRINOS]

	fig1 = plt.figure(1)
	ax = fig1.add_subplot(111)
	ax.scatter(MJD, EN)
	ax.set(title="Energy vs MJD",xlabel="MJD",ylabel="Energy [log10]")
	

def window_search(Neutrino_list, Period_list, start_time, end_time, window_size, p_value):
	###	This will search through all windows. It will test the p_values using the poisson distribution
	###	and return all that are above a certain threshold
	matching_collections = []
	for collection in Time_window_searcher(start_time, end_time, window_size, Neutrino_list):
		total_p_value = 1
		for window in event_density_windows(Neutrino_list, Period_list):
			###	Collection[1] is the start time of the collection, window[0].start is the start of this time block
			###	Finding the max wwill find the lower bounds to determine the density
			time_start = max(collection[1], window[0].start)
			time_end = min(collection[2], window[0].end)

			window_density = window[0].density * TOTAL_AREA * (time_end - time_start)/(window[0].end - window[0].start)
			p_value = poisson_prob(len(window[1]), window_density)

			total_p_value *= p_value #### 	I think this is how you can calculate it? Check with someone 
									###		More knowledgable than me.

		if (total_p_value <= p_value):
			matching_collections.append(collection)


def test_window_search():
	###	This will collect the windows. I will now find the expected number per time window, and if
	###	it is less than the actual number, print it.
	All = list()
	total_counted = 0
	for collection in Time_window_searcher(PERIODS[0].start, PERIODS[-1].end, 10000, NEUTRINOS):
		print("I have a collection:", collection[1], collection[2])	#	This is working (apparently)
		total_expected = 0
		index = -1
		total_counted += 1
		for window in event_density_windows(NEUTRINOS, PERIODS):
			index += 1
			###	Collection[1] is the start time of the collection, window[0].start is the start of this time block
			###	Finding the max will find the lower bounds to determine the density
			time_start = max(collection[1], window[0].start)
			time_end = min(collection[2], window[0].end)
			if time_start > time_end or time_end < time_start:
				continue
			expected = TOTAL_AREA * window[0].density * (time_end-time_start)/(window[0].end - window[0].start)
			total_expected = total_expected + expected
			print(index,time_end, time_start,time_end - time_start, window[0].density,len(collection[0]), len(window[1]),total_expected)
		if (len(collection[0]) > total_expected):
			All.append(collection)
	print(len(All), "/", total_counted)
	return(All)





def sky_map():
	import matplotlib
	import matplotlib.pyplot as plt
	import numpy as np
	from mpl_toolkits.axes_grid1 import make_axes_locatable

	RA = [neut.RA for neut in NEUTRINOS]
	DEC = [neut.DEC for neut in NEUTRINOS]
	EN = [neut.ENERGY for neut in NEUTRINOS]
	coords = [(R, D) for R in RA for D in DEC]
	

	fig2 = plt.figure(2)
	ax = fig2.add_subplot(111)
	divider = make_axes_locatable(ax)
	cax = divider.append_axes('right', size='5%', pad=0.05)

	smap = ax.scatter(RA, DEC, label='IceCube Data', c = EN, cmap = 'BuPu', s = 50)
	ax.plot(ORIGIN_RA, ORIGIN_DEC, 'ro', label='TXS0506+056')
	ax.legend(loc="upper right")
	ax.set(title='Right Ascension and Declination of Data Readings', xlabel='Right Ascension (Degrees)', ylabel='Declination (Degrees)')
	fig2.colorbar(smap, cax=cax, orientation='vertical', label='Energy')
	    


#	randomised_times creates an array of random 'event' times in MJD.
def randomised_times():
	starts = [st.start for st in PERIODS]
	ends = [en.end for en in PERIODS]

	events1 = 0
	events2 = 0
	events3 = 0
	events4 = 0
	events5 = 0
	events6 = 0
	overflow = 0
	randomTimeArray = []

	for event in NEUTRINOS:

		if(event.MJD >= starts[0] and event.MJD <= ends[0]):
			events1+=1
		elif(event.MJD > starts[1] and event.MJD <= ends[1]):
			events2+=1
		elif(event.MJD > starts[2] and event.MJD <= ends[2]):
			events3+=1
		elif(event.MJD > starts[3] and event.MJD <= ends[3]):
			events4+=1			
		elif(event.MJD > starts[4] and event.MJD <= ends[4]):
			events5+=1	
		elif(event.MJD > starts[5] and event.MJD <= ends[5]):
			events6+=1	
		else:
			overflow+=1	

		

	for i in range(events1):	
		randomTimeArray.append(random_event_time(starts[0],ends[0]))
	for i in range(events2):
		randomTimeArray.append(random_event_time(starts[1],ends[0]))
	for i in range(events3):
		randomTimeArray.append(random_event_time(starts[2],ends[2]))
	for i in range(events4):
		randomTimeArray.append(random_event_time(starts[3],ends[3]))
	for i in range(events5):
		randomTimeArray.append(random_event_time(starts[4],ends[4]))
	for i in range(events6+overflow):
		randomTimeArray.append(random_event_time(starts[5],ends[5]))				


	return randomTimeArray	




#	Function to create a histogram of the log of the probabilities
#	The function takes in an array of probability values and plots 
#	a histogram of their log10 values.
def prob_histogram(probabilities):
	import matplotlib.pyplot as plt
	import math

	log_probs = [math.log10(p) for p in probabilities]

	fig3 = plt.figure(3)
	ax = fig.add_subplot(111)
	ax.hist(log_probs,bins=20)
	ax.set(title="Log10 of the Probabilities",xlabel="log(P)")
	


### run this function to actually DO the stuff.
def run():
	import matplotlib.pyplot as plt

	process_all_files()
	plot()
	sky_map()
	plt.show()

#	This allows the code to run if you just use $ python AstroScript
if __name__ == '__main__':
	run()
