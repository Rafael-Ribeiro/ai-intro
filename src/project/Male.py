#!/usr/share/breve/bin/breve
# -*- coding: utf-8 -*-

import sys
sys.path.append("../") 

import math
import breve

from custom.proximity.sensor import ProximitySensor
from custom.proximity.obstacles import SphereStationary

from custom.smell.sensor import SmellSensor
from custom.smell.source import SmellSource

from custom.sound.sensor import SoundSensor
from custom.sound.source import SoundSource

from custom.light.sensor import LightSensor
from Egg import Egg
from custom.constants import color, direction as dir
from custom.functions import cut,gaussian

from lib.Activator import BraitenbergActivator

MATURITY 		= 60.0 / 3
PROCRIATION 	= 30.0 / 3
LIFESPAN 		= 250.0
VELOCITY 		= 4.0
NATURAL			= 2.0
CURVING_FACTOR	= 25

HALF_DISTANCE = 3
HALF_LIGHT = 14.0
HALF_SMELL = 30.0
HALF_SOUND = 7.0

DISTANCE_BIAS = 1.0
LIGHT_BIAS = 5.0
SMELL_BIAS = 2.0
SOUND_BIAS = 9.0

DISTANCE_CUT	= 0.2
LIGHT_CUT		= DISTANCE_CUT
SMELL_CUT		= DISTANCE_CUT
SOUND_CUT		= DISTANCE_CUT

#	Sensor Pair	|	Connection	|	Bias		|	Behaviour				|	Explanation	         		#
#---------------+---------------+---------------+---------------------------+-------------------------------#
#	Light		|	Uncrossed	|	Negative	|	Lover of light			| 	Cares for "its" eggs		#
#	Proximity	|	Crossed 	|	Negative	|	Explorer of objects		|	                    		#
#	Smell		|	Crossed		|	Positive	|	Aggressor towards smell	|	Tries to procriate 			#
#	Sound		|	Uncrossed	|	Positive	|	Coward towards sound	|	Runs away from noisy babies #

def leftActivator(vehicle, rightProximitySensor, leftLightSensor, leftSmellSensor, rightSmellSensor, leftSoundSensor):
	prox = cut(rightProximitySensor, 0, DISTANCE_CUT, (DISTANCE_CUT - rightProximitySensor) * DISTANCE_BIAS, 0.5, -NATURAL + 1)
	light = cut(leftLightSensor, 0, LIGHT_CUT, (LIGHT_CUT - leftLightSensor) * LIGHT_BIAS)
	sound = cut(leftSoundSensor, 0, SOUND_CUT, (leftSoundSensor - SOUND_CUT) * SOUND_BIAS)

	smell_diff = rightSmellSensor - leftSmellSensor
	smell_sum = rightSmellSensor + leftSmellSensor
	smell = ((smell_diff * CURVING_FACTOR) + cut(smell_sum, 0, 0.20, cut(abs(smell_diff)/(max(smell_sum,0.0001)/2.0), -sound + 1, 0.05, 0))) * vehicle.sexuality * SMELL_BIAS

	return VELOCITY*(prox + light + smell + sound + NATURAL)

def rightActivator(vehicle, leftProximitySensor, rightLightSensor, leftSmellSensor, rightSmellSensor, rightSoundSensor):
	prox = cut(leftProximitySensor, 0, DISTANCE_CUT, (DISTANCE_CUT - leftProximitySensor) * DISTANCE_BIAS, 0.5, -NATURAL - 1)
	light = cut(rightLightSensor, 0, LIGHT_CUT, (LIGHT_CUT - rightLightSensor) * LIGHT_BIAS)
	sound = cut(rightSoundSensor, 0, SOUND_CUT, (rightSoundSensor - SOUND_CUT) * SOUND_BIAS - 0.1)

	smell_diff = leftSmellSensor - rightSmellSensor
	smell_sum = leftSmellSensor + rightSmellSensor
	smell = ((smell_diff * CURVING_FACTOR) + cut(smell_sum, 0, 0.20, cut(abs(smell_diff)/(max(smell_sum,0.0001)/2.0), -sound + 1, 0.05, 0))) * vehicle.sexuality * SMELL_BIAS

	return VELOCITY*(prox + light + smell + sound + NATURAL)

class MaleVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(3, 0.7, 3))
		self.setColor(color.RED)

		self.handleCollisions("FemaleVehicle", "reproduce", ["Link", "LightSensor"])

		self.age = 0.0
		self.last = 0.0

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 0.5, 0.2, color.BLACK)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.5, 0.2, color.BLACK)

		self.addWheel(self.leftWheel,  breve.vector(0.5, 0, -1.5), dir.RIGHT)
		self.addWheel(self.rightWheel, breve.vector(0.5, 0,  1.5), dir.RIGHT)

		from Female import FemaleVehicle

		# Proximity
		self.leftProximitySensor  = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/2, [SphereStationary, MaleVehicle, Egg], HALF_DISTANCE)
		self.rightProximitySensor  = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/2, [SphereStationary, MaleVehicle, Egg], HALF_DISTANCE)
		
		self.addSensor(self.leftProximitySensor,  breve.vector(1.5, 0.21, -1.3), dir.FRONT)
		self.addSensor(self.rightProximitySensor,  breve.vector(1.5, 0.21, 1.3), dir.FRONT)
		
		# Smell
		self.leftSmellSensor  = breve.createInstances(SmellSensor, 1, 'leftSmellSensor', color.PINK, HALF_SMELL)
		self.rightSmellSensor  = breve.createInstances(SmellSensor, 1, 'rightSmellSensor', color.PINK, HALF_SMELL)
		
		self.addSensor(self.leftSmellSensor, breve.vector(1.3, -0.3, -1.3), dir.FRONT)
		self.addSensor(self.rightSmellSensor, breve.vector(1.3, -0.3, 1.3), dir.FRONT)

		# Light
		self.leftLightSensor  = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2, color.EGG, HALF_LIGHT, [Egg])
		self.rightLightSensor  = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2, color.EGG, HALF_LIGHT, [Egg])
		
		self.addSensor(self.leftLightSensor,  breve.vector(1.2, 0.1, -1.3), dir.FRONT)
		self.addSensor(self.rightLightSensor,  breve.vector(1.2, 0.1, 1.3), dir.FRONT)

		# Sound
		self.leftSoundSensor  = breve.createInstances(SoundSensor, 1, 'leftSoundSensor', color.GREEN, HALF_SOUND)
		self.rightSoundSensor  = breve.createInstances(SoundSensor, 1, 'rightSoundSensor', color.GREEN, HALF_SOUND)
		
		self.addSensor(self.leftSoundSensor,  breve.vector(1, 0.0, -1), dir.FRONT + dir.LEFT)
		self.addSensor(self.rightSoundSensor,  breve.vector(1, 0.0, 1), dir.FRONT + dir.RIGHT)

		# Activators
		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.rightProximitySensor, self.leftLightSensor, self.leftSmellSensor, self.rightSmellSensor, self.leftSoundSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftProximitySensor, self.rightLightSensor, self.leftSmellSensor, self.rightSmellSensor, self.rightSoundSensor], rightActivator)

		self.cry = breve.createInstances(SoundSource, 1, 1.0, color.GREEN, True)
		self.attach(self.cry, breve.vector(0, 0, 0))  

		self.hormone = breve.createInstances(SmellSource, 1, 0.0, color.RED, True)
		self.attach(self.hormone, breve.vector(-1.5,0.7,0))

		self.sexuality = 0.0
		self.maturity = 0.0

	def updateSexuality(self):
		tired = 1 - min(1.0, (self.age-self.last)/PROCRIATION)

		self.maturity = min(1.0, self.age/MATURITY)
	
		if self.maturity - tired == 1.0:
			self.sexuality = 1.0
		else:
			self.sexuality = 0.0

		self.hormone.setIntensity(self.sexuality)
		self.cry.setIntensity(max(1-self.maturity, 0.1))

	def iterate(self):
		self.age = self.getAge()

		if self.age >= LIFESPAN:
			self.getController().unwatch(self)
			breve.deleteInstances(self)

		self.updateSexuality()

	def reproduce(self, obj):
		if self.sexuality == 1.0 and obj.sexuality == 1.0:
			self.hadSex(obj)
			obj.hadSex(self)

	def hadSex(self, obj):
		self.last = self.getAge()
		self.updateSexuality()

	def getOpacity(self):
		return 1.0
