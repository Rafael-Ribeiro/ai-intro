#!/usr/bin/python
# -*- coding: utf-8 -*-

import math, random, copy

DEBUG_MODE = False				# console prints

A = [0.0, 3.0] # initial point
B = [1.0, 2.0] # end point

DX = float(B[0] - A[0])
DY = float(B[1] - A[1])

DX_MIN = 0.0001
DY_MIN = DX_MIN

POPULATION_MAX = 500			# size of population, must be pair
SELECTION_TYPE = "Tournament" 	# "Roulette"

POINTS_INIT = 100				# max number of points per individual
ELITISM = 0.1					# percentage

CROSSOVER = 0.05				# probability
CROSSOVER_LEN_MAX = 0.25		# 1 quarter of the individual is cut

MUTATION_BURST = 0.50			# probability
MUTATION = 0.01					# probability
MUTATION_Y = 0.20				# percentage of Y mutation

# physical constants
G_ACC = 9.80655

class Individual:
	@staticmethod
	def new(nPoints):
		individuals = [[DX/(nPoints-1), 0.0] for i in xrange(nPoints - 2)] + [[DX/(nPoints-1), B[1]]]

		individuals[0][1] = min(A[1] + (random.random() - 0.5) * 2 * DY/nPoints,A[1] - DY_MIN)
		for i in xrange(1,nPoints - 1):
			individuals[i][1] = min(individuals[i-1][1] + (random.random() - 0.5) * 2 * DY/nPoints,A[1] - DY_MIN)

		return Individual(individuals)

	# List of n points (2 sized arrays: [dx, abs y])
	def __init__(self, points):
		self.points = points
		self.fitness_val = None

	def _findXCoord(self, x): # returns a tuple (index, splitNeeded)
		x_acc = 0.0

		for i in xrange(len(self.points)):
			x_acc += self.points[i][0]

			if x_acc > x:
				return i, x_acc == x

		return len(self.points) - 1, False

	def _splitXCoord(self, x):
		xIndex, splitNeeded = self._findXCoord(x)

		if not splitNeeded:
			return xIndex

		# TODO

	def crossover(self, other, xInit, xEnd):
		self.fitness_val = None
		other.fitness_val = None
		pass
	
	def crossoverSegment(self, xInit, xEnd):
		pass # return a (i,j) tuple

	def fitness(self):
		if self.fitness_val:
			return self.fitness_val

		y_i = maxHeight = A[1]
		v_i = time = 0.0
		
		#It has to have at least 2 points, otherwise it is not doable
		if len(self.points) < 2:
			return -1;
		
		for i in range(1, len(self.points)):
			if self.points[i][1] > maxHeight or (self.points[i][1] == maxHeight and i != len(self.points)):
				print "c", i, maxHeight, self.points[i][1]
				return -1
			
			#Calculate acceleration based on segment slope. Open question - would be using cos() faster?
			#Since the angle had to be calculated beforehand, I don't think so
			dx = self.points[i][0]
			dy = self.points[i][1] - y_i
			li = math.sqrt(dx*dx + dy*dy)
			ai = -G_ACC*dy/float(li)
			
			#Energy conservation. You really needn't be reading this, but if you have doubts, tell me
			v_j = math.sqrt(2*(-G_ACC*dy + v_i*v_i/2))
			#If speed is less than 0, forget about it. This actually never happens thanks to our checks.
			#But you never know what magic lies in wait...

			if v_j < 0.0:
				sys.exit(-1)
				return -1

			dv = v_j - v_i
			
			#The speed variation over the acceleration gives us the time. Voila
			time += dv/ai if ai != 0 else v_j*li

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
		
		self.fitness_val = time
		return time

	def getPlotData(self):
		x = [A[0]]
		y = [A[1]]

		for i in self.points:
			x.append(x[-1]+i[0])
			y.append(i[1])
		return x, y

	def mutate(self):
		# TODO Bursts
		mutations = random.sample(range(len(self.points)-1), int(MUTATION * len(self.points) - 1))
		for mutIndex in mutations:
			dx = self.points[mutIndex][0] + self.points[mutIndex + 1][0]
			randX = random.random() * (dx - 2 * DX_MIN) + DX_MIN
			self.points[mutIndex][0] = randX
			self.points[mutIndex+1][0] = dx - randX
			self.points[mutIndex][1] += (random.random() - 0.5) * 2 * MUTATION_Y * DY
			self.points[mutIndex][1] = min(self.points[mutIndex][1],A[1] - DY_MIN)

			if self.points[mutIndex][1] == self.points[mutIndex+1][1]:
				self.points[mutIndex][1] -= DY_MIN

		self.fitness_val = None

class Population:
	@staticmethod
	def new(nIndividuals):
		individuals = [Individual.new(POINTS_INIT) for i in xrange(nIndividuals)]

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
			if prob <= CROSSOVER: # crossover both individuals (else: clone them)
				crossoverMaxLen = random.random() * CROSSOVER_LEN_MAX * DX

				startingCrossoverPoint = random.random() * (DX - crossoverMaxLen)
				endingCrossoverPoint = startingCrossoverPoint + crossoverMaxLen

				individual1.crossover(individual2, startingCrossoverPoint, endingCrossoverPoint)

			individuals.append(individual1)
			individuals.append(individual2)

		if len(self.individuals) % 2 != 0: # forever alone: survives without change
			individuals.push(copy.deepcopy(self.individuals[-1]))

		# mutate childs
		for individual in individuals:
			individual.mutate()

		# join parents and childs
		individuals += self.individuals
		individuals.sort(key = Individual.fitness)

		# elitism selection

		# tournament/roulette selection

		self.individuals = individuals[:POPULATION_MAX] # TODO: its here just while there is no selection
		

	def getBest(self):
		return self.individuals[0]

	def getStatistics(self):
		max_fitness = self.individuals[0].fitness()
		min_fitness = self.individuals[-1].fitness()

		avg_fitness = 0.0
		for i in self.individuals:
			avg_fitness += i.fitness()
		avg_fitness /= POPULATION_MAX

		sqr_sum = 0.0
		for i in self.individuals:
			sqr_sum += (i.fitness() - avg_fitness)**2

		dev_fitness = math.sqrt(sqr_sum/POPULATION_MAX)
		return max_fitness, avg_fitness, min_fitness, dev_fitness

	def save(self, fileout):
		pass
