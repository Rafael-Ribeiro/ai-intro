#!/usr/bin/env python
# -*- coding: utf-8 -*-

import breve

class SoundSource(breve.Link):
	def __init__(self, intensity, type, physics): #type is an (r,g,b) vector (to identify the smell)
		breve.Link.__init__(self)

		self.intensity = intensity
		self.type = type

		self.setShape(breve.createInstances(breve.Sphere,1).initWith(0.300000))
		self.setColor(type)
	
		if not physics:
			self.disablePhysics()

	def getIntensity(self):
		return self.intensity

	def getType(self):
		return self.type

breve.SoundSource = SoundSource
