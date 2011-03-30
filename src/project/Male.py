#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.proximity.sensor import ProximitySensor
from custom.proximity.obstacles import SphereMobile

from custom.smell.source import SmellSource

from lib.Activator import BraitenbergActivator

MATURITY = 60.0
PROCRIATION = 30.0
LIFESPAN = 300.0

def leftActivator(leftSensor, rightSensor):
	return 1

def rightActivator(leftSensor, rightSensor):
	return 1

class MaleVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		self.age = 0.0
		self.last = 0.0

		breve.BraitenbergVehicle.__init__(self, breve.vector(7, 1, 4))
		self.setColor(breve.vector(1, 0, 0.0))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.5, 0.5, breve.vector(0,0,0))
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.5, breve.vector(0,0,0))

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  2), breve.vector(0, 0, 1))

		self.leftSensor  = breve.createInstances(ProximitySensor, 1, 'leftSensor', math.pi/3, [SphereMobile])
		self.rightSensor  = breve.createInstances(ProximitySensor, 1, 'rightSensor', math.pi/3, [SphereMobile])
		
		self.addSensor(self.leftSensor,  breve.vector(3.5, 0.3, -2), breve.vector(0, 0, -1))
		self.addSensor(self.rightSensor,  breve.vector(3.5, 0.3, 2), breve.vector(0, 0, 1))
		
		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.leftSensor, self.rightSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftSensor, self.rightSensor], rightActivator)

		self.hormone = breve.createInstances(SmellSource, 1, 0.0, breve.vector(1, 0.0, 0), True)
		self.attach(self.hormone, breve.vector(-3.5,0.5,0))

	def iterate(self):
		self.age = self.getAge()

		if self.age >= LIFESPAN:
			self.destroy()

		tired = 1 - min(1.0, (self.age-self.last)/PROCRIATION)
		mature = min(1.0, self.age/MATURITY)

		self.hormone.setIntensity(mature - tired)
