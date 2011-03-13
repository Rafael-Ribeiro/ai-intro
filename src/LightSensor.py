#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve

class LightSensor(breve.BraitenbergSensor):
	'''A BraitenbergSensor is used in conjunction with OBJECT(BraitenbergVehicle) to build Braitenberg vehicles.  This class is typically not instantiated manually, since OBJECT(BraitenbergVehicle) creates one for you when you add a sensor to the vehicle. <p> <b>NOTE: this class is included as part of the file "Braitenberg.tz".</b>'''

	def __init__( self ):
		breve.Link.__init__( self )

		self.direction = breve.vector()
		self.sensorAngle = 0

	def init( self, name, direction, angle):
		breve.BraitenbergSensor.init(self, name)

		self.direction = direction #breve.vector( 0, 1, 0 )
		self.sensorAngle = angle #1.600000

	def iterate( self ):
		total = 0

		transDir = self.getRotation() * self.direction
		for i in breve.allInstances("BraitenbergLights"):
			toLight = i.getLocation() - self.getLocation()
			angle = breve.breveInternalFunctionFinder.angle( self, toLight, transDir )

			if ( angle < self.sensorAngle ):
				distance = breve.length(toLight)
				strength = i.getIntensity()/(1.0 + (distance*distance))

				total += strength
	
		total = min(total, 1.0)
		print "Total: %d" % (total,)
		self.activators.activate(total, self)

breve.LightSensor = LightSensor
