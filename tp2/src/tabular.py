#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import time
from math import *
from matplotlib.pyplot import figure

SEEDS = range(1,31)

def listsum(a, b):
	for i in xrange(len(a)):
		a[i] += b[i]

def listdiv(a, q):
	for i in xrange(len(a)):
		a[i] /= q

# parameters to be tested
CROSSOVER_PROBS = [0.0, 0.35]										# probabilities
CROSSOVER_POINTS = [2, 5]											# number of points that are cut
ELITISMS = [0.05, 0.20]
POINTS = [15, 30]
POPULATION_SIZES = [25, 50, 100]
REPRESENTATIONS = ["Dynamic spacing", "Even spacing"]
REPRESENTATIONS_DIC = {"Dynamic spacing" : "Dynamic", "Even spacing" : "Even"}
SELECTION_TYPES = ["Tournament","Roulette","Rafael-Ribeiro"]
MUTATION_PROBS = [0.05, 0.25]											# probability (percentage when using Rafael/Ribeiro)
INITIAL_POINTS = [[[0.0,3.0],[4.0,2.0]], [[0.0,3.0],[4.0,2.8]]]

MAX_ITERATIONS = 2000
ITERATIONS = [20, 100, 1000, 2000]

if __name__ == '__main__':
	for initial in xrange(len(INITIAL_POINTS)):
		initial_path = '../results/initial_%d' % (initial,)

		for representation in REPRESENTATIONS:
			repr_path = '%s/%s' % (initial_path, representation.split()[0].lower())

			for selection_type in SELECTION_TYPES:
				selection_types_path = "%s/%s" % (repr_path, selection_type.lower())

				for points in POINTS:
					points_path = '%s/%d_points' % (selection_types_path, points)

					for population_size in POPULATION_SIZES:
						population_sizes_path = "%s/%d_pop" %(points_path, population_size)

						for elitism in ELITISMS:
							elitisms_path = "%s/%.2f_elite" % (population_sizes_path, elitism)

							for crossover_prob in CROSSOVER_PROBS:
								crossover_prob_path = "%s/%.2f_cross_prob" % (elitisms_path, crossover_prob)

								for crossover_points in CROSSOVER_POINTS:
									crossover_points_path = "%s/%d_cross_points" % (crossover_prob_path, crossover_points)

									for mutation_prob in MUTATION_PROBS:
										mutation_probs_path = "%s/%.2f_mut_prob" % (crossover_points_path, mutation_prob)

										# TODO:
										# render average graphs for each of the population sizes
										# render the best individual for all seeds for the population size
										bests = [-1 for i in xrange(MAX_ITERATIONS)]
										best_val = [float("inf") for i in xrange(MAX_ITERATIONS)]

										total_best = [[0.0 for i in SEEDS] for j in ITERATIONS]
										best_list = [0.0 for i in xrange(MAX_ITERATIONS)]
										avg_list = [0.0 for i in xrange(MAX_ITERATIONS)]
										worst_list = [0.0 for i in xrange(MAX_ITERATIONS)]
										stddev_list = [0.0 for i in xrange(MAX_ITERATIONS)]
										
										for seed in SEEDS:
											seed_path = "%s/%d/%d/data" % (mutation_probs_path, seed, MAX_ITERATIONS)

											f = open(seed_path, 'r')
											f.readline() # nr of iterations 

											this_best = eval(f.readline().rstrip())
											for i in xrange(len(this_best)):
												if this_best[i] < best_val[i]:
													bests[i] = seed
													best_val[i] = this_best[i]

											listsum(best_list, this_best)

											for i in xrange(len(ITERATIONS)):
												total_best[i][seed-1] = this_best[ITERATIONS[i]-1]

											this_avg = eval(f.readline().rstrip())
											listsum(avg_list, this_avg)

											this_worst = eval(f.readline().rstrip())
											listsum(worst_list, this_worst)

											this_stddev = eval(f.readline().rstrip())
											listsum(stddev_list, this_stddev)

											# do not need points for now
											f.close()

										listdiv(best_list, 30.0)
										listdiv(avg_list, 30.0)
										listdiv(worst_list, 30.0)
										listdiv(stddev_list, 30.0)

										for i in xrange(len(ITERATIONS)):
											seed_path = "%s/%d/%d/data" % (mutation_probs_path, bests[ITERATIONS[i]-1], ITERATIONS[i])
											f = open(seed_path, 'r')
											lines = map(lambda x: x.rstrip(), f.readlines())

											total_best_avg = 0.0
											for x in xrange(len(SEEDS)):
												total_best_avg += total_best[i][x]
											total_best_avg /= len(SEEDS)

											sum_total_diffs = 0.0
											for x in xrange(len(SEEDS)):
												sum_total_diffs += (total_best[i][x]-total_best_avg)**2
											total_best_std = sqrt(sum_total_diffs/len(SEEDS))

										print "\t\t%d\t&\t%s\t&\t%s\t&\t%d\t&\t%d\t&\t%.2f\t&\t%.2f\t&\t%d\t&\t%.2f\t&\t%.7f\t&\t%.7f\t&\t%.7f\t&\t%.7f\t&\t%.7f\t&\t%.7f\t&\t%.7f\t&\t%.7f \\\\\n\t\t\\hline" % (initial + 1,REPRESENTATIONS_DIC[representation],selection_type,points,population_size,elitism*100,crossover_prob*100,crossover_points,mutation_prob*100,best_list[19],best_list[99],best_list[999],best_list[1999],avg_list[1999],worst_list[1999],stddev_list[1999],total_best_std*100)

										#print "finished graphs: ", mutation_probs_path 
	#print "FINISHED!"
