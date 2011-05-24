#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import config
import random

from population import Population
from matplotlib.pyplot import figure

if len(sys.argv) < 3:
	print "Error: must provide seeds' range"
	sys.exit(0)
else:
	SEEDS = range(int(sys.argv[1]), int(sys.argv[2])+1)

# parameters to be tested
CROSSOVER_PROBS = [0.40]									# probabilities
CROSSOVER_LEN_MAXS = [0.40]									# % of the individual is cut
ELITISMS = [0.15]
POINTS = [15, 30]
POPULATION_SIZES = [100]
REPRESENTATIONS = ["Dynamic spacing", "Even spacing"]
SELECTION_TYPES = ["Tournament","Roulette","Rafael-Ribeiro"]
MUTATION_PROBS = [0.15]										# probability (percentage when using Rafael/Ribeiro)

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


if __name__ == '__main__':
	for representation in REPRESENTATIONS:
		config.REPRESENTATION = representation
		
		repr_path = '../results/{0}'.format(representation.split()[0].lower())
		make_dir(repr_path)
		if os.path.isfile(repr_path + "/.done"):
			continue

		for selection_type in SELECTION_TYPES:
			config.SELECTION_TYPE = selection_type

			selection_types_path = "{0}/{1}".format(repr_path, selection_type.lower())
			make_dir(selection_types_path)
			if os.path.isfile(selection_types_path + "/.done"):
				continue

			for points in POINTS:
				config.POINTS_INIT = points

				points_path = '{0}/{1}_points'.format(selection_types_path, points)
				make_dir(points_path)
				if os.path.isfile(points_path + "/.done"):
					continue

				for population_size in POPULATION_SIZES:
					config.POPULATION_SIZE = population_size

					population_sizes_path = "{0}/{1}_pop".format(points_path, population_size)
					make_dir(population_sizes_path)
					if os.path.isfile(population_sizes_path + "/.done"):
						continue

					for elitism in ELITISMS:
						config.ELITISM = elitism

						elitisms_path = "{0}/{1}_elite".format(population_sizes_path, elitism)
						make_dir(elitisms_path)
						if os.path.isfile(elitisms_path + "/.done"):
							continue

						for crossover_prob in CROSSOVER_PROBS:
							config.CROSSOVER_PROB = crossover_prob

							crossover_prob_path = "{0}/{1}_cross_prob".format(elitisms_path, crossover_prob)
							make_dir(crossover_prob_path)
							if os.path.isfile(crossover_prob_path + "/.done"):
								continue

							for crossover_len_max in CROSSOVER_LEN_MAXS:
								config.CROSSOVER_LEN_MAX = crossover_len_max

								crossover_len_maxs_path = "{0}/{1}_cross_max_len".format(crossover_prob_path, crossover_len_max)
								make_dir(crossover_len_maxs_path)
								if os.path.isfile(crossover_len_maxs_path + "/.done"):
									continue

								for mutation_prob in MUTATION_PROBS:
									config.MUTATION_PROB = mutation_prob

									mutation_probs_path = "{0}/{1}_mut_prob".format(crossover_len_maxs_path, mutation_prob)
									make_dir(mutation_probs_path)
									if os.path.isfile(mutation_probs_path + "/.done"):
										continue

									for seed in SEEDS:
										random.seed(seed)

										seed_path = "{0}/{1}".format(mutation_probs_path, seed)
										make_dir(seed_path)
										if os.path.isfile(seed_path + "/.done"):
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
									open(mutation_probs_path + "/.done", 'w').close()
								open(crossover_len_maxs_path + "/.done", 'w').close()
							open(crossover_prob_path + "/.done", 'w').close()
						open(elitisms_path + "/.done", 'w').close()
					open(population_sizes_path + "/.done", 'w').close()
				open(points_path + "/.done", 'w').close()
			open(selection_types_path + "/.done", 'w').close()
		open(repr_path + "/.done", 'w').close()

	print "FINISHED!"
