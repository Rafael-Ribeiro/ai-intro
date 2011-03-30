#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve
import math

class SoundSensor(breve.BraitenbergSensor):
	def __init__( self, name, type = breve.vector(0,0,1), bias = 5.0, balance = 0.5):
		breve.BraitenbergSensor.__init__(self,name)

		self.bias = bias
		self.type = type
		self.setColor(type)
	
		self.direction = breve.vector(0, 1, 0)

		self.shape = breve.createInstances(breve.PolygonCone, 1, 20, 0.3, 0.3)
		self.setShape(self.shape)

		self.frequency = type.x*3900 + type.y*6000 + type.z*10000 + 100 # Minimum frequency = 100Hz, maximum frequency = 20000Hz
		self.balance = balance
		self.tone = breve.createInstances(breve.Tone, 1, self.frequency, self.balance)

	def iterate(self):
		total = 0

		transDir = self.getRotation() * self.direction
		for i in breve.allInstances("SoundSource"):
			if i.getType() != self.type:
				continue

			toSound = i.getLocation() - self.getLocation()

			angle = breve.breveInternalFunctionFinder.angle(self, toSound, transDir)
			distance = toSound.length()

			strength = i.getIntensity()*0.5*((1+math.cos(angle))/(distance/self.bias+1))

			total += strength
	
		total = min(total, 1.0)

		self.tone.setVolume(min(total,0.5)) # Total ranges from 0 to 1, the same as volume

		self.activators.activate(total, self)

breve.SoundSensor = SoundSensor
