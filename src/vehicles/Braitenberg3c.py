#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

# Braitenberg 3c vehicle:

#	Sensor Pair	|	Connection	|	Bias		|	Behaviour					|	Color	#
#---------------+---------------+---------------+-------------------------------+-----------#
#	Proximity	|	Crossed		|	Negative	|	Explorer of objects			|	White	#
#	Sound		|	Uncrossed	|	Positive	|	Coward towards sound		|	Black	#
#	Smell		|	Crossed		|	Positive	|	Aggressor towards smell		|	Red		#
#	Light		|	Crossed		|	Negative	|	Explorer of light			|	Green	#

import sys
sys.path.append("../") 

import breve
import math

from custom.proximity.sensor import ProximitySensor
from custom.proximity.obstacles import SphereStationary

from custom.sound.sensor import SoundSensor
from custom.sound.source import SoundSource

from custom.smell.sensor import SmellSensor
from custom.smell.source import SmellSource

from custom.light.sensor import LightSensor
from custom.light.source import LightSource

from lib.Activator import BraitenbergActivator

from custom.constants import color,direction as dir
from custom.functions import *

#Simulation constants
VELOCITY = 5.0 			# Natural velocity
D = 3.0 				# distance between objects on the grid

# Distance where the intensity of the sensor is 0.5
HALF_LIGHT = 3.0
HALF_SMELL = 4.0
HALF_SOUND = 4.0
HALF_PROXIMITY = 3.0

# Senses factors
LIGHT_BIAS = 2.0
SMELL_BIAS = 4.0
SOUND_BIAS = 5.0
PROXIMITY_BIAS = 2.0

#Sensor/Source types
LIGHT_TYPE = color.GREEN
SMELL_TYPE = color.RED
SOUND_TYPE = color.BLACK
PROXIMITY_TYPES = [SphereStationary]

NATURAL = 2.0
C = 0.2
CSOUND = 0.3
def leftActivator(vehicle, rightLightSensor, rightProximitySensor,rightSmellSensor,leftSoundSensor):
	a = cut(rightProximitySensor, 0, C, (C-rightProximitySensor)*PROXIMITY_BIAS, 0.5, (NATURAL-1)) # 
	b = cut(rightLightSensor, 0, C, (C-rightLightSensor)*LIGHT_BIAS, 0.5, -(NATURAL+1))
	c = cut(rightSmellSensor, 0, C, (rightSmellSensor-C)*SMELL_BIAS)
	d = cut(leftSoundSensor, 0, CSOUND, (leftSoundSensor-CSOUND)*SOUND_BIAS)

	return VELOCITY*(a + b + c + d + NATURAL)

def rightActivator(vehicle, leftLightSensor, leftProximitySensor,leftSmellSensor,rightSoundSensor):
	a = cut(leftProximitySensor, 0, C, (C-leftProximitySensor)*PROXIMITY_BIAS, 0.5, -(NATURAL+1))
	b = cut(leftLightSensor, 0, C, (C-leftLightSensor)*LIGHT_BIAS, 0.5, (NATURAL-1))
	c = cut(leftSmellSensor, 0, C, (leftSmellSensor-C)*SMELL_BIAS)
	d = cut(rightSoundSensor, 0, CSOUND, (rightSoundSensor-CSOUND)*SOUND_BIAS)

	return VELOCITY*(a + b + c + d + NATURAL)

class Braitenberg3cVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(3, 0.7, 3))

		#Wheels
		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
	
		self.addWheel(self.leftWheel, breve.vector(0, 0, -1.500000))
		self.addWheel(self.rightWheel, breve.vector(0, 0, 1.500000))

		# Sensors #
		# Light sensors
		self.leftLightSensor = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2.0, LIGHT_TYPE, HALF_LIGHT)
		self.rightLightSensor = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2.0, LIGHT_TYPE, HALF_LIGHT)

		self.addSensor(self.leftLightSensor,  breve.vector(1.30, 0.2,-1.1), dir.FRONT)
		self.addSensor(self.rightLightSensor, breve.vector(1.30, 0.2, 1.1), dir.FRONT)

		#Proximity sensors
		self.leftProximitySensor = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/2.0, PROXIMITY_TYPES, HALF_PROXIMITY)
		self.rightProximitySensor = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/2.0, PROXIMITY_TYPES, HALF_PROXIMITY)

		self.addSensor(self.leftProximitySensor,  breve.vector(1.5, 0.2,-1.1), dir.FRONT)
		self.addSensor(self.rightProximitySensor, breve.vector(1.5, 0.2, 1.1), dir.FRONT)

		#Smell sensors
		self.leftSmellSensor = breve.createInstances(SmellSensor, 1, 'leftSmellSensor', SMELL_TYPE, HALF_SMELL)
		self.rightSmellSensor = breve.createInstances(SmellSensor, 1, 'rightSmellSensor', SMELL_TYPE, HALF_SMELL)

		self.addSensor(self.leftSmellSensor,  breve.vector(1.5, -0.125,-1.1), dir.FRONT)
		self.addSensor(self.rightSmellSensor, breve.vector(1.5, -0.125, 1.1), dir.FRONT)

		#Sound sensors
		self.leftSoundSensor = breve.createInstances(SoundSensor, 1, 'leftSoundSensor', SOUND_TYPE, HALF_SOUND, SoundSensor.LEFT_BALANCE)
		self.rightSoundSensor = breve.createInstances(SoundSensor, 1, 'rightSoundSensor', SOUND_TYPE, HALF_SOUND, SoundSensor.RIGHT_BALANCE)

		self.addSensor(self.leftSoundSensor,  breve.vector(1.0, 0,-1.5), dir.LEFT)
		self.addSensor(self.rightSoundSensor, breve.vector(1.0, 0, 1.5), dir.RIGHT)

		#Activators
		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.rightLightSensor,self.rightProximitySensor,self.rightSmellSensor,self.leftSoundSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftLightSensor,self.leftProximitySensor,self.leftSmellSensor,self.rightSoundSensor], rightActivator)


class Braitenberg3cController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		self.vehicle = breve.createInstances(Braitenberg3cVehicle, 1).move(breve.vector(0, 2, 0))
		self.watch(self.vehicle)

		#Scenario
		f = open('maps/braitenberg3c', 'r')
		lines = f.readlines()
		for i in xrange(len(lines)):
			for j in xrange(len(lines[i])):
				if lines[i][j] == '*': #objects
					breve.createInstances(SphereStationary, 1, 1.0).move(breve.vector(i*D, 1.0, j*D))
				elif lines[i][j] == 'l': #<L>ight
					breve.createInstances(LightSource, 1, 1.0, LIGHT_TYPE, False).move(breve.vector(i*D, 1.0, j*D))
				elif lines[i][j] == 's': #<S>mell
					breve.createInstances(SmellSource, 1, 0.2, SMELL_TYPE, False).move(breve.vector(i*D, 1.0, j*D))
				elif lines[i][j] == 'o': #s<O>und
					breve.createInstances(SoundSource, 1, 0.3, SOUND_TYPE, False).move(breve.vector(i*D, 1.0, j*D))
				elif lines[i][j] == 'X': #vehicle
					self.vehicle.move(breve.vector(i*D, 2, j*D))
		f.close()

		self.vehicle.rotate(breve.vector(0,1,0),3*math.pi/4)

Braitenberg3cController()
