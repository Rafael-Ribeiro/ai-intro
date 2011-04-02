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

# http://en.wikipedia.org/wiki/Angular_frequency
RADIUS = 40.0
VELOCITY = 5.0

def leftActivator(self, distanceSensor):
	return VELOCITY - VELOCITY/2*gaussian(distanceSensor, 9.5, 5.0)

def rightActivator(self, distanceSensor):
	return VELOCITY + VELOCITY/2*gaussian(distanceSensor, 9.5, 5.0)

class ElipseVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(7, 1, 4))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.5, 0.5)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.5)

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  2), breve.vector(0, 0, 1))

		self.distanceSensor  = breve.createInstances(DistanceSensor, 1, 'distanceSensor', math.pi, [SphereMobile])
		
		self.addSensor(self.distanceSensor,  breve.vector(-0.5, 1, 0), breve.vector(1, 0, 0))
		
		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.distanceSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.distanceSensor], rightActivator)

class ElipseController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		RADIUSX = RADIUS+10
		self.lights = breve.createInstances(SphereMobile, 2, 1.0)
		self.lights[0].move(breve.vector(0, 1, RADIUSX))
		self.lights[1].move(breve.vector(0, 1, -RADIUSX))
	
		self.vehicle = breve.createInstances(ElipseVehicle, 1)
		self.vehicle.move(breve.vector(0,1, RADIUS))
		#self.vehicle.setRotation(dir.UP, math.pi/2)
		self.watch(self.vehicle)

elipse = ElipseController()
