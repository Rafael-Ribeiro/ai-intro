#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-
# Proximity aggressor

import sys
sys.path.append("../") 

import breve
import math

from custom.proximity.obstacles import SphereMobile
from custom.proximity.sensor import ProximitySensor
from custom.smell.source import SmellSource
from custom.smell.sensor import SmellSensor
from lib.Activator import BraitenbergActivator
from custom.functions import cut, greater, hiperbole

VELOCITY = 10.0	 	# Natural velocity
BIAS = 2.0			# Try to maintain a 2 meter distance
D = 3.0				# Distance between spheres

def leftActivator(vehicle, rightProximitySensor):
#	a = 1 - rightProximitySensor*2
#	b = 1 - leftProximitySensor*2

#	if (abs(a+b) < 0.1):
#		return 2*VELOCITY

	a = cut(rightProximitySensor, 1-rightProximitySensor*2, 0.5, 1)
	return VELOCITY*a

def rightActivator(vehicle, leftProximitySensor):
#	a = 1 - leftProximitySensor*2
#	b = 1 - rightProximitySensor*2

#	if (abs(a+b) < 0.1):
#		return -2*VELOCITY

	a = cut(leftProximitySensor, 1-leftProximitySensor*2, 0.5, -1)   
	return VELOCITY*a

class ExplorerVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(3, 0.7, 3))
	
		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.addWheel(self.leftWheel, breve.vector(-0, 0, -1.500000))
		self.addWheel(self.rightWheel, breve.vector(-0, 0, 1.500000))

		self.leftProximitySensor = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/2.0, [SphereMobile], BIAS)
		self.rightProximitySensor = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/2.0, [SphereMobile], BIAS)

		self.addSensor(self.leftProximitySensor,  breve.vector(1.5, 0.4,-1.5), breve.vector(1,0,0))
		self.addSensor(self.rightProximitySensor, breve.vector(1.5, 0.4, 1.5), breve.vector(1,0,0))

		self.leftActivator = BraitenbergActivator(self ,self.leftWheel, [self.rightProximitySensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftProximitySensor], rightActivator)

class ExplorerController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		self.vehicle = breve.createInstances(ExplorerVehicle, 1)
		self.watch(self.vehicle)

		f = open('maps/road', 'r')
		lines = f.readlines()
		for i in xrange(len(lines)):
			for j in xrange(len(lines[i])):
				if lines[i][j] == '*':
					breve.createInstances(SphereMobile, 1, 1.0, True).move(breve.vector(i*D, 1.0, j*D))
				if lines[i][j] == 'X':
					self.vehicle.move(breve.vector(i*D, 2, j*D))
		f.close()

ExplorerController()
