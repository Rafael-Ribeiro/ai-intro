#!/usr/bin/python

def apply_filter(item, f):
	for i in xrange(len(f)):
		if f[i] != None and f[i] != item[i]:
			return False

	return True

def sum_col(data, col):
	return sum(map(lambda x: x[col], data))

def avg_col(data, col):
	return sum_col(data, col) / len(data)

def max_col(data, col):
	return max(map(lambda x: x[col], data))

def min_col(data, col):
	return min(map(lambda x: x[col], data))

items = [
	"Best (20)",
	"Best (100)", 

	"Best (1000)",
	"Best (2000)",
	"Average (2000)",
	"Worst (2000)",
	"Std. Dev. (2000, Pop.)",
	"Std. Dev. x100 (2000, 30 runs)"
]

if __name__ == '__main__':
	f = open('data.py', 'r')
	data = eval(f.read())
	f.close()

	filters = [
		2,		# point
		"Dynamic",	# representation
		"Rafael-Ribeiro",	# selection
		None,	# individual size
		None,	# population size
		None,	# elitism
		None,	# crossover
		None,	# crossover points
		None	# mutation size
	]
	data = filter(lambda x: apply_filter(x, filters), data)

	print str(filters)+"\n"
	for i in xrange(4): # len(items)
		col = i + 9

		#print "%s: max: %.7f avg: %.7f min: %.7f" % (items[i], max_col(data, col), avg_col(data, col), min_col(data, col))
		print "%.7f" % (avg_col(data, col))
