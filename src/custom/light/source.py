#!/usr/bin/env python
# -*- coding: utf-8 -*-

import breve

class LightSource(breve.Mobile):
	'''A BraitenbergLight is used in conjunction with OBJECT(BraitenbergControl) and OBJECT(BraitenbergVehicle).  It is what the OBJECT(BraitenbergSensor) objects on the BraitenbergVehicle detect. <p> There are no special behaviors associated with the lights--they're  basically just plain OBJECT(Mobile) objects.'''

	def __init__(self, intensity, color):
		breve.Mobile.__init__(self)

		self.intensity = intensity
		self.setShape(breve.createInstances(breve.Sphere, 1).initWithSphere(0.300000))
		self.setColor(color)
	
	def getIntensity(self):
		return self.intensity

breve.LightSource = LightSource
