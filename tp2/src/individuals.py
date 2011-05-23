#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import random

# physical constants
G_ACC = 9.80655

class Individual:
	def fitness(self):
		if self.fitness_val:
			return self.fitness_val

		x_i = config.A[0]
		y_i = maxHeight = config.A[1]
		v_i = time = 0.0

		points = self.getPoints()
	
		for i in range(1, len(self.points)):
			if self.points[i][1] > maxHeight or (self.points[i][1] == maxHeight and i != len(self.points)):
				print "c", i, maxHeight, self.points[i][1]
				return -1
			
			#Calculate acceleration based on segment slope. Open question - would be using cos() faster?
			#Since the angle had to be calculated beforehand, I don't think so
			dx = points[0][i] - x_i
			dy = points[1][i] - y_i
			li = math.sqrt(dx*dx + dy*dy)
			ai = -G_ACC*dy/float(li)
			
			#Energy conservation. You really needn't be reading this, but if you have doubts, tell me
			v_j = math.sqrt(2*(-G_ACC*dy + v_i*v_i/2))
			#If speed is less than 0, forget about it. This actually never happens thanks to our checks.
			#But you never know what magic lies in wait...

			if v_j <= 0.0:
				sys.exit(-1)
				return -1

			dv = v_j - v_i
			
			#The speed variation over the acceleration gives us the time. Voila
			time += dv/ai if ai != 0 else li/v_j

			#Debugging, ignore
			if config.DEBUG_MODE:
				print "Segment " + str(i/2)
				print "dX: " + str(dx) + " dY: " + str(dy)
				print "Distance Travelled: " + str(li)
				print "Gained velocity: " + str(dv)
				print "Acceleration: " + str(ai)
				print "Time to travel: " + time +"\n"
			
			#Update the positions and current speed
			v_i = v_j
			x_i = self.points[0][i]
			y_i = self.points[1][i]
		
		self.fitness_val = time
		return time

class EvenSpacing(Individual):
	@staticmethod
	def new(n):
		genes = [(random.random() - 0.5) * 2 * config.DY + config.B[1] for i in xrange(n-2)]
		return EvenlySpaced([config.A[1]] + genes + [config.B[1]])

	# List of n points (2 sized arrays: [abs x, abs y])
	def __init__(self, points):
		self.points = points
		self.n = len(points)
		self.fitness_val = None

	def crossover(self, other):
		length = random.randint(0, config.CROSSOVER_LEN_MAX)
		start = random.randint(0, self.n - length)
		end = start + length

		tempPoints = self.points[:start] + other.points[start:end] + self.points[end:]
		other.points = other.points[:start] + self.points[start:end] + other.points[end:]
		self.points = tempPoints

		self.fitness_val = None
		other.fitness_val = None
	
	def getPoints(self):
		dx = (B[0]-A[0])/(len(self.n)-1)
		x = [A[0]+i*dx for i in xrange(self.n-1)] + [B[0]]

		return x, self.points

	def mutate(self):
		prob = config.MUTATION

		for i in xrange(1, self.n-1):
			if random.random() > prob:
				# mutate this gene
				dy = random.gauss(0, config.MUTATION_Y_STDEV)
				self.points = min(self.points[i] + dy, config.A[1] - config.DY_MIN)

				prob = config.MUTATION_BURST
			else:
				prob = config.MUTATION

class DynamicSpacing(Individual):
	@staticmethod
	def new(nPoints):
		genes = [[config.A[0] + config.DX*i/(nPoints-1), (random.random() - 0.5) * 2 * config.DY + config.B[1]] for i in xrange(1,nPoints-1)]
		return Individual([config.A] + genes + [config.B])

	# List of n points (2 sized arrays: [abs x, abs y])
	def __init__(self, points):
		self.points = points
		self.fitness_val = None

	def _findXCoord(self, x): # returns a tuple (index, splitNeeded)
		for i in xrange(len(self.points)):
			if self.points[i][0] >= x:
				return i, self.points[i][0] != x

		print "_findXCoord Error: {0} exceeds boundaries {1}".format(x, self.points[-1][0])
		sys.exit(-1)

		return -1

	def _splitXCoord(self, x):
		xIndex, splitNeeded = self._findXCoord(x)

		if not splitNeeded:
			return xIndex

		self.points.insert(xIndex,[x, self.points[xIndex][1]])

		return xIndex

	def crossover(self, other):
		crossoverMaxLen = random.random() * config.CROSSOVER_LEN_MAX * config.DX

		xInit = random.random() * (config.DX - crossoverMaxLen)
		xEnd = startingCrossoverPoint + crossoverMaxLen

		xi1, xj1 = self.crossoverSegment(xInit, xEnd)
		xi2, xj2 = other.crossoverSegment(xInit, xEnd)

		tempPoints = self.points[:xi1] + other.points[xi2:xj2] + self.points[xj1:]
		other.points = other.points[:xi2] + self.points[xi1:xj1] + other.points[xj2:]
		self.points = tempPoints

		self.fitness_val = None
		other.fitness_val = None
	
	def crossoverSegment(self, xInit, xEnd):
		return self._splitXCoord(xInit), self._splitXCoord(xEnd) + 1

	def fitness(self):
		if self.fitness_val:
			return self.fitness_val

		x_i = config.A[0]
		y_i = maxHeight = config.A[1]
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
			dx = self.points[i][0] - x_i
			dy = self.points[i][1] - y_i
			li = math.sqrt(dx*dx + dy*dy)
			ai = -G_ACC*dy/float(li)
			
			#Energy conservation. You really needn't be reading this, but if you have doubts, tell me
			v_j = math.sqrt(2*(-G_ACC*dy + v_i*v_i/2))
			#If speed is less than 0, forget about it. This actually never happens thanks to our checks.
			#But you never know what magic lies in wait...

			if v_j <= 0.0:
				sys.exit(-1)
				return -1

			dv = v_j - v_i
			
			#The speed variation over the acceleration gives us the time. Voila
			time += dv/ai if ai != 0 else li/v_j

			#Debugging, ignore
			if config.DEBUG_MODE:
				print "Segment " + str(i/2)
				print "dX: " + str(dx) + " dY: " + str(dy)
				print "Distance Travelled: " + str(li)
				print "Gained velocity: " + str(dv)
				print "Acceleration: " + str(ai)
				print "Time to travel: " + time +"\n"
			
			#Update the positions and current speed
			v_i = v_j
			x_i = self.points[i][0]
			y_i = self.points[i][1]
		
		self.fitness_val = time
		return time

	def getPoints(self):
		x = [i[0] for i in self.points]
		y = [i[1] for i in self.points]

		return x, y

	def mutate(self):
		prob = config.MUTATION_PROB

		for i in xrange(1,len(self.points)-1):
			if random.random() <= prob:
				window = self.points[i+1][0] - self.points[i-1][0] - 2 * config.DX_MIN
				self.points[i][0] = self.points[i-1][0] + config.DX_MIN + random.random() * window

				self.points[i][1] += (random.random() - 0.5) * 2 * config.MUTATION_Y * config.DY
				self.points[i][1] = min(self.points[i][1], config.A[1] - config.DY_MIN)

				prob = config.MUTATION_BURST
			else:
				prob = config.MUTATION_PROB

		self.fitness_val = None
