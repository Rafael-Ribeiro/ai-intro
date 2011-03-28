import breve
import math

from custom.sound.source import SoundSource
from custom.sound.sensor import SoundSensor
from custom.proximity.sensor import ProximitySensor
from lib.Activator import BraitenbergActivator

class AggressorController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		for i in range(100):
			for j in range(100):
				sound = breve.createInstances(breve.SoundSource, 1, 1.0, breve.vector(0,1,0))
				sound.move(breve.vector(0.01 * i - 0.5,0.5,0.01 * j - 0.5))

		self.block = breve.createInstances(breve.Mobile, 1)
		self.blockShape = breve.createInstances(breve.Cube, 1).initWith(breve.vector(1,1,1))
		self.block.setShape(self.blockShape)
		self.block.move(breve.vector(18, 2, 0))

		self.vehicle = breve.createInstances(breve.BraitenbergVehicle, 1, breve.vector(4, 1, 3))
		self.watch(self.vehicle)

		self.vehicle.move(breve.vector(0, 0.5, 0))
	
		self.middleSensor = breve.createInstances(SoundSensor, 1, 'leftSensor', breve.vector(0,1,0), math.pi/4)

		self.vehicle.addSensor(self.middleSensor, breve.vector(0.000000, 0.000000, 0.000000), breve.vector(1,0,0))

		#self.middleActivator = BraitenbergActivator(self.rightWheel, [self.leftSensor, self.middleSensor], lambda leftSensor: leftSensor*10-(1/middleSensor)*11 + 1)

breve.AggressorController = AggressorController

# Create an instance of our controller object to initialize the simulation

AggressorController()
