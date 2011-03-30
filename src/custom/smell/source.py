#!/usr/bin/env python
# -*- coding: utf-8 -*-

import breve

class SmellSource(breve.Link):
	def __init__(self, intensity, type): #type is an (r,g,b) vector (to identify the smell)
		breve.Link.__init__(self)

		self.intensity = intensity
		self.type = type

		self.setShape(breve.createInstances(breve.Sphere,1).initWith(0.300000))
		self.setColor(type)

	def getIntensity(self):
		return self.intensity

	def getType(self):
		return self.type


breve.SmellSource = SmellSource
