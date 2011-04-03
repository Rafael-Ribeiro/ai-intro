#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.proximity.obstacles import SphereMobile
from custom.proximity.sensor import DistanceSensor
from custom.functions import gaussian, limit, negexp
from lib.Activator import BraitenbergActivator
from custom.constants import color, direction as dir

from custom.smell.sensor import SmellSensor

# http://en.wikipedia.org/wiki/Angular_frequency
DISTANCE = 35.0
RADIUS = 10.0
VELOCITY = 5.0
ANGULAR_FREQUENCY = VELOCITY / RADIUS

AXIS_DIST = 4.0

def leftActivator(self, distanceSensor):
	return VELOCITY

def rightActivator(self, distanceSensor):
	if distanceSensor >= RADIUS*2:
		return VELOCITY
	else:
		return VELOCITY + ANGULAR_FREQUENCY * AXIS_DIST
	#return VELOCITY + VELOCITY*gaussian(distanceSensor, 5, 2.0)

class ElipseVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(7, 1, 4))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.2, 0.5)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.2, 0.5)

		self.addWheel(self.leftWheel,  breve.vector(2, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(2, 0,  2), breve.vector(0, 0, 1))
		self.attach(breve.createInstances(SmellSensor,1,'smell',color.RED,5.0),breve.vector(-3.5,-0.5,0))

		self.distanceSensor  = breve.createInstances(DistanceSensor, 1, 'distanceSensor', math.pi, [SphereMobile])

		self.addSensor(self.distanceSensor,  breve.vector(2, 0, 0), breve.vector(1, 0, 0))

		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.distanceSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.distanceSensor], rightActivator)

class ElipseController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		DISTANCEX = DISTANCE + RADIUS*2
		self.lights = breve.createInstances(SphereMobile, 2, 1.0)
		self.lights[0].move(breve.vector(0, 1.2, DISTANCEX))
		self.lights[1].move(breve.vector(0, 1.2, -DISTANCEX))

		self.vehicle = breve.createInstances(ElipseVehicle, 1).move(breve.vector(RADIUS,1, DISTANCE))

		self.vehicle.rotate(dir.UP, math.pi/2)
		self.watch(self.vehicle)

elipse = ElipseController()
