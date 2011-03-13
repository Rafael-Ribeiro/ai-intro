#!/usr/bin/python
# -*- coding: utf-8 -*-

#import breve

class BraitenbergActivator(object):
	def __init__(self, wheel, sensors, fn):
		self.wheel = wheel
		self.activationFunction = fn

		self.sensors = {}

		for sensor in sensors:
			sensor.link(self)
			self.sensors[sensor.getName()] = 1

	def activate(self, value, sensor):
		self.sensors[sensor.getName()] = min(max(value, 0.00001), 0.999999) # avoid division by zero errors
		self.wheel.activate(self.activationFunction(**self.sensors))
