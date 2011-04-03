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

from lib.Activator import BraitenbergActivator

MATURITY 		= 50.0
PROCRIATION 	= 30.0
LIFESPAN 		= 250.0
VELOCITY 		= 10.0

DISTANCE_BIAS = 2.5
LIGHT_BIAS = 4.0
SMELL_BIAS = 10.0
SOUND_BIAS = 3.0

#	Sensor Pair	|	Connection	|	Bias		|	Behaviour				|	Explanation	         		#
#---------------+---------------+---------------+---------------------------+-------------------------------#
#	Light		|	Uncrossed	|	Negative	|	Lover of light			| 	Cares for "its" eggs		#
#	Proximity	|	Crossed 	|	Negative	|	Explorer of objects		|	                    		#
#	Smell		|	Crossed		|	Positive	|	Aggressor towards smell	|	Tries to procriate 			#
#	Sound		|	Uncrossed	|	Positive	|	Coward towards sound	|	Runs away from noisy babies #

def leftActivator(vehicle, leftProximitySensor, rightProximitySensor, leftLightSensor, rightSmellSensor, leftSoundSensor):
	a = 1 - rightProximitySensor*2
	b = 1 - leftProximitySensor*2

	if (abs(a+b) < 0.1):
		return 5*VELOCITY

	return VELOCITY*(a - 2*leftLightSensor + leftSoundSensor + 3*rightSmellSensor) #*vehicle.sexuality + 0.5*leftSoundSensor)

def rightActivator(vehicle, leftProximitySensor, rightProximitySensor, rightLightSensor, leftSmellSensor, rightSoundSensor):
	a = 1 - rightProximitySensor*2
	b = 1 - leftProximitySensor*2

	if (abs(a+b) < 0.1):
		return -5*VELOCITY
	
	return VELOCITY*(b - 2*rightLightSensor + rightSoundSensor + 3*leftSmellSensor) # +3*leftSmellSensor*vehicle.sexuality + 0.5*rightSoundSensor)

class MaleVehicle(breve.BraitenbergVehicle):
	def __init__(self):
		breve.BraitenbergVehicle.__init__(self, breve.vector(4, 0.7, 3))
		self.setColor(color.RED)

		self.handleCollisions("FemaleVehicle", "reproduce", ["Link", "LightSensor"])

		self.age = 0.0
		self.last = 0.0

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel,  1, 0.6, 0.2, color.BLACK)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.2, color.BLACK)

		self.addWheel(self.leftWheel,  breve.vector(-0.5, 0, -1.5), dir.RIGHT)
		self.addWheel(self.rightWheel, breve.vector(-0.5, 0,  1.5), dir.RIGHT)

		from Female import FemaleVehicle

		# Proximity
		self.leftProximitySensor  = breve.createInstances(ProximitySensor, 1, 'leftProximitySensor', math.pi/3, [SphereStationary, MaleVehicle, FemaleVehicle], DISTANCE_BIAS)
		self.rightProximitySensor  = breve.createInstances(ProximitySensor, 1, 'rightProximitySensor', math.pi/3, [SphereStationary, MaleVehicle, FemaleVehicle], DISTANCE_BIAS)
		
		self.addSensor(self.leftProximitySensor,  breve.vector(2, 0.21, -1.2), dir.FRONT)
		self.addSensor(self.rightProximitySensor,  breve.vector(2, 0.21, 1.2), dir.FRONT)
		
		# Hormones
		self.leftSmellSensor  = breve.createInstances(SmellSensor, 1, 'leftSmellSensor', color.PINK, SMELL_BIAS)
		self.rightSmellSensor  = breve.createInstances(SmellSensor, 1, 'rightSmellSensor', color.PINK, SMELL_BIAS)
		
		self.addSensor(self.leftSmellSensor,  breve.vector(2, -0.3, -1.5), dir.FRONT)
		self.addSensor(self.rightSmellSensor,  breve.vector(2, -0.3, 1.5), dir.FRONT)

		# Light
		self.leftLightSensor  = breve.createInstances(LightSensor, 1, 'leftLightSensor', math.pi/2, color.EGG, LIGHT_BIAS, [Egg])
		self.rightLightSensor  = breve.createInstances(LightSensor, 1, 'rightLightSensor', math.pi/2, color.EGG, LIGHT_BIAS, [Egg])
		
		self.addSensor(self.leftLightSensor,  breve.vector(2, 0.1, -1.5), dir.FRONT)
		self.addSensor(self.rightLightSensor,  breve.vector(2, 0.1, 1.5), dir.FRONT)

		# Sound
		self.leftSoundSensor  = breve.createInstances(SoundSensor, 1, 'leftSoundSensor', color.GREEN, SOUND_BIAS)
		self.rightSoundSensor  = breve.createInstances(SoundSensor, 1, 'rightSoundSensor', color.GREEN, SOUND_BIAS)
		
		self.addSensor(self.leftSoundSensor,  breve.vector(1.5, 0.0, -1.5), dir.LEFT)
		self.addSensor(self.rightSoundSensor,  breve.vector(1.5, 0.0, 1.5), dir.RIGHT)

		# Activators
		self.leftActivator = BraitenbergActivator(self, self.leftWheel, [self.leftProximitySensor, self.rightProximitySensor, self.leftLightSensor, self.rightSmellSensor, self.leftSoundSensor], leftActivator)
		self.rightActivator = BraitenbergActivator(self, self.rightWheel, [self.leftProximitySensor, self.rightProximitySensor, self.rightLightSensor, self.leftSmellSensor, self.rightSoundSensor], rightActivator)

		self.cry = breve.createInstances(SoundSource, 1, 1.0, color.GREEN, True)
		self.attach(self.cry, breve.vector(1.5, 0, 0))  

		self.hormone = breve.createInstances(SmellSource, 1, 0.0, color.RED, True)
		self.attach(self.hormone, breve.vector(-2.0,0.7,0))

		self.sexuality = 0.0
		self.maturity = 0.0

	def updateSexuality(self):
		tired = 1 - min(1.0, (self.age-self.last)/PROCRIATION)

		self.maturity = min(1.0, self.age/MATURITY)
		self.sexuality = max(0.0, self.maturity - tired)

		self.hormone.setIntensity(self.sexuality)
		self.cry.setIntensity(max(1-self.maturity, 0.3))

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
