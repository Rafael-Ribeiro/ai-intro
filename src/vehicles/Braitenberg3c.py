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

VELOCITY = 0.0 	# Natural velocity

LIGHT_BIAS = 5.0
PROXIMITY_BIAS = 5.0
SMELL_BIAS = 3.5
SOUND_BIAS = 5.0

LIGHT_FACTOR = 5.0
PROXIMITY_FACTOR = 5.0
SMELL_FACTOR = 20.0
SOUND_FACTOR = 5.0

def leftActivator(rightLightSensor,rightProximitySensor,rightSmellSensor,leftSoundSensor):
	return VELOCITY - rightLightSensor*LIGHT_FACTOR - rightProximitySensor*PROXIMITY_FACTOR + rightSmellSensor*SMELL_FACTOR + leftSoundSensor*SOUND_FACTOR

def rightActivator(leftLightSensor,leftProximitySensor,leftSmellSensor,rightSoundSensor):
	return VELOCITY - leftLightSensor*LIGHT_FACTOR - leftProximitySensor*PROXIMITY_FACTOR + leftSmellSensor*SMELL_FACTOR + rightSoundSensor*SOUND_FACTOR

class Braitenberg3cController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		#Scenario
		light = breve.createInstances(breve.LightSource, 1, 1.0, breve.vector(0,1,0))
		light.move(breve.vector(20, 1, 10))

		smell = breve.createInstances(breve.SmellSource, 1, 1.0, breve.vector(1,0,0))
		smell.move(breve.vector(20, 1, -10))

		sound = breve.createInstances(breve.SoundSource, 1, 1, breve.vector(0,0,0))
		sound.move(breve.vector(20, 1, 0))
		sound = breve.createInstances(breve.SoundSource, 1, 1, breve.vector(0,0.5,1))
		sound.move(breve.vector(20, 1, 0))

		self.vehicle = breve.createInstances(breve.BraitenbergVehicle, 1, breve.vector(4, 0.7, 3))
		self.watch(self.vehicle)

		self.vehicle.move(breve.vector(0, 2, 0))

		#Wheels
		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2)
	
		self.vehicle.addWheel(self.leftWheel, breve.vector(-0.500000, 0, -1.500000))
		self.vehicle.addWheel(self.rightWheel, breve.vector(-0.500000, 0, 1.500000))

		# Sensors #
		#Light sensors
		self.leftLightSensor = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2.0, breve.vector(0,1,0), LIGHT_BIAS)
		self.rightLightSensor = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2.0, breve.vector(0,1,0), LIGHT_BIAS)

		self.vehicle.addSensor(self.leftLightSensor,  breve.vector(1.80, 0.2,-1.1), breve.vector(1,0,0))
		self.vehicle.addSensor(self.rightLightSensor, breve.vector(1.80, 0.2, 1.1), breve.vector(1,0,0))

		#Proximity sensors
		self.leftProximitySensor = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/4.0, [], PROXIMITY_BIAS)
		self.rightProximitySensor = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/4.0, [], PROXIMITY_BIAS)

		self.vehicle.addSensor(self.leftProximitySensor,  breve.vector(2.0, 0.2,-1.1), breve.vector(1,0,0))
		self.vehicle.addSensor(self.rightProximitySensor, breve.vector(2.0, 0.2, 1.1), breve.vector(1,0,0))

		#Smell sensors
		self.leftSmellSensor = breve.createInstances(SmellSensor, 1, 'leftSmellSensor', breve.vector(1,0,0), SMELL_BIAS)
		self.rightSmellSensor = breve.createInstances(SmellSensor, 1, 'rightSmellSensor', breve.vector(1,0,0), SMELL_BIAS)

		self.vehicle.addSensor(self.leftSmellSensor,  breve.vector(2.0, -0.125,-1.1), breve.vector(1,0,0))
		self.vehicle.addSensor(self.rightSmellSensor, breve.vector(2.0, -0.125, 1.1), breve.vector(1,0,0))

		#Sound sensors
		self.leftSoundSensor = breve.createInstances(SoundSensor, 1, 'leftSoundSensor', breve.vector(0,0,0), SOUND_BIAS, 0)
		self.rightSoundSensor = breve.createInstances(SoundSensor, 1, 'rightSoundSensor', breve.vector(0,0.5,1), SOUND_BIAS, 1)

		self.vehicle.addSensor(self.leftSoundSensor,  breve.vector(1.5, 0,-1.5), breve.vector(0,0,-1))
		self.vehicle.addSensor(self.rightSoundSensor, breve.vector(1.5, 0, 1.5), breve.vector(0,0,1))


		#Activators
		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.rightLightSensor,self.rightProximitySensor,self.rightSmellSensor,self.leftSoundSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftLightSensor,self.leftProximitySensor,self.leftSmellSensor,self.rightSoundSensor], rightActivator)


# Create an instance of our controller object to initialize the simulation

Braitenberg3cController()
