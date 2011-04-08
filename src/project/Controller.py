#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from random import sample

from custom.proximity.obstacles import SphereStationary
from custom.constants import direction as d
from Male import MaleVehicle
from Female import FemaleVehicle
from Egg import Egg

D = 3.0
class PopulationController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		
		for i in xrange(40):
			sphere = breve.createInstances(SphereStationary, 1).move(breve.vector((i-20)*D, 1, -20*D))
			sphere = breve.createInstances(SphereStationary, 1).move(breve.vector((i-20)*D, 1, 20*D))
			sphere = breve.createInstances(SphereStationary, 1).move(breve.vector(-20*D, 1, (i-20)*D))
			sphere = breve.createInstances(SphereStationary, 1).move(breve.vector(20*D, 1, (i-20)*D))

		#male = breve.createInstances(MaleVehicle, 1)
		#female = breve.createInstances(FemaleVehicle, 1)

		#male.move(breve.vector(-10, 2, 10))
		#female.move(breve.vector(10, 2, 10)).rotate(d.UP, math.pi)

		eggs = breve.createInstances(Egg, 4)
		eggs[0].move(breve.vector(10, -1, 10)) #breve.vector(0, 0, 10)
		eggs[1].move(breve.vector(-10, -1, 10)) #breve.vector(0, 0, 10)
		eggs[2].move(breve.vector(10, -1, -10)) #breve.vector(0, 0, 10)
		eggs[3].move(breve.vector(-10, -1, -10)) #breve.vector(0, 0, 10)

		#self.watch(male)
		self.watch(eggs[0])

		self.jazzMusic = breve.createInstances(breve.Sound, 1)
		self.jazzMusic.load("sounds/jazzMusic.wav")
		self.jazzMusic.play()

	def playJazzMusic(self):
		self.jazzMusic.play()

	def unwatch(self, obj): # return whether the object was the target or not
		if obj == self.watchObject:
			targets = breve.allInstances(MaleVehicle) + breve.allInstances(FemaleVehicle) + breve.allInstances(Egg)
			targets.remove(obj)
			try:
				self.watch(sample(targets, 1)[0])
			except ValueError:
				self.watch(None)
				self.pause()

			return True

		return False


if __name__ == '__main__':
	population = PopulationController()

	global asd
	asd = population
