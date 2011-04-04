#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.proximity.sensor import ProximitySensor
from custom.proximity.obstacles import SphereMobile
from lib.Activator import BraitenbergActivator
from custom.constants import direction as dir

ANGULAR = 0.5
AXIS_DIST = 4.0
RADIUS = 10.0

drawing = None
lastLocation = None

def draw(vehicle):
	global drawing,lastLocation
	drawing.drawLine(lastLocation,vehicle.getLocation())
	lastLocation = vehicle.getLocation()


def leftActivator(vehicle, leftSensor, rightSensor):
	draw(vehicle)
	# tangent velocity @ left wheel
	return RADIUS*leftSensor*ANGULAR + (RADIUS+AXIS_DIST)*rightSensor*ANGULAR

def rightActivator(vehicle, leftSensor, rightSensor):
	# tangent velocity @ right wheel
	return (RADIUS+AXIS_DIST)*leftSensor*ANGULAR + RADIUS*rightSensor*ANGULAR

class EightVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(7, 1, 4))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.5, 0.5)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.5)

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  2), breve.vector(0, 0, 1))

		self.leftSensor  = breve.createInstances(ProximitySensor, 1, 'leftSensor', math.pi/3, [SphereMobile])
		self.rightSensor  = breve.createInstances(ProximitySensor, 1, 'rightSensor', math.pi/3, [SphereMobile])
		
		self.addSensor(self.leftSensor,  breve.vector(3.5, 0.3, -2), breve.vector(0, 0, -1))
		self.addSensor(self.rightSensor,  breve.vector(3.5, 0.3, 2), breve.vector(0, 0, 1))
		
		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.leftSensor, self.rightSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftSensor, self.rightSensor], rightActivator)

class OrbitController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		# environment
		z = 1.3*RADIUS
		self.blocks = breve.createInstances(SphereMobile, 2)
		self.blocks[0].move(breve.vector(0, 2, z))
		self.blocks[1].move(breve.vector(0, 2, -z))

		self.vehicle = breve.createInstances(EightVehicle, 1)
		self.vehicle.move(breve.vector(0, 2, z+RADIUS+AXIS_DIST/2.0))
		#self.watch(self.vehicle)
		self.setCameraOffset(dir.UP*150)

		global drawing,lastLocation
		drawing = breve.createInstances(breve.Drawing, 1)
		lastLocation = self.vehicle.getLocation()

orbit = OrbitController()
