#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve

class ProximitySensor(breve.BraitenbergSensor):
	def __init__(self, name, angle):
		breve.BraitenbergSensor.__init__(self, name)

		self.direction = breve.vector(0, 1, 0)
		self.sensorAngle = angle

		self.shape = breve.createInstances(breve.PolygonCone, 1, 10, 0.2, 0.2)
		self.setColor(breve.vector(0,0,0))
		self.setShape(self.shape)

	def iterate( self ):
		proximity = float("infinity")

		transDir = self.getRotation() * self.direction

		for obj in breve.allInstances("Real"):
			i = obj.getCollisionShape()
			toLight = obj.getLocation() - self.getLocation()
			angle = breve.breveInternalFunctionFinder.angle(self, toShape, transDir )

			if (angle < self.sensorAngle):
				proximity = min(proximity, i.distance(self.getLocation()))

		print proximity

		self.activators.activate(proximity, self)

