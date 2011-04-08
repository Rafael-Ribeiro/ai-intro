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
		
		f = open('map', 'r')
		lines = f.readlines()
		for i in xrange(len(lines)):
			for j in xrange(len(lines[i])):
				if lines[i][j] == '*':
					breve.createInstances(SphereStationary, 1, 1.0).move(breve.vector(i*D, 1.0, j*D))
				if lines[i][j] == 'E':
					breve.createInstances(Egg, 1).move(breve.vector(i*D, -1.0, j*D))
		f.close()
		
		self.watch(breve.allInstances(Egg)[0])

		self.jazzMusic = breve.createInstances(breve.Sound, 1)
		self.jazzMusic.load("sounds/sax.wav")

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
