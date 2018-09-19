#!/usr/bin/python3
from . import *

print ("These are the tests for the liklihood function!")

###	These functions will return a list of neutrinos that can be done for calculations

###	This function will return set of points spread evenly over a 10 day interval
###	and the time window
def test_data_001():
	returned_list = list()
	for i in range(0, 10, 1):
		returned_list.append(fake_neutrino(MJD = i, weight = 1))
	returned_period = fake_measure_period(start = 0, end = 10)
	returned_collection = fake_Collection(points = returned_list[:1], width = 1, total_num_points = 10, total_time = 10)

	return (returned_list, returned_period, returned_collection)

def test_data_002(weighting = 1):
	returned_list = list()
	returned_list.append(fake_neutrino(MJD = 5, weight = weighting))
	returned_list.append(fake_neutrino(MJD = 7, weight = 1))
	returned_period = fake_measure_period(start = 0, end = 10)
	returned_collection = fake_Collection(points = returned_list[:1], width = 1, total_num_points = 2, total_time = 10)

	return (returned_list, returned_period, returned_collection)
### -------------------------------------------------
###	REQUIREMENTS FOR LIKLIHOOD FUNCTION:
###	It requires a Collection:
###		points 			 : a list of points
###			weight		 : the point requires a weight
###		total_num_points : the # points inside the point list of the collection
###		width			 : Requires a width of the "collection window"
###		total_time	     : requires a length of the whole time interval it is searching over
###
###
###	It requires a list of all_neutrinos:
###		len 			 : the list only needs to be able to return a length
### -------------------------------------------------

### -------------------------------------------------
###	LIKLIHOOD RETURNS:
###		liklihood 	:	Returns a liklihood that is places into collection
###		ns 			:	returns an ns that is placed into collection
###	-------------------------------------------------


###	Input: None
###	Output: ???
def test_001(debug_text = False):
	neutrinos, period, collection = test_data_001()
	liklihood(collection, neutrinos,0.001)
	if (debug_text):
		collection.debug(ns = True, liklihood = True)
	return (collection)

def test_002(debug_text = False):
	neutrinos, period, collection = test_data_002()
	liklihood(collection, neutrinos,0.01)
	if (debug_text):
		collection.debug(ns = True, liklihood = True)
	return (collection)	

def test_003(debug_text = False, width_lower = 0, width_upper = 100, width_scale = 10):
	neutrinos, period, collection = test_data_002(weighting = 1.5)
	for i in range(width_upper, width_lower, -1):
		width = i / width_scale
		collection.width = width
		liklihood(collection, neutrinos, 0.01)
		if (debug_text):
			print("----- For width =", width, " -----")
			collection.debug(ns = True, liklihood = True)

def test_004(debug_text = False):
	neutrinos, period, collection = test_data_001()
	for i in range(1,11):
		print("For", i, "points inside the window!")
		collection.points = neutrinos[:i]
		liklihood(collection, neutrinos,0.001)
		if (debug_text):
			collection.debug(ns = True, liklihood = True)




def run_all_tests(debug_text = True):
	test_004(debug_text)

if __name__ == '__main__':
	print(__name__)
	run_all_tests()


