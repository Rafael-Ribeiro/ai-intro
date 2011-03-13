
# Note: this file was automatically converted to Python from the
# original steve-language source code.  Please see the original
# file for more detailed comments and documentation.


import breve
import math

from LightSensor import LightSensor 
from BraitenbergActivator import BraitenbergActivator

class AggressorController(breve.BraitenbergControl):
	def __init__(self):
		breve.BraitenbergControl.__init__(self)

		self.leftSensor = None
		self.leftWheel = None
		self.n = 0
		self.rightSensor = None
		self.rightWheel = None
		self.vehicle = None

		AggressorController.init(self)

	def init(self):
		for i in range(10):
			light = breve.createInstances(breve.BraitenbergLight, 1)
			light.move(breve.vector((20 * breve.breveInternalFunctionFinder.sin(self, ((i * 6.280000) / 10))), 1, (20 * breve.breveInternalFunctionFinder.cos(self, ((i * 6.280000) / 10)))))
			light.init(1.0, breve.vector(0,1,0))

		self.vehicle = breve.createInstances(breve.BraitenbergVehicle, 1)
		self.watch(self.vehicle)

		self.vehicle.move(breve.vector(0, 2, 18))

		self.leftWheel = self.vehicle.addWheel(breve.vector(-0.500000, 0, -1.500000))
		self.rightWheel = self.vehicle.addWheel(breve.vector(-0.500000, 0, 1.500000))

		self.rightSensor = breve.createInstances(LightSensor, 1)
		self.rightSensor.init('rightSensor', math.pi/4)

		self.leftSensor = breve.createInstances(LightSensor, 1)
		self.leftSensor.init('leftSensor', math.pi/4)

		self.rightSensor = self.vehicle.addSensor(self.rightSensor, breve.vector(2.000000, 0.400000, 1.500000), breve.vector(1,0,0))
		self.leftSensor = self.vehicle.addSensor(self.leftSensor, breve.vector(2.000000, 0.400000, -1.500000), breve.vector(1,0,0))

		self.leftActivator = BraitenbergActivator(self.leftWheel, lambda leftSensor: leftSensor*30)
		self.rightActivator = BraitenbergActivator(self.rightWheel, lambda rightSensor: rightSensor*30)

		self.leftSensor.link(self.leftActivator)
		self.rightSensor.link(self.rightActivator)

breve.AggressorController = AggressorController


# Create an instance of our controller object to initialize the simulation

AggressorController()
