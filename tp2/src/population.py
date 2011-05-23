#!/usr/bin/python
# -*- coding: utf-8 -*-

import math, random, copy, sys
import config
from individuals import *

class Population:
	@staticmethod
	def new(nIndividuals, representation):
		if representation == "Even spacing":
			individuals = [EvenSpacing.new(config.POINTS_INIT) for i in xrange(nIndividuals)]
		else:
			individuals = [DynamicSpacing.new(config.POINTS_INIT) for i in xrange(nIndividuals)]

		return Population(individuals)

	def __init__(self, individuals):
		self.individuals = individuals

	def evolve(self):
		individuals = [] # next population

		# reproduce (with cross-over)
		random.shuffle(self.individuals)
		for i in xrange(len(self.individuals)/2):
			individual1 = copy.deepcopy(self.individuals[i*2])
			individual2 = copy.deepcopy(self.individuals[(i*2)+1])

			prob = random.random()
			if prob <= config.CROSSOVER: # crossover both individuals (else: clone them)
				crossoverMaxLen = random.random() * config.CROSSOVER_LEN_MAX * config.DX

				startingCrossoverPoint = random.random() * (config.DX - crossoverMaxLen)
				endingCrossoverPoint = startingCrossoverPoint + crossoverMaxLen

				individual1.crossover(individual2, startingCrossoverPoint, endingCrossoverPoint)

			individuals.append(individual1)
			individuals.append(individual2)

		if len(self.individuals) % 2 != 0: # forever alone: survives without change
			individuals.push(copy.deepcopy(self.individuals[-1]))

		# mutate childs
		for individual in individuals:
			#if random.random() <= MUTATION_PROB:
			individual.mutate()

		# join parents and childs
		individuals += self.individuals
		individuals.sort(key = Individual.fitness)

		# elitism selection
		cutoff = int(config.ELITISM * len(individuals))

		self.individuals = individuals[:cutoff]
		individuals = individuals[cutoff:]

		# tournament/roulette selection

		self.individuals += individuals[len(self.individuals):config.POPULATION_MAX] # TODO: its here just while there is no selection
		
	def getBest(self):
		return self.individuals[0]

	def getStatistics(self):
		max_fitness = self.individuals[0].fitness()
		min_fitness = self.individuals[-1].fitness()

		avg_fitness = 0.0
		for i in self.individuals:
			avg_fitness += i.fitness()
		avg_fitness /= config.POPULATION_MAX

		sqr_sum = 0.0
		for i in self.individuals:
			sqr_sum += (i.fitness() - avg_fitness)**2

		dev_fitness = math.sqrt(sqr_sum/config.POPULATION_MAX)
		return max_fitness, avg_fitness, min_fitness, dev_fitness
