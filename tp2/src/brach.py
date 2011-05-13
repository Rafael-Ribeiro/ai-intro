#!/usr/bin/python
# -*- coding: utf-8 -*- 

import math

# program constants
DEBUG_MODE = True		# console prints

POINTS_MAX = 500		# max number of points per individual
ELITISM = 0.1			# percentage
CROSSOVER = 0.05		# probability
CROSSOVER_MAX = 0.25	# 1 quarter of the individual is cut
MUTATION_X = 0.01		# probability
MUTATION_Y = 0.01		# probability

SELECTION_TYPE = "TOURNAMENT" # "ROULETTE"
POPULATION_MAX = 500	# size of population, must be pair

# physical constants
G_ACC = 9.80655

class Individual:
	def new(nPoints, A, B):
		
		dx = float(B[0] - A[0])
		dy = float(B[1] - A[1])

		return Individual([[dx/nPoints, (random.random() - 0.5) * 2 * dy + B[1]] for i in xrange(nPoints)])

	# List of n points (2 sized arrays: [dx, abs y])
	def __init__(self, points):
		self.points = points

	def mutate(self):

	def cross(self, other):

	def fitness(self):
		x_i = self.points[0][0]
		y_i = maxHeight = self.points[0][1]
		v_i = time = 0
		
		#It has to have at least 2 points, otherwise it is not doable
		if(len(self.points) < 2):
			return -1;
		
		for i in range(1, len(self.points)):
			#Consistency checking. This wasn't done in a separate function for quickness
			if(self.points[i][0] <= x_i):
				return -1
			if(self.points[i][1] >= maxHeight):
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
			if(v_j < 0.0):
				return -1
			dv = v_j - v_i
			
			#The speed variation over the acceleration gives us the time. Voila
			time += dv/ai
			
			#Debugging, ignore
			if(debug):
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

	
class Population:
	def new(nIndividuals, A, B):
		individuals = [Individual.new(POINTS_MAX, A, B) for i in xrange(nIndividuals)]

		return Population(individuals)

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
