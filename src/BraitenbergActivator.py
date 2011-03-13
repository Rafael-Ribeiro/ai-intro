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
			self.sensors[sensor.getName()] = 0

	def activate(self, value, sensor):
		self.sensors[sensor.getName()] = value
		self.wheel.activate(self.activationFunction(**self.sensors))
