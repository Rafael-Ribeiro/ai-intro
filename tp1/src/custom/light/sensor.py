#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve
import math
from source import LightSource

class LightSensor(breve.BraitenbergSensor):
	'''A BraitenbergSensor is used in conjunction with OBJECT(BraitenbergVehicle) to build Braitenberg vehicles.  This class is typically not instantiated manually, since OBJECT(BraitenbergVehicle) creates one for you when you add a sensor to the vehicle. <p> <b>NOTE: this class is included as part of the file "Braitenberg.tz".</b>'''

	def __init__( self, name, angle, color, bias = 5.0, sources = [LightSource]):
		breve.BraitenbergSensor.__init__(self,name)

		self.bias = bias
		self.color = color
		self.setColor(color)
	
		self.direction = breve.vector(0, 1, 0)
		self.sensorAngle = angle
		
		self.shape = breve.createInstances(breve.PolygonCone, 1, 10, 0.5, 0.15)

		self.setShape(self.shape)
		self.sources = sources

	def iterate(self):
		total = 0

		transDir = self.getRotation() * self.direction
		for c in self.sources:
			for i in breve.allInstances(c):
				if i.getColor() != self.color:
					continue

				toLight = i.getLocation() - self.getLocation()
				angle = breve.breveInternalFunctionFinder.angle( self, toLight, transDir )

				if ( angle < self.sensorAngle ):
					distance = toLight.length()/self.bias

					 # light intensity is inversely proportional to d**2 (area of sphere surface with radius d)
					strength = i.getIntensity()/(1.0 + (distance*distance))*math.cos((math.pi/self.sensorAngle)/2*angle)
					total += strength
	
		total = min(total, 1.0)
		self.activators.activate(total, self)

breve.LightSensor = LightSensor