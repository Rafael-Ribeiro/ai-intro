#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from lib.Activator import BraitenbergActivator

from custom.proximity.obstacles import SphereMobile

from custom.proximity.sensor import DistanceSensor
from custom.proximity.sensor import LaserSensor

from custom.functions import greater, limit, negexp
from custom.constants import color, direction as dir

# http://en.wikipedia.org/wiki/Angular_frequency
DISTANCE = 20.0
RADIUS = 13.0
VELOCITY = 5.0
ANGULAR_FREQUENCY = VELOCITY / RADIUS

AXIS_DIST = 4.0

drawing = None
lastLocation = None

def draw(vehicle):
	global drawing,lastLocation
	drawing.drawLine(lastLocation,vehicle.getLocation())
	lastLocation = vehicle.getLocation()

def leftActivator(vehicle, distanceSensor,laserSensor):
	# TODO REMOVE
	draw(vehicle)
	#/ TODO REMOVE
	return VELOCITY

def rightActivator(vehicle, distanceSensor,laserSensor):
	OFFSET = 0.6 #4/math.sqrt(distanceSensor)
	DIFFERENTIAL = ANGULAR_FREQUENCY * AXIS_DIST

	a = greater(laserSensor, 0, 0, OFFSET)
	b = greater(distanceSensor, RADIUS*2, 0, DIFFERENTIAL)

	return VELOCITY + limit(a + b, 0, DIFFERENTIAL)

class EllipseVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(4, 1, 4))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.2, 0.5)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.2, 0.5)

		self.addWheel(self.leftWheel,  breve.vector(0, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(0, 0,  2), breve.vector(0, 0, 1))

		# Stabilizers
		self.attach(breve.createInstances(breve.Stabilizer,1,0.3),breve.vector(-2,-0.9,0))
		self.attach(breve.createInstances(breve.Stabilizer,1,0.3),breve.vector(2,-0.9,0))

		self.distanceSensor  = breve.createInstances(DistanceSensor, 1, 'distanceSensor', math.pi, [SphereMobile])
		self.laserSensor  = breve.createInstances(LaserSensor, 1, 'laserSensor', math.pi/20, [SphereMobile])

		self.addSensor(self.distanceSensor,  breve.vector(0, 0, 0), dir.FRONT)
		self.addSensor(self.laserSensor,  breve.vector(0, 0, 0), dir.FRONT)

		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.distanceSensor, self.laserSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.distanceSensor, self.laserSensor], rightActivator)

class EllipseController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		DISTANCEX = DISTANCE + RADIUS*2
		self.lights = breve.createInstances(SphereMobile, 2, 1.0)
		self.lights[0].move(breve.vector(0, 1.2, DISTANCEX))
		self.lights[1].move(breve.vector(0, 1.2, -DISTANCEX))

		self.vehicle = breve.createInstances(EllipseVehicle, 1).move(breve.vector(RADIUS,1, 0))

		self.vehicle.rotate(dir.UP, math.pi/2)

		self.setCameraOffset(dir.UP*200)

		global drawing,lastLocation
		drawing = breve.createInstances(breve.Drawing, 1)
		lastLocation = self.vehicle.getLocation()

ellipse = EllipseController()
