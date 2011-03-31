#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.proximity.sensor import ProximitySensor
from custom.proximity.obstacles import SphereMobile

from custom.smell.sensor import SmellSensor
from custom.smell.source import SmellSource

from custom.constants import color, direction as dir

from lib.Activator import BraitenbergActivator

MATURITY = 60.0
PROCRIATION = 45.0
LIFESPAN = 300.0
VELOCITY = 10.0

DISTANCE_BIAS = 2.5

def leftActivator(leftProximitySensor, rightProximitySensor):
	a = 1 - rightProximitySensor*2
	b = 1 - leftProximitySensor*2

	if (abs(a+b) < 0.1):
		return 5*VELOCITY

	return VELOCITY*a

def rightActivator(leftProximitySensor, rightProximitySensor):
	a = 1 - rightProximitySensor*2
	b = 1 - leftProximitySensor*2

	if (abs(a+b) < 0.1):
		return -5*VELOCITY

	return VELOCITY*b

class MaleVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(4, 0.7, 3))
		self.setColor(color.RED)

		self.age = 0.0
		self.last = 0.0

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 0.6, 0.2, color.BLACK)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2, color.BLACK)

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -1.5), dir.RIGHT)
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  1.5), dir.RIGHT)

		# Proximity
		self.leftProximitySensor  = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/3, [SphereMobile], DISTANCE_BIAS)
		self.rightProximitySensor  = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/3, [SphereMobile], DISTANCE_BIAS)
		
		self.addSensor(self.leftProximitySensor,  breve.vector(2, 0.21, -1.2), dir.FRONT)
		self.addSensor(self.rightProximitySensor,  breve.vector(2, 0.21, 1.2), dir.FRONT)
		
		# Hormones
		self.leftSmellSensor  = breve.createInstances(SmellSensor, 1, 'leftSmellSensor', color.PINK)
		self.rightSmellSensor  = breve.createInstances(SmellSensor, 1, 'rightSmellSensor', color.PINK)
		
		self.addSensor(self.leftSmellSensor,  breve.vector(2, -0.3, -1.5), dir.FRONT)
		self.addSensor(self.rightSmellSensor,  breve.vector(2, -0.3, 1.5), dir.FRONT)

		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.leftProximitySensor, self.rightProximitySensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftProximitySensor, self.rightProximitySensor], rightActivator)

		self.hormone = breve.createInstances(SmellSource, 1, 0.0, color.RED, True)
		self.attach(self.hormone, breve.vector(-2.5,0.5,0))

	def iterate(self):
		self.age = self.getAge()

		if self.age >= LIFESPAN:
			self.destroy()

		tired = 1 - min(1.0, (self.age-self.last)/PROCRIATION)
		mature = min(1.0, self.age/MATURITY)

		self.hormone.setIntensity(mature - tired)
