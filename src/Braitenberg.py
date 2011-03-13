
# Note: this file was automatically converted to Python from the
# original steve-language source code.  Please see the original
# file for more detailed comments and documentation.

import breve
import math

class BraitenbergControl(breve.PhysicalControl):
	'''This class is used for building simple Braitenberg vehicle  simulations.  To create a Braitenberg vehicle simulation,  subclass BraitenbergControl and use the init method to  create OBJECT(BraitenbergLight) and  OBJECT(BraitenbergVehicle) objects.'''

	def __init__(self):
		breve.PhysicalControl.__init__(self)
		self.cloudTexture = None
		self.floor = None
		BraitenbergControl.init(self)

	def init(self):
		self.enableLighting()
		self.enableSmoothDrawing()
		self.floor = breve.createInstances(breve.Floor, 1)
		self.pointCamera(breve.vector(0, 0, 0), breve.vector(3, 3, 24))
		self.enableShadows()
		self.enableReflections()
		self.cloudTexture = breve.createInstances(breve.Image, 1).load('images/clouds.png')
		self.setBackgroundColor(breve.vector(0.400000, 0.600000, 0.900000))
		self.setBackgroundTextureImage(self.cloudTexture)


breve.BraitenbergControl = BraitenbergControl
class BraitenbergVehicle(breve.MultiBody):
	'''This object is used in conjunction with OBJECT(BraitenbergControl) to create simple Braitenberg vehicles.'''

	def __init__(self):
		breve.MultiBody.__init__(self)
		self.bodyLink = None
		self.bodyShape = None
		self.sensorShape = None
		self.sensors = breve.objectList()
		self.wheelShape = None
		self.wheels = breve.objectList()
		BraitenbergVehicle.init(self)

	def addSensor(self, sensor, location, direction):
		'''Adds a sensor at location on the vehicle.  This method returns the sensor which is created, a OBJECT(BraitenbergSensor).  You'll use the returned object to connect it to the vehicle's wheels.'''

		joint = None

		# perpendicular to direction and (0,1,0)
		direction = direction/direction.length()
		normal = breve.vector(-direction.z, 0, direction.x)
		rotation = math.acos(direction.y)

		sensor.setShape(self.sensorShape)
		joint = breve.createInstances(breve.RevoluteJoint, 1)
		joint.setRelativeRotation(normal, rotation)

		joint.link(breve.vector(1, 0, 0), location, breve.vector(0, 0, 0), sensor, self.bodyLink)
		joint.setDoubleSpring(300, 0.010000, -0.010000)

		self.addDependency(joint)
		self.addDependency(sensor)
		self.sensors.append(sensor)

		return sensor

	def addWheel(self, location):
		'''Adds a wheel at location on the vehicle.  This method returns the wheel which is created, a OBJECT(BraitenbergWheel).  You'll use the returned object to connect it to the vehicle's sensors.'''

		joint = None
		wheel = None

		wheel = breve.createInstances(breve.BraitenbergWheel, 1)
		wheel.setShape(self.wheelShape)
		joint = breve.createInstances(breve.RevoluteJoint, 1)
		joint.setRelativeRotation(breve.vector(1, 0, 0), 1.570800)
		joint.link(breve.vector(0, 0, 1), location, breve.vector(0, 0, 0), wheel, self.bodyLink)
		wheel.setET(0.800000)
		wheel.setJoint(joint)
		joint.setStrengthLimit((joint.getStrengthHardLimit() / 2))
		wheel.setColor(breve.vector(0.600000, 0.600000, 0.600000))
		wheel.setMu(100000)
		self.addDependency(joint)
		self.addDependency(wheel)
		self.wheels.append(wheel)
		return wheel

	def destroy(self):
		breve.deleteInstances(self.sensorShape)
		breve.deleteInstances(self.wheelShape)
		breve.deleteInstances(self.bodyShape)
		breve.MultiBody.destroy(self)

	def getDensity(self):
		return 1.000000

	def getWheelRadius(self):
		return 0.600000

	def getWheelWidth(self):
		return 0.100000

	def init(self):
		self.bodyShape = breve.createInstances(breve.Cube, 1)
		self.bodyShape.initWith(breve.vector(4.000000, 0.750000, 3.000000))
		self.wheelShape = breve.createInstances(breve.Shape, 1)
		self.wheelShape.initWithPolygonDisk(40, self.getWheelWidth(), self.getWheelRadius())
		self.sensorShape = breve.createInstances(breve.Shape, 1)
		self.sensorShape.initWithPolygonCone(10, 0.500000, 0.200000)
		self.bodyShape.setDensity(self.getDensity())
		self.bodyLink = breve.createInstances(breve.Link, 1)
		self.bodyLink.setShape(self.bodyShape)
		self.bodyLink.setMu(-1.000000)
		self.bodyLink.setET(0.800000)
		self.setRoot(self.bodyLink)
		self.move(breve.vector(0, 0.900000, 0))
		self.setTextureScale(1.500000)


