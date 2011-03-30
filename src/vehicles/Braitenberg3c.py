#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

# Braitenberg 3c vehicle:

#	Sensor Pair	|	Connection	|	Bias		|	Behaviour					#
#---------------+---------------+---------------+-------------------------------#
#	Light		|	Crossed		|	Negative	|	Explorer of light			#
#	Proximity	|	Crossed		|	Negative	|	Explorer of objects			#
#	Smell		|	Crossed		|	Positive	|	Aggressor towards smell		#
#	Sound		|	Uncrossed	|	Positive	|	Coward towards sound		#

import sys
sys.path.append("../") 

import breve
import math

from custom.light.sensor import LightSensor
from custom.light.source import LightSource

from custom.proximity.sensor import ProximitySensor

from custom.smell.sensor import SmellSensor
from custom.smell.source import SmellSource

from custom.sound.sensor import SoundSensor
from custom.sound.source import SoundSource

from lib.Activator import BraitenbergActivator

from custom.constants import direction as dir

VELOCITY = 0.0 	# Natural velocity

#Sensors' bias
LIGHT_BIAS = 5.0
PROXIMITY_BIAS = 5.0
SMELL_BIAS = 3.5
SOUND_BIAS = 5.0

#Sensors' factors
LIGHT_FACTOR = 5.0
PROXIMITY_FACTOR = 5.0
SMELL_FACTOR = 20.0
SOUND_FACTOR = 5.0

#Sensor/Source types
LEFT_LIGHT_TYPE = breve.vector(0,1,0)
RIGHT_LIGHT_TYPE = LEFT_LIGHT_TYPE

LEFT_PROXIMITY_TYPES = []
RIGHT_PROXIMITY_TYPES = LEFT_PROXIMITY_TYPES

LEFT_SMELL_TYPE = breve.vector(1,0,0)
RIGHT_SMELL_TYPE = LEFT_SMELL_TYPE

LEFT_SOUND_TYPE = breve.vector(0,0,0)
RIGHT_SOUND_TYPE = LEFT_SOUND_TYPE


def leftActivator(rightLightSensor,rightProximitySensor,rightSmellSensor,leftSoundSensor):
	return VELOCITY - rightLightSensor*LIGHT_FACTOR - rightProximitySensor*PROXIMITY_FACTOR + rightSmellSensor*SMELL_FACTOR + leftSoundSensor*SOUND_FACTOR

def rightActivator(leftLightSensor,leftProximitySensor,leftSmellSensor,rightSoundSensor):
	return VELOCITY - leftLightSensor*LIGHT_FACTOR - leftProximitySensor*PROXIMITY_FACTOR + leftSmellSensor*SMELL_FACTOR + rightSoundSensor*SOUND_FACTOR

class Braitenberg3cVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(4, 0.7, 3))

		#Wheels
		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
	
		self.addWheel(self.leftWheel, breve.vector(-0.500000, 0, -1.500000))
		self.addWheel(self.rightWheel, breve.vector(-0.500000, 0, 1.500000))

		# Sensors #
		#Light sensors
		self.leftLightSensor = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2.0, LEFT_LIGHT_TYPE, LIGHT_BIAS)
		self.rightLightSensor = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2.0, RIGHT_LIGHT_TYPE, LIGHT_BIAS)

		self.addSensor(self.leftLightSensor,  breve.vector(1.80, 0.2,-1.1), dir.FRONT)
		self.addSensor(self.rightLightSensor, breve.vector(1.80, 0.2, 1.1), dir.FRONT)

		#Proximity sensors
		self.leftProximitySensor = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/4.0, LEFT_PROXIMITY_TYPES, PROXIMITY_BIAS)
		self.rightProximitySensor = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/4.0, RIGHT_PROXIMITY_TYPES, PROXIMITY_BIAS)

		self.addSensor(self.leftProximitySensor,  breve.vector(2.0, 0.2,-1.1), dir.FRONT)
		self.addSensor(self.rightProximitySensor, breve.vector(2.0, 0.2, 1.1), dir.FRONT)

		#Smell sensors
		self.leftSmellSensor = breve.createInstances(SmellSensor, 1, 'leftSmellSensor', LEFT_SMELL_TYPE, SMELL_BIAS)
		self.rightSmellSensor = breve.createInstances(SmellSensor, 1, 'rightSmellSensor', RIGHT_SMELL_TYPE, SMELL_BIAS)

		self.addSensor(self.leftSmellSensor,  breve.vector(2.0, -0.125,-1.1), dir.FRONT)
		self.addSensor(self.rightSmellSensor, breve.vector(2.0, -0.125, 1.1), dir.FRONT)

		#Sound sensors
		self.leftSoundSensor = breve.createInstances(SoundSensor, 1, 'leftSoundSensor', LEFT_SOUND_TYPE, SOUND_BIAS, SoundSensor.LEFT_BALANCE)
		self.rightSoundSensor = breve.createInstances(SoundSensor, 1, 'rightSoundSensor', RIGHT_SOUND_TYPE, SOUND_BIAS, SoundSensor.RIGHT_BALANCE)

		self.addSensor(self.leftSoundSensor,  breve.vector(1.5, 0,-1.5), dir.LEFT)
		self.addSensor(self.rightSoundSensor, breve.vector(1.5, 0, 1.5), dir.RIGHT)


		#Activators
		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.rightLightSensor,self.rightProximitySensor,self.rightSmellSensor,self.leftSoundSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftLightSensor,self.leftProximitySensor,self.leftSmellSensor,self.rightSoundSensor], rightActivator)


class Braitenberg3cController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)
		self.vehicle = breve.createInstances(Braitenberg3cVehicle, 1).move(breve.vector(0, 2, 0))
		self.watch(self.vehicle)

		#Scenario
		light = breve.createInstances(breve.LightSource, 1, 1.0, LEFT_LIGHT_TYPE).move(breve.vector(20, 1, 10))
		smell = breve.createInstances(breve.SmellSource, 1, 1.0, LEFT_SMELL_TYPE).move(breve.vector(20, 1, -10))
		sound = breve.createInstances(breve.SoundSource, 1, 1, LEFT_SOUND_TYPE).move(breve.vector(20, 1, 0))

Braitenberg3cController()
