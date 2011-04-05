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

D = 2.0
class PopulationController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		
		for i in xrange(40):
			sphere = breve.createInstances(SphereStationary, 1).move(breve.vector((i-20)*D, 1, -20*D))
			sphere = breve.createInstances(SphereStationary, 1).move(breve.vector((i-20)*D, 1, 20*D))
			sphere = breve.createInstances(SphereStationary, 1).move(breve.vector(-20*D, 1, (i-20)*D))
			sphere = breve.createInstances(SphereStationary, 1).move(breve.vector(20*D, 1, (i-20)*D))

		male = breve.createInstances(MaleVehicle, 1)
		female = breve.createInstances(FemaleVehicle, 1)

		male.move(breve.vector(-10, 2, 10))
		female.move(breve.vector(10, 2, 10)).rotate(d.UP, 0.1)
		female.move(breve.vector(10, 2, 10)).rotate(d.UP, math.pi)

		egg = breve.createInstances(Egg, 1).move(breve.vector(0, 2, 10))

		self.watch(male)
		self.target = male

	def unwatch(self, obj):
		if obj == self.watchObject:
			targets = breve.allInstances(MaleVehicle) + breve.allInstances(FemaleVehicle) + breve.allInstances(Egg)
			targets.remove(obj)
			try:
				self.watch(sample(targets, 1)[0])
			except ValueError:
				self.watch(None)
				self.pause()


if __name__ == '__main__':
	population = PopulationController()
