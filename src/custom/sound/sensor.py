#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve
import math

### TODO: This is a copy of light sensor... Adapt to cardioid formula.
### UNTESTED MODIFICATIONS

class SoundSensor(breve.BraitenbergSensor):
	def __init__( self, name, type = breve.vector(0,0,1), angle = (3.0 * math.pi / 2), bias = 5.0 ):
		breve.BraitenbergSensor.__init__(self,name)

		self.bias = bias
		self.type = type
		self.setColor(type)
	
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

			# TODO: the problem NOW is that angle is [0, pi] and should be [-pi, pi]
			# calc manualy?, or...
			angle = breve.breveInternalFunctionFinder.angle(self, toSound, transDir)
			distance = toSound.length()
			strength = i.getIntensity()*0.5*((1+sin(angle))/(distance/self.bias+1))

			total += strength
	
		total = min(total, 1.0)
		self.activators.activate(total, self)

breve.SoundSensor = SoundSensor
