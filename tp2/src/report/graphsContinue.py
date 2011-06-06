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
CROSSOVER_PROBS = [0.0]										# probabilities
CROSSOVER_POINTS = [2]											# number of points that are cut
ELITISMS = [0.20]
POINTS = [15, 30]
POPULATION_SIZES = [100]
REPRESENTATIONS = ["Even spacing"]
REPRESENTATIONS_DIC = {"Dynamic spacing" : "Dynamic", "Even spacing" : "Even"}
SELECTION_TYPES = ["Roulette"]
MUTATION_PROBS = [0.05,]											# probability (percentage when using Rafael/Ribeiro)
INITIAL_POINTS = [[[0.0,3.0],[4.0,2.0]]]

MAX_ITERATIONS = 2000
ITERATIONS = [20, 100, 1000, 2000]

if __name__ == '__main__':
	for initial in xrange(len(INITIAL_POINTS)):
		initial_path = '../../results/initial_%d' % (initial,)

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

									if crossover_prob == 0.0 and crossover_points != CROSSOVER_POINTS[0]:
										continue

									for mutation_prob in MUTATION_PROBS:
										mutation_probs_path = "%s/%.2f_mut_prob" % (crossover_points_path, mutation_prob)

										if os.path.isfile(mutation_probs_path + "/.doneGraphsContinue"):
											continue

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
											seed_path = "%s/%d_continue/%d/data" % (mutation_probs_path, seed, MAX_ITERATIONS)
											
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
											seed_path = "%s/%d_continue/%d/data" % (mutation_probs_path, bests[ITERATIONS[i]-1], ITERATIONS[i])
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

											_points = eval(lines[5]) # points
											# best_val[i-1] --> fitness
											# plot this
											iteration_list = [a for a in xrange(1, ITERATIONS[i]+1)]
											figureHist = figure(figsize=(12.0, 6.0), dpi=72)
											graphHist = figureHist.add_subplot(111)
											graphHist.plot(iteration_list, best_list[:ITERATIONS[i]], 'b', iteration_list, avg_list[:ITERATIONS[i]], 'g', iteration_list, worst_list[:ITERATIONS[i]], 'r') # TODO: stddev -> candlesticks
											graphHist.legend( ('Best fitness', 'Average fitness', 'Worst fitness'), loc='upper right')
											figureHist.savefig('%s/hist_%d_continue.png' % (mutation_probs_path, ITERATIONS[i]), format="png", transparent=True)
											figureHist.clf()

											figureBest = figure(figsize=(8.0, 8.0), dpi=72)
											graphBest = figureBest.add_subplot(111)
											graphBest.plot(_points[0], _points[1], 'r-*')
											graphBest.text(0.5, 0.9, 'Fitness stddev (x100) %.3f' % (total_best_std*100, ), fontsize=18, horizontalalignment='center', verticalalignment='center', transform = graphBest.transAxes)

											figureBest.savefig('%s/best_%d_continue.png' % (mutation_probs_path, ITERATIONS[i]) , format="png", transparent=True)
											figureBest.clf()

										cr_points = str(crossover_points) if crossover_prob != 0.0 else "NA"

										data = open(mutation_probs_path + "/data_continue", 'w')
										data.write(str(best_list) + "\n" + str(avg_list) + "\n" + str(worst_list)+"\n")
										data.flush()
										data.close()

										open(mutation_probs_path + "/.doneGraphsContinue", 'w').close()

										print "finished graphs and tabular: ", mutation_probs_path 

	print "FINISHED!"
