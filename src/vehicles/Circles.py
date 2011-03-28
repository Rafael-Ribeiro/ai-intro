#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.proximity.sensor import ProximitySensor
from custom.proximity.obstacles import SphereMobile
from custom.functions import gaussian, limit
from lib.Activator import BraitenbergActivator

# http://en.wikipedia.org/wiki/Angular_frequency
RADIUS = 40.0
VELOCITY = 5.0

ANGULAR_FREQUENCY = VELOCITY/RADIUS

AXIS_DIST = 4.0
BIAS = 1.0

def leftActivator(leftSensor):
	return VELOCITY

def rightActivator(leftSensor):
	return VELOCITY + ANGULAR_FREQUENCY*AXIS_DIST


class CircleVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(7, 1, 4))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.5, 0.5)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.5)

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  2), breve.vector(0, 0, 1))

		self.leftSensor  = breve.createInstances(ProximitySensor, 1, 'leftSensor', math.pi/2, [SphereMobile], BIAS)
		
		self.addSensor(self.leftSensor,  breve.vector(-0.5, 1.5, 0), breve.vector(0, 0, -1))
		
		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.leftSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftSensor], rightActivator)

class OrbitController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		# environment
		self.blocks = breve.createInstances(SphereMobile, 1)
		self.blocks.move(breve.vector(0, 2, 0))

		self.vehicle = breve.createInstances(CircleVehicle, 1)
		self.vehicle.move(breve.vector(0, 2, RADIUS+AXIS_DIST/2))
		self.watch(self.vehicle)

orbit = OrbitController()
