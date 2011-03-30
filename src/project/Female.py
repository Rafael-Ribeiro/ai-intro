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

def leftActivator(leftProximitySensor, rightProximitySensor):
	return 1

def rightActivator(leftProximitySensor, rightProximitySensor):
	return 1

class FemaleVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(7, 1, 4))
		self.setColor(breve.vector(1, 0.6, 1))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 1.5, 0.5, breve.vector(1,1,1))
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 1.5, 0.5, breve.vector(1,1,1))

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -2), breve.vector(0, 0, 1))
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  2), breve.vector(0, 0, 1))

		self.leftProximitySensor  = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/3, [SphereMobile])
		self.rightProximitySensor  = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/3, [SphereMobile])

		self.addSensor(self.leftProximitySensor,  breve.vector(3.5, 0.3, -2), breve.vector(0, 0, -1))
		self.addSensor(self.rightProximitySensor,  breve.vector(3.5, 0.3, 2), breve.vector(0, 0, 1))

		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.leftProximitySensor, self.rightProximitySensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftProximitySensor, self.rightProximitySensor], rightActivator)

		self.hormone = breve.createInstances(SmellSource, 1, 1.0, breve.vector(1, 0.6,1)) # TODO: modify intensity by time!
		self.attach(self.hormone, breve.vector(-3.5,0.5,0))
