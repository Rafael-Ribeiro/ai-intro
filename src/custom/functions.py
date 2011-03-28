#!/usr/bin/python

import math

def limit(x, m, M):
	return min(M, max(m, x))

def cut(x, m, v, M, V):
	if x < m:
		return v
	if x > M:
		return V
	return x

def greater(a, b, T, F):
	if a > b:
		return T
	return F

def gaussian(x, med, dev):
	return math.exp(-(x-med)**2/(2*dev**2))
