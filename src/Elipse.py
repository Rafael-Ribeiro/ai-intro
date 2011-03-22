#!/usr/share/breve/bin/breve

import math
import breve

from custom.proximity.sensor import ProximitySensor
from lib.Activator import BraitenbergActivator

DEFAULT_SPEED = 2.0
AXIS_DIST = 4.0
A_DIST = 10.0
B_DIST = 7.0
EXCENTRICITY = math.sqrt(1-(B_DIST/A_DIST)**2)
F_DIST = A_DIST*EXCENTRICITY
BIAS = math.sqrt(F_DIST**2+B_DIST**2)

def angularSpeed(intensity):
	return (max(intensity-0.5, 0))*4*math.pi*EXCENTRICITY

def leftActivator(leftSensor):
	# tangent velocity @ left wheel
	return DEFAULT_SPEED

def rightActivator(leftSensor):
	# tangent velocity @ right wheel
	return DEFAULT_SPEED + AXIS_DIST*angularSpeed(leftSensor)

class SphereMobile(breve.Mobile):
	def __init__(self):
		breve.Mobile.__init__(self)
		self.shape = breve.createInstances(breve.Sphere, 1)
		self.shape.initWith(1.0)
		self.setShape(self.shape)

class ElipseVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(7, 1, 4))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.5, 0.5)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.5)

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  2), breve.vector(0, 0, 1))

		self.leftSensor  = breve.createInstances(ProximitySensor, 1, 'leftSensor', math.pi/2, [SphereMobile], BIAS)
		
		self.addSensor(self.leftSensor,  breve.vector(-0.5, 0, -2.5), breve.vector(0, 0, -1))
		
		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.leftSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftSensor], rightActivator)

class OrbitController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		# environment
		z = 1.5*A_DIST
		self.blocks = breve.createInstances(SphereMobile, 2)
		self.blocks[0].move(breve.vector(0, 2, z))
		self.blocks[1].move(breve.vector(0, 2, -z))

		self.vehicle = breve.createInstances(ElipseVehicle, 1)
		self.vehicle.move(breve.vector(0, 2, z+A_DIST+AXIS_DIST/2.0))
		self.watch(self.vehicle)

orbit = OrbitController()
