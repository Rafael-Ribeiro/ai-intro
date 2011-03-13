#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve

class BraitenbergActivator:
	def __init__(self, wheel, fn):
		self.wheel = wheel
		self.activationFunction = fn
		self.sensors = {}

	def add(sensor):
		self.sensors[sensor.getName()] = 0

	def activate(value, sensor):
		self.sensors[sensor.getName()] = value
		self.wheel.activate(self.activationFunction(self.sensors))
