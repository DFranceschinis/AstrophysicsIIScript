###	This is the window search tools for the program

from useful_functions import *
from scipy.stats import poisson

###	CONTAINER CLASSES:
###	These are to simplify the data stores.

class Collection(object):
	def __init__(self, points = None, start = 0, end = 0):
		self.start_time = start
		self.end_time = end
		self.width = end - start
		self.midTime = start  + (self.width / 2)
		self.points = points
		self.p_value = 1

	def __repr__(self):
		return ("Mid time: " + str(self.midTime) + " Width:" +  str(self.width) + " # Points:"  + str(len(self.points)) + " p_value" + str(self.p_value))



def summed_poisson_prob_new(Num_events, background):
	summed_P_prob = 1 - poisson.cdf(Num_events, background)	

	return summed_P_prob



###	This class will allow you to iterate over every time window
###	Instead of returning all the time windows (which would suck),
###	it does each calculation every time you call next
###	You should work with this by making it a variable
### and then looping over the variable
### ex:		windows = Time_window_searcher(start, end, size, points)
###			for win in windows:
###					# Do stuff with the window

class Time_window_searcher(object):
	def __init__(self, time_start, time_end, delta_t, time_window_size, points):
		self.time_start = float(time_start)
		self.time_end = float(time_end)
		self.time_window_size = float(time_window_size)
		self.points = points
		self.delta_t = float(delta_t)

	def __iter__(self):
		###	This doesn't necessarily need to return self, but will for now.
		self.cur_start = self.time_start
		self.cur_end = self.time_start + self.time_window_size
		return self

	def __next__(self):
		###	There's going to be a bug here
		###	This doesn't properly handle the overlap with the end
		if self.cur_end > self.time_end:
			raise StopIteration
		if self.time_end - self.cur_end < self.delta_t and self.time_end - self.cur_end > 0:
			###	This implementation detail is probably best
			print("The time difference to the end time is less than the delta_t! This may cause problems!", self.time_end, self.cur_end, self.time_end - self.cur_end, self.delta_t)

		collection = Collection(find_points_in_time_window(self.cur_start, self.cur_end, self.points), self.cur_start, self.cur_end)
		self.cur_start, self.cur_end = self.cur_start + self.delta_t, self.cur_end + self.delta_t
		return (collection)


###	This will find any points within a time window.
###	This maybe work with rearranging the points in strip function but oh well
###	This takes a start time, an end time, and the array of points.
def find_points_in_time_window(timestart, timeend, points):
	matches = []

	for p in points:
		if (p.MJD >= timestart) and (p.MJD <= timeend):
			matches.append(p)

	return matches

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


def search_multiple_windows(Neutrino_list, Period_list, start_time, end_time, delta_t, window_size_list, p_value, window_density, area):
	least_p_valued_collection = Collection()
	# least_p_valued_collection.p_value *= 100000

	for size in window_size_list:
		print(size)
		collection = window_search_simple(Neutrino_list, Period_list, start_time, end_time,delta_t, size, p_value, window_density, area)
		if (collection.p_value < least_p_valued_collection.p_value):
			print("Success!", collection.p_value, least_p_valued_collection.p_value)
			least_p_valued_collection = collection

	return (least_p_valued_collection)

###	This will return the collection with the lowest p_value
def window_search_simple(Neutrino_list, Period_list, start_time, end_time, delta_t, window_size, p_value, window_density, area):
	matching_collection = Collection()
	# matching_collection.p_value *= (end_time - start_time) / window_size
	for collection in Time_window_searcher(start_time, end_time, delta_t, window_size, Neutrino_list):
		density = len(Neutrino_list) * (collection.end_time - collection.start_time)/(end_time - start_time)
		collection.p_value = summed_poisson_prob_new(len(collection.points), density)
		# collection.p_value = summed_poisson_prob_new(len(collection.points), density) * (end_time - start_time) / window_size
		if (len(collection.points) > 0 and collection.p_value < matching_collection.p_value):
			print("Success for Smaller!", collection.p_value, matching_collection.p_value)
			matching_collection = collection
	return(matching_collection)


###	Deprecated. Needs to be tinkered with slightly if you want to use it
def window_search(Neutrino_list, Period_list, start_time, end_time, delta_t, window_size, p_value):
	###	This will search through all windows. It will test the p_values using the poisson distribution
	###	and return all that are above a certain threshold
	matching_collections = []
	for collection in Time_window_searcher(start_time, end_time, delta_t, window_size, Neutrino_list):
		total_p_value = 1
		for window in event_density_windows(collection[0], Period_list):
			###	Collection[1] is the start time of the collection, window[0].start is the start of this time block
			###	Finding the max wwill find the lower bounds to determine the density
			time_start = max(collection[1], window[0].start)
			time_end = min(collection[2], window[0].end)
			if time_start > time_end or time_end < time_start:
				continue
			window_density = window[0].density * TOTAL_AREA * (time_end - time_start)/(window[0].end - window[0].start)
			p_val = poisson_prob(len(window[1]), window_density)  * (end_time - start_time) / window_size
			collection.p_val = 0

			total_p_value *= p_value_window #### 	I think this is how you can calculate it? Check with someone 
									###		More knowledgable than me.
		if (len(collection[0]) > 0 and total_p_value <= p_value):
			matching_collections.append((collection[0], collection[1],collection[2],total_p_value))
	return(matching_collections)