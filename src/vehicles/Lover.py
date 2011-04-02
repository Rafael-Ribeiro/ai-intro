#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-
# Light aggressor

import sys
sys.path.append("../") 

import breve
import math

from custom.light.source import LightSource
from custom.light.sensor import LightSensor
from lib.Activator import BraitenbergActivator

VELOCITY = 2.0 	# Natural velocity
BIAS = 10.0		# Try to maintain a 10 meter distance

def leftActivator(vehicle, leftLightSensor):
	return VELOCITY - leftLightSensor*(2*VELOCITY)

def rightActivator(vehicle, rightLightSensor):
	return VELOCITY - rightLightSensor*(2*VELOCITY)

class LoverController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		light = breve.createInstances(breve.LightSource, 1, 1.0, breve.vector(0,1,0))
		light.move(breve.vector(20, 1, 10))
		self.vehicle = breve.createInstances(breve.BraitenbergVehicle, 1, breve.vector(4, 0.7, 3))
		self.watch(self.vehicle)

		self.vehicle.move(breve.vector(0, 2, 0))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
	
		self.vehicle.addWheel(self.leftWheel, breve.vector(-0.500000, 0, -1.500000))
		self.vehicle.addWheel(self.rightWheel, breve.vector(-0.500000, 0, 1.500000))

		self.rightLightSensor = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2.0, breve.vector(0,1,0), BIAS)
		self.leftLightSensor = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2.0, breve.vector(0,1,0), BIAS)

		self.vehicle.addSensor(self.rightLightSensor, breve.vector(2.0, 0.4, 1.5), breve.vector(1,0,0))
		self.vehicle.addSensor(self.leftLightSensor,  breve.vector(2.0, 0.4,-1.5), breve.vector(1,0,0))

		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.leftLightSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.rightLightSensor], rightActivator)


# Create an instance of our controller object to initialize the simulation

LoverController()
