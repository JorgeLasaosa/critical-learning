import numpy as np
from abc import ABCMeta, abstractmethod

# Abstract class that represents Objects in the World
class object:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, coords, nType, pushable=False):
		self.coords = coords
		self.pushable = pushable
		self.world = None
		
	def addtoWorld(self, world):
		self.world = world
			
# Define a box which occupies a square in the world
# 	(i, j) : position
			
class box(object):
	def __init__(self, coords, pushable=False):				
		object.__init__(self, coords, 1, pushable)


# Define a robot which occupies a square in the world
#	(i, j)	: position
#	d 		: distance vision
		
class robot(object):
	def __init__(self, coords=(0,0), d=1):
		object.__init__(self, coords, 2)
		self.d = d
		self.sensors = -np.ones(4)
	
	# Move the robot 1 square UP in the world
	def move1UP(self):
		self.world.updateObjectPosition(self, tuple(np.add(self.coords, (-1,0))))
		self.updateSensors()
	
	# Move the robot 1 square DOWN in the world
	def move1DOWN(self):
		self.world.updateObjectPosition(self, tuple(np.add(self.coords, (1,0))))
		self.updateSensors()
	
	# Move the robot 1 square LEFT in the world
	def move1LEFT(self):
		self.world.updateObjectPosition(self, tuple(np.add(self.coords, (0,-1))))
		self.updateSensors()
	
	# Move the robot 1 square RIGHT in the world
	def move1RIGHT(self):
		self.world.updateObjectPosition(self, tuple(np.add(self.coords, (0,1))))
		self.updateSensors()
	
	# Array sensors contains the output of the 4 robot's sensors (1 on, -1 off)
	# 	sensors[0] : Top sensor
	#	sensors[1] : Bottom sensor
	#	sensors[2] : Left sensor
	#	sensors[3] : Right sensor
	def updateSensors(self):
		self.sensors = -np.ones(4)
		for v in range(1, self.d+1):
			if self.coords[0]>0 and self.world.M[tuple(np.mod(np.add(self.coords, (-v,0)), (self.world.nRows,self.world.nCols)))] is not None:
				self.sensors[0] = 1
			elif self.coords[0]<self.world.nRows-1 and self.world.M[tuple(np.mod(np.add(self.coords, (v,0)), (self.world.nRows,self.world.nCols)))] is not None:
				self.sensors[1] = 1
			elif self.coords[1]>0 and self.world.M[tuple(np.mod(np.add(self.coords, (0,-v)), (self.world.nRows,self.world.nCols)))] is not None:
				self.sensors[2] = 1
			elif self.coords[1]<self.world.nCols-1 and self.world.M[tuple(np.mod(np.add(self.coords, (0,v)), (self.world.nRows,self.world.nCols)))] is not None:
				self.sensors[3] = 1
	
	# Overrides addtoWorld
	def addtoWorld(self, world):
		object.addtoWorld(self, world)
		self.updateSensors()
		
								
											
# Define a 2D world nRows x nCols
class world:
	def __init__(self, nRows, nCols, periodic=True):	
		self.nRows = nRows
		self.nCols = nCols
		self.periodic = periodic
		self.M = np.empty((nRows, nCols), dtype=object)
	
	# Place an object in the world
	def addObject(self, obj):
		obj.coords = tuple(np.array(obj.coords) % np.array((self.nRows,self.nCols)))
		self.M[obj.coords] = obj
		obj.addtoWorld(self)
	
	# Update the position of an object int he world
	def updateObjectPosition(self, obj, newCoords):
		if self.periodic :
			newCoords = tuple(np.array(newCoords) % np.array((self.nRows,self.nCols)))
		else:
			if newCoords[0] >= self.nRows:
				newCoords = (self.nRows-1, newCoords[1])
			elif newCoords[0] < 0:
				newCoords = (0, newCoords[1])
			if newCoords[1] >= self.nCols:
				newCoords = (newCoords[0], self.nCols-1)
			elif newCoords[1] < 0:
				newCoords = (newCoords[0], 0)
		newSquare = self.M[newCoords]		# Object placed at new square
		if newSquare is None:
			self.M[obj.coords] = None
			self.M[newCoords] = obj
			obj.coords = newCoords
		elif newSquare.pushable:
		# Push the object and take the square	
			push = tuple(np.subtract(newSquare.coords, obj.coords))
			pushedPosition = np.array(np.add(newSquare.coords,push))
			if self.periodic:
				newSquare.coords = tuple(pushedPosition % np.array((self.nRows,self.nCols)))
			else:
				objectWillBePushed = True
				if pushedPosition[0] >= self.nRows:
					pushedPosition[0] = self.nRows-1
					objectWillBePushed = False
				elif pushedPosition[0] < 0:
					pushedPosition[0] = 0
					objectWillBePushed = False
				if pushedPosition[1] >= self.nCols:
					pushedPosition[1] = self.nCols-1
					objectWillBePushed = False
				elif pushedPosition[1] < 0:
					pushedPosition[1] = 0
					objectWillBePushed = False
			
			if objectWillBePushed:
				self.M[newSquare.coords] = newSquare
				self.M[newCoords] = obj
				self.M[obj.coords] = None
				obj.coords = newCoords
			
		
