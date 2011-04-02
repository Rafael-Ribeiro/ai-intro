
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

	def __init__(self, size = breve.vector(7,1,4)):
		breve.MultiBody.__init__(self)
		self.sensors = breve.objectList()
		self.wheels = breve.objectList()

		self.bodyShape = breve.createInstances(breve.Cube, 1)
		self.bodyShape.initWith(size)

		self.bodyShape.setDensity(self.getDensity())
		self.bodyLink = breve.createInstances(breve.Link, 1)
		self.bodyLink.setShape(self.bodyShape)
		self.bodyLink.setMu(-1.000000)
		self.bodyLink.setET(0.800000)

		self.setRoot(self.bodyLink)
		self.setTextureScale(1.500000)

	def addSensor(self, sensor, location, direction):
		'''Adds a sensor at location on the vehicle.  This method returns the sensor which is created, a OBJECT(BraitenbergSensor).  You'll use the returned object to connect it to the vehicle's wheels.'''

		joint = None

		# perpendicular to direction and (0,1,0)
		direction = direction.normalize()
		normal = breve.vector(-direction.z, 0, direction.x) #cross product
		rotation = math.acos(direction.y) #angle between vectors (using dot product definition)

		joint = breve.createInstances(breve.RevoluteJoint, 1)
		joint.setRelativeRotation(normal, rotation)

		joint.link(direction, location, breve.vector(0, 0, 0), sensor, self.bodyLink)
		joint.setDoubleSpring(300, 0.01, -0.01)

		self.addDependency(joint)
		self.addDependency(sensor)
		self.sensors.append(sensor)

	def addWheel(self, wheel, location, axis = breve.vector(0,0,1)):
		joint = breve.createInstances(breve.RevoluteJoint, 1)
		joint.setRelativeRotation(breve.vector(-axis.z, 0, axis.x), 1.570800) # irrelevant
		joint.link(axis, location, breve.vector(0, 0, 0), wheel, self.bodyLink)

		wheel.setET(0.800000)
		wheel.setJoint(joint)

		joint.setStrengthLimit((joint.getStrengthHardLimit() / 2))
		wheel.setMu(100000)

		self.addDependency(joint)
		self.addDependency(wheel)
		self.wheels.append(wheel)

	def attach(self, what, pos):
		joint = breve.createInstances(breve.RevoluteJoint, 1)
		joint.link(breve.vector(0,1,0), pos, breve.vector(0, 0, 0), what, self.bodyLink)

		self.addDependency(joint)
		self.addDependency(what)

	def destroy(self):
		breve.deleteInstances(self.bodyShape)
		breve.MultiBody.destroy(self)

	def getDensity(self):
		return 1.000000

class BraitenbergWheel(breve.Link):
	'''A BraitenbergWheel is used in conjunction with OBJECT(BraitenbergVehicle) to build Braitenberg vehicles.  This class is typically not instantiated manually, since OBJECT(BraitenbergVehicle) creates one for you when you add a wheel to the vehicle. <p> <b>NOTE: this class is included as part of the file "Braitenberg.tz".</b>'''

	MAX_VELOCITY = 30.0

	def __init__(self, radius, width, color = breve.vector(0,0,0)):
		breve.Link.__init__(self)

		self.joint = None
		self.velocity = 0

		self.radius = radius
		self.width = width
	
		self.shape = breve.createInstances(breve.Shape, 1)
		self.shape.initWithPolygonDisk(40, width, radius)
		self.setShape(self.shape)

		# Colision with a polygon disk is buggy at high speeds, make a sphere for the collision (also, it's faster)
		self.wheel = breve.createInstances(breve.Shape, 1)
		self.wheel.initWithSphere(radius)
		self.setCollisionShape(self.wheel)
		
		self.color = color
		self.setColor(color)

	def activate(self, n):
		self.velocity = min(n, BraitenbergWheel.MAX_VELOCITY)

	def postIterate(self):
		self.joint.setJointVelocity(self.velocity)#/self.radius)

	def getRadius(self):
		return self.radius

	def getWidth(self):
		return self.width

	def setJoint(self, j):
		self.joint = j

breve.BraitenbergWheel = BraitenbergWheel
class BraitenbergSensor(breve.Link):
	'''A BraitenbergSensor is used in conjunction with OBJECT(BraitenbergVehicle) to build Braitenberg vehicles.  This class is typically not instantiated manually, since OBJECT(BraitenbergVehicle) creates one for you when you add a sensor to the vehicle. <p> <b>NOTE: this class is included as part of the file "Braitenberg.tz".</b>'''

	def __init__(self, name):
		breve.Link.__init__(self)

		self.name = name
		self.activators = breve.objectList()

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
breve.BraitenbergWheels = BraitenbergWheel
breve.BraitenbergSensors = BraitenbergSensor

