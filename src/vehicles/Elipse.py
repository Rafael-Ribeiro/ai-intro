#!/usr/share/breve/bin/breve

import math
import breve

from custom.proximity.sensor import DistanceSensor
from custom.functions import gaussian, limit
from lib.Activator import BraitenbergActivator

# http://en.wikipedia.org/wiki/Angular_frequency
RADIUS_A = 40.0
RADIUS_B = 20.0
RADIUS_F = math.sqrt(RADIUS_A**2 - RADIUS_B**2)
VELOCITY = 1.0

ANGULAR_FREQUENCY = VELOCITY/RADIUS_A

AXIS_DIST = 4.0
BIAS = 10

def angularFrequency(sensor): # rad/s
	return # will this work? math.arccot(max(0, sensor - (RADIUS_F - RADIUS_A)))

def leftActivator(leftSensor):
	return VELOCITY

def rightActivator(leftSensor):
	return VELOCITY + angularFrequency(leftSensor)*AXIS_DIST

class SphereMobile(breve.Mobile):
	def __init__(self):
		breve.Mobile.__init__(self)
		self.shape = breve.createInstances(breve.Sphere, 1)
		self.shape.initWith(1.0)
		self.setShape(self.shape)

class ElipseVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(7, 1, 4))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.5, 0.7)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.7)

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  2), breve.vector(0, 0, 1))

		self.leftSensor  = breve.createInstances(DistanceSensor, 1, 'leftSensor', math.pi/4, [SphereMobile])
		
		self.addSensor(self.leftSensor,  breve.vector(-0.5, 1.5, 0), breve.vector(0, 0, -1))
		
		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.leftSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftSensor], rightActivator)

class OrbitController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		# environment
		self.lights = breve.createInstances(LightSource, 2, 1.0, breve.vector(0,1,0))
		self.lights[0].move(breve.vector(0, 2.5, RADIUS_F))
		self.lights[1].move(breve.vector(0, 2.5, -RADIUS_F))

		self.vehicle = breve.createInstances(ElipseVehicle, 1)
		self.vehicle.move(breve.vector(0, 2, RADIUS_A+AXIS_DIST/2))
		self.watch(self.vehicle)

orbit = OrbitController()
