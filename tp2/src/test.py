#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import config
import random
import time

from population import Population

if len(sys.argv) < 3:
	print "Error: must provide seeds' range"
	sys.exit(0)
else:
	SEEDS = range(int(sys.argv[1]), int(sys.argv[2])+1)

def listsum(a, b)
	for i in xrange(len(a)):
		a[i] += b[i]

def listdiv(a, q)
	for i in xrange(len(a)):
		a[i] /= q

# parameters to be tested
CROSSOVER_PROBS = [0.0, 0.35]										# probabilities
CROSSOVER_POINTS = [2, 5]											# number of points that are cut
ELITISMS = [0.05, 0.20]
POINTS = [15, 30]
POPULATION_SIZES = [25, 50, 100]
REPRESENTATIONS = ["Dynamic spacing", "Even spacing"]
SELECTION_TYPES = ["Tournament","Roulette","Rafael-Ribeiro"]
MUTATION_PROBS = [0.05, 0.25]											# probability (percentage when using Rafael/Ribeiro)
INITIAL_POINTS = [[[0.0,3.0],[4.0,2.0]], [[0.0,3.0],[4.0,2.8]]]

MAX_ITERATIONS = 2000
ITERATIONS = [20, 100, 1000, 2000]

def save_data(path, best, best_list, acg_list, worst_list, stddev_list, iteration_list, t):
	f = open(path + '/data', 'w')
	f.write(str(iteration_list[-1])+"\n")
	f.write(str(best_list)+"\n")
	f.write(str(avg_list)+"\n")
	f.write(str(worst_list)+"\n")
	f.write(str(stddev_list)+"\n")
	f.write(str(best)+"\n")
	f.write(str(t)+"\n")
	f.close()

	"""
	figureBest = figure(figsize=(4.0, 4.0), dpi=72)
	graphBest = figureBest.add_subplot(111)
	graphBest.plot(best[0], best[1], 'r-*')
	figureBest.savefig(path + '/best.png', format="png", transparent=True)

	figureHist = figure(figsize=(10.0, 4.0), dpi=72)
	graphHist = figureHist.add_subplot(111)
	graphHist.plot(iteration_list, best_list, 'b', iteration_list,avg_list, 'g', iteration_list, worst_list, 'r')
	figureHist.savefig(path + '/hist.png', format="png", transparent=True)
	"""

def make_dir(path):
	try:
		os.mkdir(path)
		return True
	except:
		return False	# already exists


if __name__ == '__main__':
	for initial in xrange(len(INITIAL_POINTS)):
		config.A = INITIAL_POINTS[initial][0]
		config.B = INITIAL_POINTS[initial][1]
		config.DX = float(config.B[0] - config.A[0])
		config.DY = float(config.B[1] - config.A[1])

		initial_path = '../results/initial_%d' % (initial,)

		for representation in REPRESENTATIONS:
			config.REPRESENTATION = representation
		
			repr_path = '%s/%s' % (initial_path, representation.split()[0].lower())

			for selection_type in SELECTION_TYPES:
				config.SELECTION_TYPE = selection_type

				selection_types_path = "%s/%s" % (repr_path, selection_type.lower())

				for points in POINTS:
					config.POINTS_INIT = points

					points_path = '%s/%d_points' % (selection_types_path, points)

					for population_size in POPULATION_SIZES:
						config.POPULATION_SIZE = population_size

						population_sizes_path = "%s/%d_pop" %(points_path, population_size)

						for elitism in ELITISMS:
							config.ELITISM = elitism

							elitisms_path = "%s/%.2f_elite" % (population_sizes_path, elitism)

							for crossover_prob in CROSSOVER_PROBS:
								config.CROSSOVER_PROB = crossover_prob

								crossover_prob_path = "%s/%.2f_cross_prob" % (elitisms_path, crossover_prob)

								for crossover_points in CROSSOVER_POINTS:
									config.CROSSOVER_POINTS = crossover_points

									crossover_points_path = "%s/%d_cross_points" % (crossover_prob_path, crossover_points)

									for mutation_prob in MUTATION_PROBS:
										config.MUTATION_PROB = mutation_prob

										mutation_probs_path = "%s/%.2f_mut_prob" % (crossover_points_path, mutation_prob)

										# TODO:
										# render average graphs for each of the population sizes
										# render the best individual for all seeds for the population size
										bests = [-1 for i in xrange(MAX_ITERATIONS)]
										best_val [float("inf") for i in xrange(MAX_ITERATIONS)]

										best_list = [0.0 for i in xrange(MAX_ITERATIONS)]
										avg_list = [0.0 for i in xrange(MAX_ITERATIONS)]
										worst_list = [0.0 for i in xrange(MAX_ITERATIONS)]
										stddev_list = [0.0 for i in xrange(MAX_ITERATIONS)]
										
										for seed in SEEDS:
											seed_path = "%s/%d/%d/data" % (mutation_probs_path, seed, MAX_ITERATIONS)
											
											f = open(seed_path, 'r')
											f.readline() # nr of iterations 

											this_best = eval(f.readline())
											for i in xrange(len(this_best)):
												if this_best[i] > best_val[i]:
													bests[i] = seed
													best_val[i] = this_best[i]

											listsum(best_list, this_best)

											this_avg = eval(f.readline())
											listsum(avg_list, this_avg)

											this_worst = eval(f.readline())
											listsum(worst_list, this_worst)

											this_stddev = eval(f.readline())
											listsum(stddev_list, this_stddev)

											# do not need points for now
											f.close()

										listdiv(best_list, 30.0)
										listdiv(avg_list, 30.0)
										listdiv(worst_list, 30.0)
										listdiv(stddev_list, 30.0)

										for i in ITERATIONS:
											seed_path = "%s/%d/%d/data" % (mutation_probs_path, seed, bests[i-1])
											f = open(seed_path, 'r')
											lines = f.readlines()

											points = eval(lines[5]) # points
											# best_val[i-1] --> fitness
											# plot this

										print "finished graphs: ", mutation_probs_path 
	print "FINISHED!"
