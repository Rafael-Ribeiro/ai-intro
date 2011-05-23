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
		self.individuals.sort(key = Individual.fitness) # guarantee they are sorted for the first iteration

	def evolve(self):
		individuals = [] # next population

		nSurvivingParents = int(config.ELITISM * len(self.individuals))
		nSurvivingParents += nSurvivingParents % 2 # to make sure it's even

		# tournament/roulette selection
		for i in xrange((len(self.individuals) - nSurvivingParents) / 2):
			if config.SELECTION_TYPE == "Tournament": # "Tournament"
				individual1, individual2 = self.tournament(config.TOURNAMENT_SIZE)
			else: # "Roulette"
				individual1, individual2 = self.roulette()

			# they are always copies (even if no crossover occurs)
			individual1 = copy.deepcopy(self.individuals[i*2])
			individual2 = copy.deepcopy(self.individuals[(i*2)+1])

			# reproduce (with/without cross-over)
			prob = random.random()
			if prob <= config.CROSSOVER: # crossover both individuals (else: clone them)
				individual1.crossover(individual2)

			individuals.append(individual1)
			individuals.append(individual2)

		# mutate all childs (config.MUTATION_PROB applies to every gene)
		for individual in individuals:
			individual.mutate()

		 # Elitism (config.ELITISM refers to the parents' percentage that survives);
		 # len(individuals) guarantees that POPULATION_MAX is not exceeded, since we only generate the "remaining" childs after elitism
		self.individuals = self.individuals[:nSurvivingParents] + individuals
		self.individuals.sort(key = Individual.fitness) # guarantee that self.individuals are sorted for the next iteration
		
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
