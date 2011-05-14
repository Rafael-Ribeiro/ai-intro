#!/usr/bin/python
# -*- coding: utf-8 -*-

import math, random, copy

DEBUG_MODE = True				# console prints

A = [0.0, 3.0] # initial point
B = [1.0, 2.0] # end point

dx = float(B[0] - A[0])
dy = float(B[1] - A[1])

POPULATION_MAX = 500			# size of population, must be pair
SELECTION_TYPE = "TOURNAMENT" 	# "ROULETTE"

POINTS_INIT = 500				# max number of points per individual
ELITISM = 0.1					# percentage

CROSSOVER = 0.05				# probability
CROSSOVER_LEN_MAX = 0.25		# 1 quarter of the individual is cut

MUTATION_BURST = 0.50			# probability
MUTATION_X = 0.01				# probability
MUTATION_Y = 0.01				# probability


# physical constants
G_ACC = 9.80655

class Individual:
	def new(nPoints):
		return Individual([[dx/nPoints, (random.random() - 0.5) * 2 * dy + B[1]] for i in xrange(nPoints)])

	# List of n points (2 sized arrays: [dx, abs y])
	def __init__(self, points):
		self.points = points

	def mutate(self):
		pass

	def cross(self, other):
		pass

	def fitness(self):
		x_i = self.points[0][0]
		y_i = maxHeight = self.points[0][1]
		v_i = time = 0
		
		#It has to have at least 2 points, otherwise it is not doable
		if(len(self.points) < 2):
			return -1;
		
		for i in range(1, len(self.points)):
			#Consistency checking. This wasn't done in a separate function for quickness
			if self.points[i][0] <= x_i:
				return -1

			if self.points[i][1] > maxHeight or (self.points[i][1] == maxHeight and i != len(self.points)):
				return -1
			
			#Calculate acceleration based on segment slope. Open question - would be using cos() faster?
			#Since the angle had to be calculated beforehand, I don't think so
			dx = self.points[i][0] - x_i
			dy = self.points[i][1] - y_i
			li = math.sqrt(dx*dx + dy*dy)
			ai = -G_ACC*dy/float(li)
			
			#Energy conservation. You really needn't be reading this, but if you have doubts, tell me
			v_j = math.sqrt(2*(-G_ACC*dy + v_i*v_i/2))
			#If speed is less than 0, forget about it. This actually never happens thanks to our checks.
			#But you never know what magic lies in wait...
			if v_j < 0.0:
				return -1

			dv = v_j - v_i
			
			#The speed variation over the acceleration gives us the time. Voila
			time += dv/ai
			
			#Debugging, ignore
			if DEBUG_MODE:
				print "Segment " + str(i/2)
				print "dX: " + str(dx) + " dY: " + str(dy)
				print "Distance Travelled: " + str(li)
				print "Gained velocity: " + str(dv)
				print "Acceleration: " + str(ai)
				print "Time to travel: " + str(dv/ai) +"\n"
			
			#Update the positions and current speed
			v_i = v_j
			x_i = self.points[i][0]
			y_i = self.points[i][1]
		
		return time

	def _findXCoord(self, x):
		pass

	def _splitXCoord(self, x):
		pass

	def crossoverSegment(self, x, crossoverLen):
		pass # return a (i,j) tuple
	
class Population:
	def new(nIndividuals):
		individuals = [Individual.new(POINTS_INIT, A, B) for i in xrange(nIndividuals)]

		return Population(individuals)

	def __init__(self, individuals):
		self.individuals = individuals

	def evolve(self):
		individuals = [] # next population

		# reproduce (with cross-over)
		random.shuffle(self.individuals)
		for i in xrange(len(self.individuals)/2):
			individual1 = self.individuals[i*2]
			individual2 = self.individuals[(i*2)+1]

			prob = random.random()
			if prob <= CROSSOVER: # crossover
				crossoverMaxLen = random.random() * CROSSOVER_LEN_MAX * dx

				startingCrossoverPoint = random.random() * (dx - crossoverMaxLen)
				
			else: # individuals cloned
				individuals.push(copy.deepcopy(individual1))
				individuals.push(copy.deepcopy(individual2))

		if len(self.individuals) % 2 != 0: # forever alone: survives without change
			individuals.push(copy.deepcopy(self.individuals[-1]))

		# mutate childs

		# join parents and childs
		individuals += self.individuals

		# elitism selection

		# tournament/roulette selection

		self.individuals = individuals


	def getStatistics(self):
		pass
		#return max, maxindividual, med, min, avg, dev

	def save(self, fileout):
		pass
