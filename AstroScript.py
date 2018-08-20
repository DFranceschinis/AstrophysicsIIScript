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

### Class for the data points

class neutrino(object):

	def __init__(self, MJD, RA, DEC, UNC, ENERGY):
		self.MJD = MJD
		self.RA = RA
		self.DEC = DEC
		self.UNC = UNC
		self.ENERGY = ENERGY
		#self.separation = find_angular_separation(ORIGIN_RA, ORIGIN_DEC, self.RA, self.DEC)

	# def __repr__(self):
	#     return ''.join("Neutrino Data Point: ","\tMJD: ",self.MJD,"\tRA: ",self.RA,"\tDEC",self.DEC,"\tUNC",self.UNC,"ENERGY: ",self.log10)

### Data Containers that are used to store the data that is processed.

NEUTRINOS = []

###

def process_all_files():
	""" This function will do all the data processing.
	"""

	#   Note, this function is local to this function, thus it won't have a name conflict with other functions.

	#   Clean up previous runs

	NEUTRINOS.clear()
	def process(mylist, lines, number):
		for i in lines:
			mylist.append(float((i.split())[number]))

	def process_the_file(name):
		FILE = open(os.path.join(__location__,"data", name), 'r')
		header = FILE.readline()
		for i in FILE:
			M,R,D,U,l = i.strip().split()
			NEUTRINOS.append(neutrino(M,R,D,U,l))
		

	for file in NAMES:
		process_the_file(file)


def plot():
	
	import matplotlib.pyplot as plt

	MJD = [neut.MJD for neut in NEUTRINOS]
	EN = [neut.ENERGY for neut in NEUTRINOS]

	plt.scatter(MJD, EN)
	plt.title("Energy vs MJD")
	plt.xlabel("MJD")
	plt.ylabel("Energy [log10]")
	plt.show()


def sky_map():
	import matplotlib
	import matplotlib.pyplot as plt
	import numpy as np
	from mpl_toolkits.axes_grid1 import make_axes_locatable

	RA = [neut.RA for neut in NEUTRINOS]
	DEC = [neut.DEC for neut in NEUTRINOS]
	EN = [neut.ENERGY for neut in NEUTRINOS]
	coords = [(R, D) for R in RA for D in DEC]
	

	fig = plt.figure()
	ax = fig.add_subplot(111)
	divider = make_axes_locatable(ax)
	cax = divider.append_axes('right', size='5%', pad=0.05)

	smap = ax.scatter(RA, DEC, label='IceCube Data', c = EN, cmap = 'BuPu', s = 50)
	ax.plot(ORIGIN_RA, ORIGIN_DEC, 'ro', label='TXS0506+056')
	ax.legend(loc="upper right")
	ax.set(title='Right Ascension and Declination of Data Readings', xlabel='Right Ascension (Degrees)', ylabel='Declination (Degrees)')
	fig.colorbar(smap, cax=cax, orientation='vertical', label='Energy')
	plt.show()      

### run this function to actually DO the stuff.
def run():

	process_all_files()
	plot()
	sky_map()

#	This allows the code to run if you just use $ python AstroScript
if __name__ == '__main__':
	run()
