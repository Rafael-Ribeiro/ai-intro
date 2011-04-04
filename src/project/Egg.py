#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.light.source import LightSource
from custom.constants import color, direction as d
from random import random

BIRTH_TIME = 20.0
MIN_SIZE = .5
MAX_SIZE = 2.5

class Egg(LightSource):
	def __init__(self):
		LightSource.__init__(self, 1.0, color.EGG, True)
		
		self.setShape(breve.createInstances(breve.Sphere, 1).initWithSphere(MIN_SIZE))

	def iterate(self):
		self.age = self.getAge()

		if self.age >= BIRTH_TIME:
			sex = random()

			if sex < 0.5:
				from Male import MaleVehicle
				child = breve.createInstances(MaleVehicle, 1)

			else:
				from Female import FemaleVehicle
				child = breve.createInstances(FemaleVehicle, 1)

			child.move(self.getLocation())
			child.rotate(d.UP, math.pi*2*random())

			breve.deleteInstances(self)
			return
		
		shape = breve.createInstances(breve.Sphere, 1).initWithSphere(self.age/BIRTH_TIME*(MAX_SIZE-MIN_SIZE)+MIN_SIZE)
		self.setShape(shape)
		self.offset(breve.vector(0,0.01,0))

	def getOpacity(self):
		return 1.0
