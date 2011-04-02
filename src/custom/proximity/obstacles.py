#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve

class SphereMobile(breve.Link):
	def __init__(self, opacity = 1.0, physics = False):
		breve.Link.__init__(self)

		self.shape = breve.createInstances(breve.Sphere, 1)
		self.shape.initWith(1.0)
		self.setShape(self.shape)
		self.opacity = opacity
			
		if not physics:
			self.disablePhysics()

	def getOpacity(self):
		return self.opacity

class SphereStationary(breve.Stationary):
	def __init__(self, opacity = 1.0):
		breve.Stationary.__init__(self)

		self.shape = breve.createInstances(breve.Sphere, 1)
		self.shape.initWith(1.0)
		self.setShape(self.shape)
		self.opacity = opacity

	def getOpacity(self):
		return self.opacity
