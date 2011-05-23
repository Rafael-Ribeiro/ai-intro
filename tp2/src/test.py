#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import config
import random

from population import Population
from matplotlib.pyplot import figure

SEEDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

if len(sys.argv) < 3:
	return 0
else
	SEEDS = range(int(sys.argv[1]), int(sys.argv[2])+1)

POINTS = [15, 30]
REPRESENTATIONS = ["Dynamic spacing", "Even spacing"]

MAX_ITERATIONS = 2000
ITERATIONS = [20, 100, 1000, 2000]

def save_data(path, best, best_list, acg_list, worst_list, stddev_list, iteration_list):
	f = open(path + '/data', 'w')
	f.write(str(iteration_list[-1])+"\n")
	f.write(str(best_list)+"\n")
	f.write(str(avg_list)+"\n")
	f.write(str(worst_list)+"\n")
	f.write(str(stddev_list)+"\n")
	f.write(str(best)+"\n")
	f.close()

	figureBest = figure(figsize=(4.0, 4.0), dpi=72)
	graphBest = figureBest.add_subplot(111)
	graphBest.plot(best[0], best[1], 'r-*')
	figureBest.savefig(path + '/best.png', format="png", transparent=True)

	figureHist = figure(figsize=(10.0, 4.0), dpi=72)
	graphHist = figureHist.add_subplot(111)
	graphHist.plot(iteration_list, best_list, 'b', iteration_list,avg_list, 'g', iteration_list, worst_list, 'r')
	figureHist.savefig(path + '/hist.png', format="png", transparent=True)

def make_dir(path):
	try:
		os.mkdir(path)
		return True
	except:
		return False	# already exists
		
for representation in REPRESENTATIONS:
	config.REPRESENTATION = representation
	
	repr_path = '../results/{0}'.format(representation.split()[0].lower())
	make_dir(repr_path)
	if os.path.isfile(repr_path + "/.done"):
		continue

	for points in POINTS:
		config.POINTS_INIT = points
		points_path = '{0}/{1}_points'.format(repr_path, points)

		make_dir(points_path)
		if os.path.isfile(points_path + "/.done"):
			continue

		for seed in SEEDS:
			random.seed(seed)

			seed_path = "{0}/{1}".format(points_path, seed)
			make_dir(seed_path)
			if os.path.isfile(points_path + "/.done"):
				continue

			best_list = []
			avg_list = []
			worst_list = []
			stddev_list = []

			population = Population.new(config.POPULATION_SIZE, config.REPRESENTATION)
			for i in xrange(1, MAX_ITERATIONS+1):
				population.evolve()

				stats = population.getStatistics()

				best_list.append(stats[0])
				avg_list.append(stats[1])
				worst_list.append(stats[2])
				stddev_list.append(stats[3])
	
				if i in ITERATIONS:
					final_path = "{0}/{1}".format(seed_path, i)
					best = population.getBest().getPoints()

					make_dir(final_path)
					save_data(final_path, best, best_list, avg_list, worst_list, stddev_list, xrange(1, i+1))

			print "finished test: ", seed_path

			open(seed_path + "/.done", 'w').close()
		open(points_path + "/.done", 'w').close()
	open(repr_path + "/.done", 'w').close()

print "FINISHED!"
