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
from custom.functions import cut, greater

VELOCITY = 10.0 	# Natural velocity
BIAS = 2.0			# Try to maintain a 2 meter distance
D = 3.0				# Distance between spheres 

def leftActivator(rightProximitySensor, leftSmellSensor, rightSmellSensor):
#	print leftSmellSensor, rightSmellSensor
	return VELOCITY - rightProximitySensor*(2*VELOCITY) + greater(leftSmellSensor, rightSmellSensor, 1.0, 0.0)*VELOCITY

def rightActivator(leftProximitySensor, rightSmellSensor, leftSmellSensor):
	return VELOCITY - leftProximitySensor*(2*VELOCITY) + greater(rightSmellSensor, leftSmellSensor, 1.0, 0.0)*VELOCITY

def piss(rightProximitySensor, leftProximitySensor, rightSmellSensor, leftSmellSensor):
	return (rightSmellSensor + leftSmellSensor < 1) and (abs(2*rightProximitySensor+leftSmellSensor-1) < 0.05 and abs(2*leftProximitySensor+rightSmellSensor - 1) < 0.05)

class Penis(object):
	def __init__(self, tip, sensors, fn):
		self.tip = tip

		self.sensors = {}
		self.activationFunction = fn

		for sensor in sensors:
			sensor.link(self)
			self.sensors[sensor.getName()] = 1

	def activate(self, value, sensor):
		self.sensors[sensor.getName()] = value
		if (self.activationFunction(**self.sensors)):
			print "Pissing!"
			breve.createInstances(SmellSource, 1, 1.0, breve.vector(1,1,0)).move(self.tip.getLocation())

class ExplorerVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(4, 0.7, 3))
	
		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.tip = breve.createInstances(breve.BraitenbergWheel, 1, 0.1, 0.1)

		self.addWheel(self.leftWheel, breve.vector(-0.5, 0, -1.500000))
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0, 1.500000))
		self.addWheel(self.tip, breve.vector(3, -0.1, -2.0))

		self.rightProximitySensor = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/2.0, [SphereMobile], BIAS)
		self.leftProximitySensor = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/2.0, [SphereMobile], BIAS)

		self.rightSmellSensor = breve.createInstances(SmellSensor, 1, 'rightSmellSensor', breve.vector(1,1,0), BIAS*2)
		self.leftSmellSensor = breve.createInstances(SmellSensor, 1, 'leftSmellSensor', breve.vector(1,1,0), BIAS*2)

		self.addSensor(self.rightProximitySensor, breve.vector(2.0, 0.4, 1.5), breve.vector(1,0,0))
		self.addSensor(self.leftProximitySensor,  breve.vector(2.0, 0.4,-1.5), breve.vector(1,0,0))

		self.addSensor(self.rightSmellSensor, breve.vector(2.0, 0.4, 1.5), breve.vector(1,0,0))
		self.addSensor(self.leftSmellSensor,  breve.vector(2.0, 0.4,-1.5), breve.vector(1,0,0))

		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.rightProximitySensor, self.leftSmellSensor, self.rightSmellSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftProximitySensor, self.rightSmellSensor, self.leftSmellSensor], rightActivator)
		self.penis = Penis(self.tip, [self.rightProximitySensor, self.leftProximitySensor, self.rightSmellSensor, self.leftSmellSensor], piss)

class ExplorerController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		self.vehicle = breve.createInstances(ExplorerVehicle, 1)
		self.watch(self.vehicle)

		f = open('trap', 'r')
		lines = f.readlines()
		for i in xrange(len(lines)):
			for j in xrange(len(lines[i])):
				if lines[i][j] == '*':
					breve.createInstances(SphereMobile, 1, 1.0).move(breve.vector(i*D, 1.0, j*D))
				if lines[i][j] == 'X':
					self.vehicle.move(breve.vector(i*D, 2, j*D))
		f.close()

ExplorerController()
