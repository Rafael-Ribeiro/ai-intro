#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import breve
import math

from custom.proximity.sensor import ProximitySensor
from lib.Activator import BraitenbergActivator

def actFn(middleSensor):
	if middleSensor == float("infinity"):
		return 0

	return max(0, middleSensor-2) # try to maintain a 2 metter distance

class AggressorController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		self.block = breve.createInstances(breve.Mobile, 1)
		self.blockShape = breve.createInstances(breve.Cube, 1).initWith(breve.vector(1.0,1.0,10.0))
		self.block.setShape(self.blockShape)
		self.block.move(breve.vector(10, 1, 0))
		self.block.setRotation(breve.vector(0, 1, 0), math.pi/2)

		self.vehicle = breve.createInstances(breve.BraitenbergVehicle, 1, breve.vector(4, 0.7, 3))
		self.watch(self.vehicle)

		self.vehicle.move(breve.vector(0, 1, 0))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.1)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.1)
	
		self.vehicle.addWheel(self.leftWheel, breve.vector(-0.500000, 0, -1.500000))
		self.vehicle.addWheel(self.rightWheel, breve.vector(-0.500000, 0, 1.500000))

		self.middleSensor = breve.createInstances(ProximitySensor, 1, 'middleSensor', math.pi/4)
		self.vehicle.addSensor(self.middleSensor, breve.vector(2.2, 0.4, 0), breve.vector(1, 0, 0))

		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.middleSensor], actFn)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.middleSensor], actFn)

breve.AggressorController = AggressorController

# Create an instance of our controller object to initialize the simulation

AggressorController()
