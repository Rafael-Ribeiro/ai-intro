#!/usr/bin/python

path = "/home/jprafael/dei/3o Ano/IIA/projects/tp2/results/initial_0/even/rafael-ribeiro/15_points/100_pop/0.20_elite/0.00_cross_prob/2_cross_points/0.25_mut_prob/"
fitness = 1.2216529

for i in xrange(1,31):
	f = open(path + str(i) + "/2000/data", 'r')
	fit = eval(f.readlines()[1].rstrip())[-1]

	if fit == fitness:
		print i
