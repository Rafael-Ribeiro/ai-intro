#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve

#TODO: Everything (the code is a template)

class SmellSensor(breve.BraitenbergSensor):
	def __init__( self ):
		breve.BraitenbergSensor.__init__(self)

	def iterate( self ):
		i = None
		smellSources = 0
		angle = 0
		strength = 0
		total = 0
		transDir = breve.vector()
		toLight = breve.vector()

		transDir = ( self.getRotation() * self.direction )
		for i in breve.allInstances( "SmellSource" ):
			toLight = ( i.getLocation() - self.getLocation() )
			angle = breve.breveInternalFunctionFinder.angle( self, toLight, transDir )
			if ( angle < self.sensorAngle ):
				strength = breve.length( ( self.getLocation() - i.getLocation() ) )
				strength = ( 1.000000 / ( strength * strength ) )
				if ( self.activationMethod and self.activationObject ):
					strength = self.activationObject.callMethod( self.activationMethod, [ strength ] )


				if ( strength > 10 ):
					strength = 10

				total = ( total + strength )
				lights = ( lights + 1 )




		if ( lights != 0 ):
			total = ( total / lights )

		self.wheels.activate( total )

breve.SmellSensor = SmellSensor
