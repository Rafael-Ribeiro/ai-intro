#!/usr/bin/env python
# -*- coding: utf-8 -*-

import breve

class LightSource(breve.Link):
	'''A BraitenbergLight is used in conjunction with OBJECT(BraitenbergControl) and OBJECT(BraitenbergVehicle).  It is what the OBJECT(BraitenbergSensor) objects on the BraitenbergVehicle detect. <p> There are no special behaviors associated with the lights--they're  basically just plain OBJECT(Mobile) objects.'''

	def __init__(self, intensity, color, physics = False):
		breve.Link.__init__(self)

		self.intensity = intensity
		self.shape = breve.createInstances(breve.Sphere, 1).initWithSphere(0.300000)

		self.setShape(self.shape)
		self.setColor(color)
				
		if not physics:
			self.disablePhysics()

	def getIntensity(self):
		return self.intensity

breve.LightSource = LightSource
