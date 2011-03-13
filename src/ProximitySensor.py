#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve

class ProximitySensor(breve.BraitenbergSensor):
	def __init__(self, name):
		breve.BraitenbergSensor.__init__(self, name)

	def iterate( self ):
		i = None
		lights = 0
		angle = 0
		strength = 0
		
		proximity = float("infinity")
		transDir = breve.vector()
		toLight = breve.vector()

		transDir = ( self.getRotation() * self.direction )
		for i in breve.allInstances("Shape"):
			toLight = i.getLocation() - self.getLocation()
			angle = breve.breveInternalFunctionFinder.angle( self, toShape, transDir )

			if ( angle < self.sensorAngle ):
				proximity = min(proximity, distance(self.getLocation()))

		self.activators.activate(proximity, self)

breve.ProximitySensor = ProximitySensor
