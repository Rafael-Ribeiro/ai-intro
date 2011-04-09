#!/usr/bin/python
# -*- coding: utf-8 -*-

#import breve

class BraitenbergActivator(object):
	def __init__(self, vehicle, wheel, sensors, fn):
		self.vehicle = vehicle
		self.wheel = wheel
		self.activationFunction = fn

		self.sensors = {}

		for sensor in sensors:
			sensor.link(self)
			self.sensors[sensor.getName()] = 1

	def activate(self, value, sensor):
		self.sensors[sensor.getName()] = value
		self.wheel.activate(self.activationFunction(self.vehicle, **self.sensors))