breve.BraitenbergVehicle = BraitenbergVehicle
class BraitenbergHeavyVehicle(breve.BraitenbergVehicle):
	'''A heavy duty version of OBJECT(BraitenbergVehicle), this vehicle is heavier and harder to control, but more stable at higher  speeds.'''

	def __init__(self):
		breve.BraitenbergVehicle.__init__(self)

	def getDensity(self):
		return 20.000000

	def getWheelRadius(self):
		return 0.800000

	def getWheelWidth(self):
		return 0.400000


breve.BraitenbergHeavyVehicle = BraitenbergHeavyVehicle
class BraitenbergLight(breve.Mobile):
	'''A BraitenbergLight is used in conjunction with OBJECT(BraitenbergControl) and OBJECT(BraitenbergVehicle).  It is what the OBJECT(BraitenbergSensor) objects on the BraitenbergVehicle detect. <p> There are no special behaviors associated with the lights--they're  basically just plain OBJECT(Mobile) objects.'''

	def __init__(self):
		breve.Mobile.__init__(self)

		self.intensity = 0
		self.color = breve.vector()

	def init(self, intensity, color):
		self.intensity = intensity
		self.color = color # vector(r,g,b)

		self.setShape(breve.createInstances(breve.Shape, 1).initWithSphere(0.300000))
		self.setColor(color)
	
	def getIntensity(self):
		return self.intensity

breve.BraitenbergLight = BraitenbergLight
class BraitenbergWheel(breve.Link):
	'''A BraitenbergWheel is used in conjunction with OBJECT(BraitenbergVehicle) to build Braitenberg vehicles.  This class is typically not instantiated manually, since OBJECT(BraitenbergVehicle) creates one for you when you add a wheel to the vehicle. <p> <b>NOTE: this class is included as part of the file "Braitenberg.tz".</b>'''

	MAX_VELOCITY = 30

	def __init__(self):
		breve.Link.__init__(self)

		self.joint = None
		self.velocity = 0

		BraitenbergWheel.init(self)

	def init(self):
		pass

	def activate(self, n):
		self.velocity = min(n, BraitenbergWheel.MAX_VELOCITY)

	def postIterate(self):
		self.joint.setJointVelocity(self.velocity)

	def setJoint(self, j):
		self.joint = j

breve.BraitenbergWheel = BraitenbergWheel
class BraitenbergSensor(breve.Link):
	'''A BraitenbergSensor is used in conjunction with OBJECT(BraitenbergVehicle) to build Braitenberg vehicles.  This class is typically not instantiated manually, since OBJECT(BraitenbergVehicle) creates one for you when you add a sensor to the vehicle. <p> <b>NOTE: this class is included as part of the file "Braitenberg.tz".</b>'''

	def __init__(self):
		breve.Link.__init__(self)

		self.name = ""
		self.activators = breve.objectList()

	def init(self, name):
		self.name = name

	def getName(self):
		return self.name

	def iterate(self):
		raise NotImplementedError('Braitenberg sensors must override this method')

	def link(self, activator):
		self.activators.append(activator)

	def getName(self):
		return self.name

breve.BraitenbergSensor = BraitenbergSensor
# Add our newly created classes to the breve namespace

breve.BraitenbergVehicles = BraitenbergVehicle
breve.BraitenbergHeavyVehicles = BraitenbergHeavyVehicle
breve.BraitenbergLights = BraitenbergLight
breve.BraitenbergWheels = BraitenbergWheel
breve.BraitenbergSensors = BraitenbergSensor



