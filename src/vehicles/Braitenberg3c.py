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

#Simulation constants
VELOCITY = 5.0 	# Natural velocity
D = 2.0 #distance between objects on the grid


#Sensors' bias
LIGHT_BIAS = 3.0
SMELL_BIAS = 4.0
SOUND_BIAS = 0.5
PROXIMITY_BIAS = 4.0

#Sensors' factors
LIGHT_FACTOR = 1.0
SMELL_FACTOR = 1.0
SOUND_FACTOR = 1.0
PROXIMITY_FACTOR = LIGHT_FACTOR + SMELL_FACTOR + SOUND_FACTOR + 2

#Sensor/Source types
LEFT_LIGHT_TYPE = color.GREEN
RIGHT_LIGHT_TYPE = LEFT_LIGHT_TYPE

LEFT_SMELL_TYPE = color.RED
RIGHT_SMELL_TYPE = LEFT_SMELL_TYPE

LEFT_SOUND_TYPE = color.BLACK
RIGHT_SOUND_TYPE = LEFT_SOUND_TYPE

LEFT_PROXIMITY_TYPES = [SphereStationary]
RIGHT_PROXIMITY_TYPES = LEFT_PROXIMITY_TYPES


def leftActivator(vehicle, rightLightSensor,leftProximitySensor,rightProximitySensor,rightSmellSensor,leftSoundSensor):
	proximity = PROXIMITY_FACTOR * (0.5 - rightProximitySensor)
	opposite_proximity = PROXIMITY_FACTOR * (0.5 - leftProximitySensor)

	#if abs(proximity + opposite_proximity) < 0.1:
	#	return 2*VELOCITY

	sound = SOUND_FACTOR * 0
	smell = SMELL_FACTOR * 0
	light = LIGHT_FACTOR * (1 - 0)

	return VELOCITY * (proximity + sound + smell + light)

def rightActivator(vehicle, leftLightSensor,leftProximitySensor,rightProximitySensor,leftSmellSensor,rightSoundSensor):
	proximity = PROXIMITY_FACTOR * (0.5 - leftProximitySensor)
	opposite_proximity = PROXIMITY_FACTOR * (0.5 - rightProximitySensor)

	#if abs(proximity + opposite_proximity) < 0.1:
	#	return -2*VELOCITY

	sound = SOUND_FACTOR * 0
	smell = SMELL_FACTOR * 0
	light = LIGHT_FACTOR * (1 - 0)

	return VELOCITY * (proximity + sound + smell + light)

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
		self.leftProximitySensor = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/2.0, LEFT_PROXIMITY_TYPES, PROXIMITY_BIAS)
		self.rightProximitySensor = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/2.0, RIGHT_PROXIMITY_TYPES, PROXIMITY_BIAS)

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
		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.rightLightSensor,self.leftProximitySensor,self.rightProximitySensor,self.rightSmellSensor,self.leftSoundSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftLightSensor,self.leftProximitySensor,self.rightProximitySensor,self.leftSmellSensor,self.rightSoundSensor], rightActivator)


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
					breve.createInstances(LightSource, 1, 1.0, LEFT_LIGHT_TYPE, False).move(breve.vector(i*D, 1.0, j*D))
				elif lines[i][j] == 's': #<S>mell
					breve.createInstances(SmellSource, 1, 1.0, LEFT_SMELL_TYPE, False).move(breve.vector(i*D, 1.0, j*D))
				elif lines[i][j] == 'o': #s<O>und
					breve.createInstances(SoundSource, 1, 1.0, LEFT_SOUND_TYPE, False).move(breve.vector(i*D, 1.0, j*D))
				elif lines[i][j] == 'X': #vehicle
					self.vehicle.move(breve.vector(i*D, 2, j*D))
		f.close()
		self.vehicle.rotate(breve.vector(0,1,0),40)

Braitenberg3cController()
