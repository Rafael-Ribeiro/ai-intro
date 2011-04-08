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
from custom.functions import cut

from lib.Activator import BraitenbergActivator

MATURITY 		= 50.0 / 3
PROCRIATION 	= 40.0 / 3
LIFESPAN 		= 300.0
VELOCITY 		= 3.0
NATURAL			= 2.0

HALF_DISTANCE = 3
HALF_LIGHT = 7.0
HALF_SOUND = 7.0

DISTANCE_BIAS = 1.0
LIGHT_BIAS = 4.0
SOUND_BIAS = 3.0

DISTANCE_CUT	= 0.2
LIGHT_CUT		= DISTANCE_CUT
SOUND_CUT		= DISTANCE_CUT

#	Sensor Pair	|	Connection	|	Bias		|	Behaviour				|	Explanation	         		#
#---------------+---------------+---------------+---------------------------+-------------------------------#
#	Light		|	Uncrossed	|	Negative	|	Lover of light			| 	Cares for its eggs			#
#	Proximity	|	Crossed 	|	Negative	|	Explorer of objects		|	                    		#
#	Sound		|	Uncrossed	|	Negative	|	Lover towards sound		|	Cares for its babies		#

def leftActivator(vehicle, rightProximitySensor, leftLightSensor, leftSoundSensor):
	prox = cut(rightProximitySensor, 0, DISTANCE_CUT, (DISTANCE_CUT - rightProximitySensor) * DISTANCE_BIAS, 0.5, -NATURAL + 1)
	light = cut(leftLightSensor, 0, LIGHT_CUT, (LIGHT_CUT - leftLightSensor) * LIGHT_BIAS)
	sound = cut(leftSoundSensor, 0, SOUND_CUT, (SOUND_CUT - leftSoundSensor) * SOUND_BIAS)

	return VELOCITY*(prox + light + sound + NATURAL)

def rightActivator(vehicle, leftProximitySensor, rightLightSensor, rightSoundSensor, leftSoundSensor):
	prox = cut(leftProximitySensor, 0, DISTANCE_CUT, (DISTANCE_CUT - leftProximitySensor) * DISTANCE_BIAS, 0.5, -NATURAL - 1)
	light = cut(rightLightSensor, 0, LIGHT_CUT, (LIGHT_CUT - rightLightSensor) * LIGHT_BIAS)
	sound = cut(rightSoundSensor, 0, SOUND_CUT, (SOUND_CUT - rightSoundSensor) * SOUND_BIAS)

	return VELOCITY*(prox + light + sound + NATURAL)

class FemaleVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(3, 0.7, 3))
		self.setColor(color.PINK)

		self.handleCollisions("MaleVehicle", "reproduce", ["Link", "LightSensor"])

		self.age = 0.0
		self.last = 0.0

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 0.5, 0.2, color.WHITE)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.5, 0.2, color.WHITE)

		self.addWheel(self.leftWheel,  breve.vector(0.5, 0, -1.5), dir.RIGHT)
		self.addWheel(self.rightWheel, breve.vector(0.5, 0,  1.5), dir.RIGHT)

		from Male import MaleVehicle

		# Proximity
		self.leftProximitySensor  = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/2, [SphereStationary, FemaleVehicle, MaleVehicle, Egg], HALF_DISTANCE)
		self.rightProximitySensor  = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/2, [SphereStationary, FemaleVehicle, MaleVehicle, Egg], HALF_DISTANCE)
		
		self.addSensor(self.leftProximitySensor,  breve.vector(1.5, 0.21, -1.2), dir.FRONT)
		self.addSensor(self.rightProximitySensor,  breve.vector(1.5, 0.21, 1.2), dir.FRONT)
		
		# Smell
		#self.leftSmellSensor  = breve.createInstances(SmellSensor, 1, 'leftSmellSensor', color.RED, HALF_SMELL)
		#self.rightSmellSensor  = breve.createInstances(SmellSensor, 1, 'rightSmellSensor', color.RED, HALF_SMELL)

		#self.addSensor(self.leftSmellSensor,  breve.vector(2, -0.3, -1.5), dir.FRONT)
		#self.addSensor(self.rightSmellSensor,  breve.vector(2, -0.3, 1.5), dir.FRONT)


		# Light
		self.leftLightSensor  = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2, color.EGG, HALF_LIGHT, [Egg])
		self.rightLightSensor  = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2, color.EGG, HALF_LIGHT, [Egg])
		
		self.addSensor(self.leftLightSensor,  breve.vector(1.2, 0.1, -1.3), dir.FRONT)
		self.addSensor(self.rightLightSensor,  breve.vector(1.2, 0.1, 1.3), dir.FRONT)

		# Sound
		self.leftSoundSensor  = breve.createInstances(SoundSensor, 1, 'leftSoundSensor', color.GREEN, HALF_SOUND)
		self.rightSoundSensor  = breve.createInstances(SoundSensor, 1, 'rightSoundSensor', color.GREEN, HALF_SOUND)
		
		self.addSensor(self.leftSoundSensor,  breve.vector(1.0, 0.0, -1.0), dir.FRONT + dir.LEFT)
		self.addSensor(self.rightSoundSensor,  breve.vector(1.0, 0.0, 1.0), dir.FRONT + dir.RIGHT)

		# Activator
		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.rightProximitySensor, self.leftLightSensor, self.leftSoundSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftProximitySensor, self.rightLightSensor, self.rightSoundSensor, self.leftSoundSensor], rightActivator)

		self.cry = breve.createInstances(SoundSource, 1, 1.0, color.GREEN, True)
		self.attach(self.cry, breve.vector(0, 0, 0))  

		self.hormone = breve.createInstances(SmellSource, 1, 0.0, color.PINK, True)
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


		self.hormone.setIntensity(self.sexuality*0.2)
		self.cry.setIntensity(max(0.5, 1 - self.maturity))

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

		location = self.getLocation()
		location.y = 3.0

		egg = breve.createInstances(Egg, 1)
		egg.move(location)

	def getOpacity(self):
		return 1.0

breve.FemaleVehicle = FemaleVehicle
