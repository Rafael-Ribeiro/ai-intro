#!/usr/bin/python
# -*- coding: utf-8 -*- 

ITERATIONS = 1000		# number of iterations

POINTS_MAX = 500		# max number of points per individual
ELITISM = 0.1			# percentage
CROSSOVER = 0.05		# probability
CROSSOVER_MAX = 0.25	# 1 quarter of the individual is cut
MUTATION_X = 0.01		# probability
MUTATION_Y = 0.01		# probability

SELECTION_TYPE = "TOURNAMENT" # "ROULETTE"
POPULATION_MAX = 500	# size of population, must be pair

class Individual:
	def new(npoints, A, B):
		
		dx = float(B[0] - A[0])
		dy = float(B[1] - A[1])
		
		# TODO: GENERATE A RANDOM (VALID) INDIVIDUAL
		return Individual([[dx/npoints, A[1]+i*dy/npoints] for i in xrange(npoints)])

	# List of n points (2 sized arrays)
	#	with dx
	#	and absolute y
	def __init__(self, points):
		self.points = points

	def mutate(self):

	def cross(self, other):

	def fitness(self):

	def plot(self):
	
class Population:
	def new(nindividuals):
	
	def __init__(self, individuals):
		self.individuals = individuals

	def evolve(self):
		# reproduce (with cross-over)

		# mutate childs

		# elitism selection

		# tournament/roulette selection

		self.individuals = individuals

	def getStatistics(self)

		#return max, maxindividual, med, min, avg, dev

	def save(self, fileout):
		pass

if __name__ == '__main__':
	gtk()
