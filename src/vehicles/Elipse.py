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

# TODO
from custom.smell.sensor import SmellSensor

# http://en.wikipedia.org/wiki/Angular_frequency
DISTANCE = 20.0
RADIUS = 13.0
VELOCITY = 5.0
ANGULAR_FREQUENCY = VELOCITY / RADIUS

AXIS_DIST = 4.0

def leftActivator(self, distanceSensor,laserSensor):
	return VELOCITY

def rightActivator(self, distanceSensor,laserSensor):
	#	if distanceSensor > RADIUS*2:
	#		if laserSensor > 0:
	#			# object detected
	#			return VELOCITY
	#		else:
	#			# no object found, correct trajectory
	#			return VELOCITY + 4/math.sqrt(distanceSensor) #inverse quadratic function
	#	else:
	#		return VELOCITY + ANGULAR_FREQUENCY * AXIS_DIST
	return greater(distanceSensor,RADIUS*2,greater(laserSensor,0,VELOCITY,VELOCITY + 4/math.sqrt(distanceSensor)),VELOCITY + ANGULAR_FREQUENCY * AXIS_DIST)

class ElipseVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(4, 1, 4))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.2, 0.5)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.2, 0.5)

		self.addWheel(self.leftWheel,  breve.vector(0, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(0, 0,  2), breve.vector(0, 0, 1))

		#TODO: Class "Stabilizers", since sensors are ugly and wheels don't work
		# since friction causes the vehicle to bump with the ground;
		# however, without them the vehicle is unstable enough to render
		# every single calculation useless
		self.attach(breve.createInstances(SmellSensor,1,'smell',color.RED,5.0),breve.vector(-2,-1.0,0))
		self.attach(breve.createInstances(SmellSensor,1,'smell',color.RED,5.0),breve.vector(2,-1.0,0))

		self.distanceSensor  = breve.createInstances(DistanceSensor, 1, 'distanceSensor', math.pi, [SphereMobile])
		self.laserSensor  = breve.createInstances(LaserSensor, 1, 'laserSensor', math.pi/20, [SphereMobile])

		self.addSensor(self.distanceSensor,  breve.vector(0, 0, 0), dir.FRONT)
		self.addSensor(self.laserSensor,  breve.vector(0, 0, 0), dir.FRONT)

		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.distanceSensor, self.laserSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.distanceSensor, self.laserSensor], rightActivator)

class ElipseController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		DISTANCEX = DISTANCE + RADIUS*2
		self.lights = breve.createInstances(SphereMobile, 2, 1.0)
		self.lights[0].move(breve.vector(0, 1.2, DISTANCEX))
		self.lights[1].move(breve.vector(0, 1.2, -DISTANCEX))

		self.vehicle = breve.createInstances(ElipseVehicle, 1).move(breve.vector(RADIUS,1, 0))

		self.vehicle.rotate(dir.UP, math.pi/2)

		self.setCameraOffset(dir.UP*200)

elipse = ElipseController()
