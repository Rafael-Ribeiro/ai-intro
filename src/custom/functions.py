#!/usr/bin/python

import math

def limit(x, m, M):
	return min(M, max(m, x))

def gaussian(x, med, dev):
	return math.exp(-(x-med)**2/(2*dev**2))
