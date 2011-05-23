#!/usr/bin/python
# -*- coding: utf-8 -*-

DEBUG_MODE = False				# console prints

A = [0.0, 3.0] 					# initial point
B = [1.0, 2.0]					# end point

DX = float(B[0] - A[0])
DY = float(B[1] - A[1])

DX_MIN = 0.0001
DY_MIN = DX_MIN

POPULATION_MAX = 100			# size of population, must be pair
SELECTION_TYPE = "Tournament" 	# "Roulette"

POINTS_INIT = 30				# max number of points per individual
ELITISM = 0.1					# percentage

CROSSOVER = 0.05				# probability
CROSSOVER_LEN_MAX = 0.25		# 1 quarter of the individual is cut

MUTATION_BURST = 0.50			# probability
MUTATION = 0.1					# percentage
MUTATION_PROB = 0.10			# probability
MUTATION_Y = 0.2				# percentage of Y mutation
