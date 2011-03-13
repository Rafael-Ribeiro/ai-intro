#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve
import math

class SmellSensor(breve.BraitenbergSensor):
	'''A BraitenbergSensor is used in conjunction with OBJECT(BraitenbergVehicle) to build Braitenberg vehicles.  This class is typically not instantiated manually, since OBJECT(BraitenbergVehicle) creates one for you when you add a sensor to the vehicle. <p> <b>NOTE: this class is included as part of the file "Braitenberg.tz".</b>'''

	def __init__(self, name, type, bias = 5.0): #type is an (r,g,b) vector (to identify the smell)
		breve.BraitenbergSensor.__init__(self,name)

		self.type = type
		self.setColor(type)

		self.bias = bias

		self.shape = breve.createInstances(breve.PolygonCone, 1, 5, 0.4, 0.5)
		self.setShape(self.shape)


	def iterate(self):
		total = 0

		for i in breve.allInstances("SmellSource"):
			if i.getType() != self.type:
				continue

			toSmell = i.getLocation() - self.getLocation()

			distance = toSmell.length()

			 # smell intensity is inversely proportional to d**2
			strength = i.getIntensity()/(1.0 + (distance*distance)/self.bias)
			total += strength
	
		total = min(total, 1.0)
		self.activators.activate(total, self)

breve.SmellSensor = SmellSensor
