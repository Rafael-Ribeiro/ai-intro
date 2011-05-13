#!/usr/bin/python
# -*- coding: utf-8 -*- 

try:
	import	gtk
	import	gtk.glade
except:
	print	"You	need	to	install	pyGTK	or	GTK"
	sys.exit(1)

GUI_FILENAME = "gui.xml"

ITERATIONS = 1000		# number of iterations

POPULATION_MAX = 500	# size of population, must be pair
SELECTION_TYPE = "TOURNAMENT" # "ROULETTE"

POINTS_MAX = 500		# max number of points per individual
ELITISM = 0.1			# percentage
CROSSOVER = 0.05		# probability
CROSSOVER_MAX = 0.25	# 1 quarter of the individual is cut
MUTATION_X = 0.01		# probability
MUTATION_Y = 0.01		# probability


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

class BrachGUI:
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file(filename)
	
		self.builder.connect_signals(self)
		self.builder.get_object('window_main').show()

if __name__ == '__main__':
	app=SimulatorGUI()
	gtk.main()
