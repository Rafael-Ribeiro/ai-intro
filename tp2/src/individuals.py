#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import random
import math

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
	
		for i in range(1, len(points[0])):
			if points[1][i] > maxHeight or (points[1][i] == maxHeight and i != len(points[0])):
				print "c", i, maxHeight, points[1][i]
				return -1
			
			#Calculate acceleration based on segment slope. Open question - would be using cos() faster?
			#Since the angle had to be calculated beforehand, I don't think so
			dx = points[0][i] - x_i
			dy = points[1][i] - y_i
			li = math.sqrt(dx*dx + dy*dy)
			try:
				ai = -G_ACC*dy/float(li)
			except:
				print points		
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
			x_i = points[0][i]
			y_i = points[1][i]
		
		self.fitness_val = time
		return time

class EvenSpacing(Individual):
	@staticmethod
	def new(n):
		genes = [(random.random() - 0.5) * 2 * config.DY + config.B[1] for i in xrange(n-2)]
		return EvenSpacing([config.A[1]] + genes + [config.B[1]])

	# List of n points (2 sized arrays: [abs x, abs y])
	def __init__(self, points):
		self.points = points
		self.n = len(points)
		self.fitness_val = None

	def crossover(self, other):
		length = random.randint(1, int(self.n * config.CROSSOVER_LEN_MAX))
		start = random.randint(0, self.n - length)
		end = start + length

		tempPoints = self.points[:start] + other.points[start:end] + self.points[end:]
		other.points = other.points[:start] + self.points[start:end] + other.points[end:]
		self.points = tempPoints

		self.fitness_val = None
		other.fitness_val = None
	
	def getPoints(self):
		dx = (config.B[0]-config.A[0])/(self.n-1)
		x = [config.A[0]+i*dx for i in xrange(self.n-1)] + [config.B[0]]

		return x, self.points

	def mutate(self):
		prob = config.MUTATION_PROB

		for i in xrange(1, self.n-1):
			if random.random() > prob:
				# mutate this gene
				dy = random.gauss(0, config.MUTATION_Y_STDEV)
				self.points[i] = min(self.points[i] + dy, config.A[1] - config.DY_MIN)

				prob = config.MUTATION_PROB + config.MUTATION_BURST
			else:
				prob = config.MUTATION_PROB

class DynamicSpacing(Individual):
	@staticmethod
	def new(nPoints):
		genes = [[config.A[0] + config.DX*i/(nPoints-1), (random.random() - 0.5) * 2 * config.DY + config.B[1]] for i in xrange(1,nPoints-1)]
		return DynamicSpacing([config.A] + genes + [config.B])

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
			return xIndex, splitNeeded

		self.points.insert(xIndex,[x, self.points[xIndex][1]])

		return xIndex, splitNeeded

	def crossover(self, other):
		crossoverMaxLen = random.random() * config.CROSSOVER_LEN_MAX * config.DX

		xInit = random.random() * (config.DX - crossoverMaxLen)
		xEnd = xInit + crossoverMaxLen

		xi1, xj1 = self.crossoverSegment(xInit, xEnd)
		xi2, xj2 = other.crossoverSegment(xInit, xEnd)

		tempPoints = self.points[:xi1] + other.points[xi2:xj2] + self.points[xj1:]
		other.points = other.points[:xi2] + self.points[xi1:xj1] + other.points[xj2:]
		self.points = tempPoints

		other.interpolate()
		self.interpolate()

		self.fitness_val = None
		other.fitness_val = None
	
	def crossoverSegment(self, xInit, xEnd):
		a, splita = self._splitXCoord(xInit)
		b, splitb = self._splitXCoord(xEnd)

		count = 0
		if splita:
			count += 1
		if splitb:
			count += 1

		for k in xrange(count):
			i = b
			while (i == b or i == a):
				i = random.randint(1, len(self.points)-2)

			if i < a:
				a -= 1
			if i < b:
				b -= 1

			self.points.pop(i)

		return a, b + 1

	def getPoints(self):
		x = [i[0] for i in self.points]
		y = [i[1] for i in self.points]

		return x, y

	def interpolate(self):
		needed = config.POINTS_INIT - len(self.points)

		for i in xrange(needed):
			k = random.choice(xrange(len(self.points)-1))
			self.points.insert(k+1, [(self.points[k][0]+self.points[k+1][0])/2, (self.points[k][1]+self.points[k+1][1])/2])

		print len(self.points)

	def mutate(self):
		prob = config.MUTATION_PROB

		for i in xrange(1,len(self.points)-1):
			if random.random() <= prob:
				window = self.points[i+1][0] - self.points[i-1][0] - 2 * config.DX_MIN
				self.points[i][0] = self.points[i-1][0] + config.DX_MIN + random.random() * window

				dy = random.gauss(0, config.MUTATION_Y_STDEV)
				self.points[i][1] = min(self.points[i][1] + dy, config.A[1] - config.DY_MIN)

				prob = config.MUTATION_PROB + config.MUTATION_BURST
			else:
				prob = config.MUTATION_PROB

		self.fitness_val = None
