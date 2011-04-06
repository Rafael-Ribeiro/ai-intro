#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-
# Proximity aggressor

import sys
sys.path.append("../") 

import breve
import math

from custom.proximity.obstacles import SphereStationary
from custom.proximity.sensor import ProximitySensor
from custom.light.source import LightSource
from custom.light.sensor import LightSensor
from lib.Activator import BraitenbergActivator

from custom.functions import *
from custom.constants import direction as d, color

VELOCITY = 10.0 			# Natural velocity
HALF_DISTANCE = 3.0			# Try to maintain at least 3 meter distance
HALF_LIGHT = 5.0			# Behaviour change at 5 meters
D = 3.0						# Distance between spheres

def leftActivator(vehicle, rightProximitySensor, leftProximitySensor, rightLightSensor):
	#a = 1 - rightProximitySensor*2
	#b = 1 - leftProximitySensor*2

	#if (abs(a+b) < 0.1):
	#	return 2*VELOCITY

	a = cut(rightProximitySensor, 1-rightProximitySensor*2, 0.45, -1)
	b = cut(rightLightSensor, gaussian(rightLightSensor, 0.25, 0.1)/2-0.02, 0.5, -(1-rightLightSensor*2)**2)

	return VELOCITY*(a+b)

def rightActivator(vehicle, leftProximitySensor, rightProximitySensor, leftLightSensor):
	#a = 1 - leftProximitySensor*2
	#b = 1 - rightProximitySensor*2

	#if (abs(a+b) < 0.1):
	#	return -2*VELOCITY

	a = cut(leftProximitySensor, 1-leftProximitySensor*2, 0.45, 1)
	b = cut(leftLightSensor, gaussian(leftLightSensor, 0.25, 0.1)/2-0.02, 0.5, -(1-leftLightSensor*2)**2)

	return VELOCITY*(a+b)

class ExplorerVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(3, 0.7, 3))
	
		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.addWheel(self.leftWheel, breve.vector(-0, 0, -1.500000))
		self.addWheel(self.rightWheel, breve.vector(-0, 0, 1.500000))

		# Proximity
		self.leftProximitySensor = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/4.0, [SphereStationary], HALF_DISTANCE)
		self.rightProximitySensor = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/4.0, [SphereStationary], HALF_DISTANCE)

		self.addSensor(self.leftProximitySensor,  breve.vector(1.5, 0.4,-1.5), breve.vector(1,0,0))
		self.addSensor(self.rightProximitySensor, breve.vector(1.5, 0.4, 1.5), breve.vector(1,0,0))

		# Light
		self.leftLightSensor = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2.0, color.RED, HALF_LIGHT)
		self.rightLightSensor = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2.0, color.RED, HALF_LIGHT)

		self.addSensor(self.leftLightSensor,  breve.vector(1.5, 0.4,-1.5), breve.vector(1,0,0))
		self.addSensor(self.rightLightSensor, breve.vector(1.5, 0.4, 1.5), breve.vector(1,0,0))


		self.leftActivator = BraitenbergActivator(self ,self.leftWheel, [self.rightProximitySensor, self.leftProximitySensor, self.rightLightSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftProximitySensor, self.rightProximitySensor, self.leftLightSensor], rightActivator)

class ExplorerController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		self.vehicle = breve.createInstances(ExplorerVehicle, 1)
		self.watch(self.vehicle)

		f = open('maps/labirynth', 'r')
		lines = f.readlines()
		for i in xrange(len(lines)):
			for j in xrange(len(lines[i])):
				pos = breve.vector(i*D, 1.0, j*D)

				if lines[i][j] == '*':
					breve.createInstances(SphereStationary, 1, 1.0).move(pos)
				if lines[i][j] == 'o':
					breve.createInstances(LightSource, 1, 1.0, color.RED).move(pos)
				if lines[i][j] == 'X':
					self.vehicle.move(pos)
		f.close()

ExplorerController()
