#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import random
import math
from operator import itemgetter

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
		points = random.randint(1, config.CROSSOVER_POINTS)		
		cross = [random.randint(1, self.n-2) for i in xrange(points)]
		cross.sort()

		swap = False
		i = 0
		for j in xrange(1, self.n-2):
			while i < points and cross[i] == j:
				swap = not swap
				i += 1

			if swap:
				tmp = self.points[j]
				self.points[j] = other.points[j]
				other.points[j] = tmp

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

		self.fitness_val = None

	def mutateRR(self):
		mutations = random.sample(range(1,len(self.points)-1),min(1,int(len(self.points) * config.MUTATION_PROB)))

		for mutIndex in mutations:
			# mutate this gene
			dy = random.gauss(0, config.MUTATION_Y_STDEV)
			self.points[mutIndex] = min(self.points[mutIndex] + dy, config.A[1] - config.DY_MIN)

		self.fitness_val = None

class DynamicSpacing(Individual):
	@staticmethod
	def new(nPoints):
		genes = [[config.A[0] + config.DX*i/(nPoints-1), (random.random() - 0.5) * 2 * config.DY + config.B[1]] for i in xrange(1,nPoints-1)]
		return DynamicSpacing([config.A] + genes + [config.B])

	# List of n points (2 sized arrays: [abs x, abs y])
	def __init__(self, points):
		self.points = points
		self.fitness_val = None
	"""
		def _findXCoord(self, x): # returns a tuple (index, splitNeeded)
			for i in xrange(len(self.points)):
				if self.points[i][0] >= x:
					return i, self.points[i][0] != x

			print "_findXCoord Error: {0} exceeds boundaries {1}".format(x, self.points[-1][0])
			sys.exit(-1)

			return -1

		def _splitXCoord(self, x):
			xIndex, splitNeeded = self._findXCoord(x)

			if splitNeeded:
				self.points.insert(xIndex,[x, self.points[xIndex][1]])

			return xIndex
	"""
	def crossover(self, other):
		points = random.randint(1, config.CROSSOVER_POINTS)		
		cross = [config.A[0]+config.DX_MIN + random.random()*(config.DX-2*config.DX_MIN) for i in xrange(points)]
		cross.sort()

		lasta = a = 1
		lastb = b = 1
		swap = False
		tmpA = [self.points[0]]
		tmpB = [other.points[0]]

		for x in cross:
			while self.points[a][0] < x:
				a += 1
			while other.points[b][0] < x:
				b += 1

			if swap:
				tmpA += other.points[lastb:b]
				tmpB += self.points[lasta:a]
			else:
				tmpB += self.points[lasta:a]
				tmpA += other.points[lastb:b]

			swap = not swap
			lasta = a
			lastb = b

		if swap:
			tmpA += other.points[lastb:]
			tmpB += self.points[lasta:]
		else:
			tmpB += self.points[lasta:]
			tmpA += other.points[lastb:]

		self.points = tmpA
		other.points = tmpB
		
		self.interpolate()
		other.interpolate()

		self.fitness_val = None
		other.fitness_val = None
	
	def crossoverSegment(self, xInit, xEnd):
		a = self._splitXCoord(xInit)
		b = self._splitXCoord(xEnd)

		return a, b + 1

	def getPoints(self):
		x = [i[0] for i in self.points]
		y = [i[1] for i in self.points]

		return x, y

	def interpolate(self):
		needed = config.POINTS_INIT - len(self.points)

		if needed > 0:
			for i in xrange(needed):
				k = random.choice(xrange(len(self.points)-1))
				self.points.insert(k+1, [(self.points[k][0]+self.points[k+1][0])/2, (self.points[k][1]+self.points[k+1][1])/2])
		elif needed < 0:
			for k in xrange(-needed):
				self.points.pop(random.randint(1, len(self.points)-2))

	def mutate(self):
		prob = config.MUTATION_PROB

		for i in xrange(1,len(self.points)-1):
			if random.random() <= prob:
				# x coord deviation
				xCoord = self.points[0][0] # guarantee that at least one random occurs
				xs = map(lambda x: x[0],self.points) # only use x coords

				while xCoord in xs:
					dx = random.gauss(0, config.MUTATION_X_STDEV)
					xCoord = max(config.A[0] + config.DX_MIN,min(self.points[i][0] + dx,config.B[0] - config.DX_MIN))

				self.points[i][0] = xCoord

				# y coord deviation
				dy = random.gauss(0, config.MUTATION_Y_STDEV)
				self.points[i][1] = min(self.points[i][1] + dy, config.A[1] - config.DY_MIN)

				prob = config.MUTATION_PROB + config.MUTATION_BURST
			else:
				prob = config.MUTATION_PROB

		self.points.sort(key = itemgetter(0))

		self.fitness_val = None

	def mutateRR(self):
		mutations = random.sample(range(1,len(self.points)-1),min(1,int(len(self.points) * config.MUTATION_PROB)))

		xs = map(lambda x: x[0],self.points) # only use x coords
		for mutIndex in mutations:
			# x coord deviation
			xCoord = self.points[mutIndex][0]

			while xCoord in xs:
				dx = random.gauss(0, config.MUTATION_X_STDEV)
				xCoord = max(config.A[0] + config.DX_MIN,min(self.points[mutIndex][0] + dx,config.B[0] - config.DX_MIN))

			self.points[mutIndex][0] = xCoord

			# y coord deviation
			dy = random.gauss(0, config.MUTATION_Y_STDEV)
			self.points[mutIndex][1] = min(self.points[mutIndex][1] + dy, config.A[1] - config.DY_MIN)

		self.points.sort(key = itemgetter(0))

		self.fitness_val = None
