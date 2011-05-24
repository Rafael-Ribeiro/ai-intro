#!/usr/bin/python
# -*- coding: utf-8 -*-

DEBUG_MODE = False					# console prints

A = [0.0, 3.0] 						# initial point
B = [4.0, 2.0]						# end point

DX = float(B[0] - A[0])
DY = float(B[1] - A[1])

DX_MIN = 0.0001
DY_MIN = DX_MIN

POPULATION_SIZE = 100				# size of population, must be pair
SELECTION_TYPE = "Tournament"	 	# "Roulette"

REPRESENTATION = "Even spacing"		# "Dynamic spacing"
TOURNAMENT_SIZE = 5					# Tournament size (absolute value)

POINTS_INIT = 15					# max number of points per individual
ELITISM = 0.15						# percentage

CROSSOVER_PROB = 0.40				# probability
CROSSOVER_POINTS = 1				# 40% of the individual is cut

MUTATION_BURST = 0.0				# probability
MUTATION_PROB = 0.15				# probability
MUTATION_X_STDEV = (A[0] - B[0])/10	# standard deviation
MUTATION_Y_STDEV = (A[1] - B[1])/10	# standard deviation
