#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.proximity.obstacles import SphereMobile

from Male import MaleVehicle
from Female import FemaleVehicle
from Egg import Egg

D = 2.0
class PopulationController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		
		for i in xrange(40):
			sphere = breve.createInstances(SphereMobile, 1).move(breve.vector((i-20)*D, 1, -20*D))
			sphere = breve.createInstances(SphereMobile, 1).move(breve.vector((i-20)*D, 1, 20*D))
			sphere = breve.createInstances(SphereMobile, 1).move(breve.vector(-20*D, 1, (i-20)*D))
			sphere = breve.createInstances(SphereMobile, 1).move(breve.vector(20*D, 1, (i-20)*D))

		male = MaleVehicle()

		egg = Egg()
		egg.move(breve.vector(10, 10, 10))
		male.move(breve.vector(-10, 2, 10))

		self.watch(male)


orbit = PopulationController()
