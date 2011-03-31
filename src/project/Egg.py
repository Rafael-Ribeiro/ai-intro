#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.light.source import LightSource
from custom.constants import color

BIRTH_TIME = 30.0
MIN_SIZE = .5
MAX_SIZE = 2.5

class Egg(LightSource):
	def __init__(self):
		LightSource.__init__(self, 1.0, color.EGG, True)
		
		self.setShape(breve.createInstances(breve.Sphere, 1).initWithSphere(MIN_SIZE))

	def iterate(self):
		self.age = self.getAge()

		if self.age >= BIRTH_TIME: # work
			return
		
		shape = breve.createInstances(breve.Sphere, 1).initWithSphere(self.age/BIRTH_TIME*(MAX_SIZE-MIN_SIZE)+MIN_SIZE)
		self.setShape(shape)
		self.offset(breve.vector(0,0.01,0))
