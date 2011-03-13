#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve
import math

### TODO: This is a copy of light sensor... Adapt to cardioid formula.
### UNTESTED MODIFICATIONS

class SoundSensor(breve.BraitenbergSensor):
	def __init__( self, name, angle = (3.0 * math.pi / 2), type = breve.vector(0,0,1), bias = 5.0 ):
		breve.BraitenbergSensor.__init__(self,name)

		self.bias = bias
		self.type = type
		self.setColor(color)
	
		self.direction = breve.vector(0, 1, 0)
		self.sensorAngle = angle

		self.shape = breve.createInstances(breve.PolygonCone, 1, 3, 0.3, 0.7)
		self.setShape(self.shape)

	def iterate(self):
		total = 0

		transDir = self.getRotation() * self.direction
		for i in breve.allInstances("SoundSource"):
			if i.getType() != self.type:
				continue

			toSound = i.getLocation() - self.getLocation()
			angle = breve.breveInternalFunctionFinder.angle( self, toSound, transDir )

			if ( angle < self.sensorAngle ):
				distance = toSound.length()

				 # sound intensity is inversely proportional to d**2 (area of sphere surface with radius d)
				strength = i.getIntensity()/(1.0 + (distance*distance)/self.bias)
				total += strength
	
		total = min(total, 1.0)
		self.activators.activate(total, self)

breve.SoundSensor = SoundSensor
