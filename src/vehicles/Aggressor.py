#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-
# Light aggressor

import sys
sys.path.append("../") 

import breve
import math

from custom.light.source import LightSource
from custom.light.sensor import LightSensor
from custom.proximity.sensor import ProximitySensor
from lib.Activator import BraitenbergActivator

def leftActivator(vehicle, rightLightSensor):
	return rightLightSensor * 10 + 1

def rightActivator(vehicle, leftLightSensor):
	return leftLightSensor * 10 + 1

class AggressorVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(4, 0.7, 3))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.1)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.1)
	
		self.addWheel(self.leftWheel, breve.vector(-0.500000, 0, -1.500000))
		self.addWheel(self.rightWheel, breve.vector(-0.500000, 0, 1.500000))

		self.rightLightSensor = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2.0, breve.vector(0,1,0), 2.0)
		self.leftLightSensor = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2.0, breve.vector(0,1,0), 2.0)

		self.addSensor(self.rightLightSensor, breve.vector(2.0, 0.4, 1.5), breve.vector(1,0,0))
		self.addSensor(self.leftLightSensor,  breve.vector(2.0, 0.4,-1.5), breve.vector(1,0,0))

		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.rightLightSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftLightSensor], rightActivator)

class AggressorController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		N = 40
		R = 50
		D = 10

		self.vehicle = breve.createInstances(AggressorVehicle, 1).move(breve.vector(0, 2, R))
		self.watch(self.vehicle)

		# Scenario
		for i in range(N):
			light = breve.createInstances(breve.LightSource, 1, 1.0, breve.vector(0,1,0))
			light.move(breve.vector((R * breve.breveInternalFunctionFinder.sin(self, ((i * 6.280000) / N))), 1, (R * breve.breveInternalFunctionFinder.cos(self, ((i * 6.280000) / N)))))

AggressorController()
