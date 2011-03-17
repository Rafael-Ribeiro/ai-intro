#!/usr/share/breve/bin/breve

# Light aggressor, that runs away from blocks

import breve
import math

from custom.light.source import LightSource
from custom.light.sensor import LightSensor
from custom.proximity.sensor import ProximitySensor
from lib.Activator import BraitenbergActivator

def leftActivator(leftProxSensor, rightProxSensor):
	return 5 - leftProxSensor*rightProxSensor*5

def rightActivator(leftProxSensor, rightProxSensor):
	return 5 - leftProxSensor*rightProxSensor*5

def frontActivator(leftProxSensor, rightProxSensor):
	return leftProxSensor*10 - rightProxSensor*10

class AggressorController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		N = 10
		R = 5
		D = 3
		for i in range(N):
			light = breve.createInstances(breve.LightSource, 1, 1.0, breve.vector(1,0,0))
			light.move(breve.vector((R-D+i%2*D*2)*math.cos(i*2*math.pi/10), 1, (R-D+i%2*D*2)*math.sin(i*2*math.pi/10)))

		self.vehicle = breve.createInstances(breve.BraitenbergVehicle, 1, breve.vector(10, 1, 1))
		self.watch(self.vehicle)

		self.vehicle.move(breve.vector(-40, 2, 20))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.4)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.4)
		self.frontWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.4, 0.4)

		self.vehicle.addWheel(self.leftWheel, breve.vector(-5, 0, -1.500000), breve.vector(0,0,1))
		self.vehicle.addWheel(self.rightWheel, breve.vector(-5, 0, 1.500000), breve.vector(0,0,1))
		self.vehicle.addWheel(self.frontWheel, breve.vector(+5, -0.3, 0), breve.vector(1,0,0))

		self.rightProxSensor = breve.createInstances(LightSensor, 1, 'rightProxSensor', math.pi,breve.vector(1,0,0))
		self.leftProxSensor = breve.createInstances(LightSensor, 1, 'leftProxSensor', math.pi, breve.vector(1,0,0))

		self.vehicle.addSensor(self.rightProxSensor, breve.vector(5, 0.2, .5), breve.vector(0,0,1))
		self.vehicle.addSensor(self.leftProxSensor,  breve.vector(5, 0.2,-.5), breve.vector(0,0,-1))

		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.rightProxSensor, self.leftProxSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.rightProxSensor, self.leftProxSensor], rightActivator)
		self.frontActivator = BraitenbergActivator(self.frontWheel, [self.rightProxSensor, self.leftProxSensor], frontActivator)

breve.AggressorController = AggressorController

# Create an instance of our controller object to initialize the simulation

AggressorController()
