
# Note: this file was automatically converted to Python from the
# original steve-language source code.  Please see the original
# file for more detailed comments and documentation.


import breve
import math

from custom.light.source import LightSource
from custom.light.sensor import LightSensor
from custom.proximity.sensor import ProximitySensor
from lib.Activator import BraitenbergActivator

class AggressorController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		for i in range(10):
			light = breve.createInstances(breve.LightSource, 1, 1.0, breve.vector(0,1,0))
			light.move(breve.vector((20 * breve.breveInternalFunctionFinder.sin(self, ((i * 6.280000) / 10))), 1, (20 * breve.breveInternalFunctionFinder.cos(self, ((i * 6.280000) / 10)))))

		self.block = breve.createInstances(breve.Mobile, 1)
		self.blockShape = breve.createInstances(breve.Cube, 1).initWith(breve.vector(1,1,1))
		self.block.setShape(self.blockShape)
		self.block.move(breve.vector(18, 2, 0))

		self.vehicle = breve.createInstances(breve.BraitenbergVehicle, 1, breve.vector(4, 0.7, 3))
		self.watch(self.vehicle)

		self.vehicle.move(breve.vector(0, 2, 18))

		self.leftWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.1)
		self.rightWheel = breve.createInstances(breve.BraitenbergWheel, 1, 0.6, 0.1)
	
		self.vehicle.addWheel(self.leftWheel, breve.vector(-0.500000, 0, -1.500000))
		self.vehicle.addWheel(self.rightWheel, breve.vector(-0.500000, 0, 1.500000))

		self.rightSensor = breve.createInstances(LightSensor, 1, 'rightSensor', math.pi/4, breve.vector(0,1,0))
		self.leftSensor = breve.createInstances(LightSensor, 1, 'leftSensor', math.pi/4, breve.vector(0,1,0))
		self.middleSensor = breve.createInstances(ProximitySensor, 1, 'middleSensor', math.pi/4)

		self.vehicle.addSensor(self.rightSensor, breve.vector(2.000000, 0.400000, 1.500000), breve.vector(1,0,0))
		self.vehicle.addSensor(self.leftSensor, breve.vector(2.000000, 0.400000, -1.500000), breve.vector(1,0,0))
		self.vehicle.addSensor(self.middleSensor, breve.vector(2.2, 0.4, 0), breve.vector(1, 0, 0))

		self.leftActivator = BraitenbergActivator(self.leftWheel, [self.rightSensor, self.middleSensor], lambda rightSensor, middleSensor: rightSensor*10-(1/middleSensor)*11 + 1)
		self.rightActivator = BraitenbergActivator(self.rightWheel, [self.leftSensor, self.middleSensor], lambda leftSensor, middleSensor: leftSensor*10-(1/middleSensor)*11 + 1)

breve.AggressorController = AggressorController

# Create an instance of our controller object to initialize the simulation

AggressorController()
