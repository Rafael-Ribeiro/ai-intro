#!/usr/share/breve/bin/breve

# Light aggressor, that runs away from blocks

import breve
import math

from custom.light.source import LightSource
from custom.light.sensor import LightSensor
from custom.proximity.sensor import ProximitySensor
from lib.Activator import BraitenbergActivator

def leftActivator(rightLightSensor):
	return rightLightSensor*10 + 1

def rightActivator(leftLightSensor):
	return leftLightSensor*10 + 1

class AggressorController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		N = 40
		R = 50
		D = 10

		for i in range(N):
			light = breve.createInstances(breve.LightSource, 1, 1.0, breve.vector(0,1,0))
			light.move(breve.vector((R * breve.breveInternalFunctionFinder.sin(self, ((i * 6.280000) / N))), 1, (R * breve.breveInternalFunctionFinder.cos(self, ((i * 6.280000) / N)))))
		self.vehicle = breve.createInstances(breve.BraitenbergVehicle, 1, breve.vector(4, 0.7, 3))
		self.watch(self.vehicle)

		self.vehicle.move(breve.vector(0, 2, R))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.1)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.1)
	
		self.vehicle.addWheel(self.leftWheel, breve.vector(-0.500000, 0, -1.500000))
		self.vehicle.addWheel(self.rightWheel, breve.vector(-0.500000, 0, 1.500000))

		self.rightLightSensor = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/4.0, breve.vector(0,1,0), 2.0)
		self.leftLightSensor = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/4.0, breve.vector(0,1,0), 2.0)

		self.vehicle.addSensor(self.rightLightSensor, breve.vector(2.0, 0.4, 1.5), breve.vector(1,0,0))
		self.vehicle.addSensor(self.leftLightSensor,  breve.vector(2.0, 0.4,-1.5), breve.vector(1,0,0))

		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.rightLightSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftLightSensor], rightActivator)

breve.AggressorController = AggressorController

# Create an instance of our controller object to initialize the simulation

AggressorController()
