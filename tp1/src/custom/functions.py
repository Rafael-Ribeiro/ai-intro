#!/usr/bin/python

import math

def limit(x, m, M):
	return min(M, max(m, x))

def cut(x, *args):
	for i in xrange(len(args)/2):
		if x < args[i*2+1]:
			try:
				return args[i*2](x)	
			except TypeError:
				return args[i*2]
			
	try:
		return args[-1](x)
	except TypeError:
		return args[-1]

def greater(a, b, T, F):
	if a > b:
		return T
	return F

def gaussian(x, med, dev):
	x = min(x,10000)
	return math.exp(-(x-med)**2/(2*dev**2))

def hiperbole(x):
	return math.sqrt(1.0+x*x)

def negexp(x, lamb):
	return lamb*math.exp(-lamb*x)
	

