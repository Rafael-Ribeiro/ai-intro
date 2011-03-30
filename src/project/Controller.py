#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.proximity.obstacles import SphereMobile
from Male import MaleVehicle
from Female import FemaleVehicle

D = 3
class PopulationController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		
		for i in xrange(100):
			sphere = breve.createInstances(SphereMobile, 1).move(breve.vector((i-50)*D, 1, -50*D))
			sphere = breve.createInstances(SphereMobile, 1).move(breve.vector((i-50)*D, 1, 50*D))
			sphere = breve.createInstances(SphereMobile, 1).move(breve.vector(-50*D, 1, (i-50)*D))
			sphere = breve.createInstances(SphereMobile, 1).move(breve.vector(50*D, 1, (i-50)*D))

		male = MaleVehicle()
		female = FemaleVehicle()

		male.move(breve.vector(10, 2, 0))
		female.move(breve.vector(-10, 2, 0))
		self.watch(male)

orbit = PopulationController()
