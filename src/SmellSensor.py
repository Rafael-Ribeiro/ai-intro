#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve
import math

class SmellSensor(breve.BraitenbergSensor):
	'''A BraitenbergSensor is used in conjunction with OBJECT(BraitenbergVehicle) to build Braitenberg vehicles.  This class is typically not instantiated manually, since OBJECT(BraitenbergVehicle) creates one for you when you add a sensor to the vehicle. <p> <b>NOTE: this class is included as part of the file "Braitenberg.tz".</b>'''

	def __init__(self):
		breve.BraitenbergSensor.__init__(self)

		self.bias = 0
		self.direction = breve.vector()
		self.sensorAngle = 0

	def init(self, name, angle, bias = 5.0):
		breve.BraitenbergSensor.init(self, name)
		
		self.bias = bias
		self.direction = breve.vector(0, 1, 0)
		self.sensorAngle = angle #1.600000

	def iterate(self):
		total = 0

		transDir = self.getRotation() * self.direction
		for i in breve.allInstances("SmellSource"):
			toSmell = i.getLocation() - self.getLocation()
			angle = breve.breveInternalFunctionFinder.angle(self, toSmell, transDir)

			if (angle < self.sensorAngle):
				distance = breve.length(toSmell)

				 # sound intensity is inversely proportional to d**2
				strength = i.getIntensity()/(1.0 + (distance*distance)/self.bias)
				total += strength
	
		total = min(total, 1.0)
		self.activators.activate(total, self)

breve.SmellSensor = SmellSensor
