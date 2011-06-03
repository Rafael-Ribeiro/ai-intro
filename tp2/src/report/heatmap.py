#!/usr/bin/python

import itertools

filters = [
	[1, 2],											# point
	["Even", "Dynamic"],							# representation
	["Tournament", "Roulette", "Rafael-Ribeiro"],	# selection
	[15, 30],										# individual size
	[25, 50, 100],									# population size
	[5.0, 20.0], 									# elitism
	[0.0, 35.0],									# crossover
	[2, 5],											# crossover points
	[5, 25]											# mutation prob
]

pre_filter = [
	None,											# point
	None,											# representation
	None,											# selection
	None,											# individual size
	None,											# population size
	None, 											# elitism
	None,											# crossover
	None,											# crossover points
	None											# mutation prob
]

dimensions = [
	0,
	1,
	2,
	3,
	4,
	5,
	6,
	7,
	8
]

def apply_filter(item, curfilters):
	for i in xrange(len(curfilters)):
		if curfilters[i] != None and curfilters[i] != item[i]:
			return False

	return True

def plot(data, dimension):
	if dimension == 8:join
		if len(data) == 0:
			return (255, 255, 255)
		else
			return heat(data[0])

	datas = [plot(filter(lambda x: data[dimensions[dimension]] == val, data)) for val in filters[dimensions[dimension]]]

	if dimension % 2 == 0:
		return datas

	points = [[] for i in xrange(len(data))]
		

	return points


if __name__ == '__main__':
	f = open('data.py', 'r')
	data = eval(f.read())
	f.close()

	data = filter(lambda x: apply_filter(data, pre_filter) , data)

	for i in xrange(len(items)):
		col = i + 9

		print "%s: max: %.7f avg: %.7f min: %.7f" % (items[i], max_col(data, col), avg_col(data, col), min_col(data, col))
