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
			
# Define a box which occupies a square in the map
# 	(i, j) : position
			
class box(object):
	def __init__(self, coords, pushable=False):				
		object.__init__(self, coords, 1, pushable)


# Define a robot which occupies a square in the map
#	(i, j)	: position
#	d 		: distance vision
		
class robot(object):
	def __init__(self, coords, d):
		object.__init__(self, coords, 2)
		self.d = d
	
	# Move the robot 1 square UP in the world
	def move1UP(self):
		self.world.updateObjectPosition(self, tuple(np.add(self.coords, (-1,0))))
	
	# Move the robot 1 square DOWN in the world
	def move1DOWN(self):
		self.world.updateObjectPosition(self, tuple(np.add(self.coords, (1,0))))
	
	# Move the robot 1 square LEFT in the world
	def move1LEFT(self):
		self.world.updateObjectPosition(self, tuple(np.add(self.coords, (0,-1))))
	
	# Move the robot 1 square RIGHT in the world
	def move1RIGHT(self):
		self.world.updateObjectPosition(self, tuple(np.add(self.coords, (0,1))))
	
	# Array sensors contains the output of the 4 robot's sensors (1 on, -1 off)
	# 	sensors[0] : Top sensor
	#	sensors[1] : Bottom sensor
	#	sensors[2] : Left sensor
	#	sensors[3] : Right sensor
	def updateSensors(self):
		self.sensors = -np.ones(4)
		for v in range(1, self.d+1):
			if self.coords[0]>0 and self.world.M[tuple(np.add(self.coords, (-v,0)))] is not None:
				self.sensors[0] = 1
			elif self.coords[0]<self.world.nRows-1 and self.world.M[tuple(np.add(self.coords, (v,0)))] is not None:
				self.sensors[1] = 1
			elif self.coords[1]>0 and self.world.M[tuple(np.add(self.coords, (0,-v)))] is not None:
				self.sensors[2] = 1
			elif self.coords[1]<self.world.nCols-1 and self.world.M[tuple(np.add(self.coords, (0,v)))] is not None:
				self.sensors[3] = 1
			
								
											
# Define a 2D world nRows x nCols
class world:
	def __init__(self, nRows, nCols):	
		self.nRows = nRows
		self.nCols = nCols
		self.M = np.empty((nRows, nCols), dtype=object)
	
	# Place an object in the world
	def addObject(self, obj):
		obj.coords = (obj.coords[0] % self.nRows, obj.coords[1] % self.nCols)
		self.M[obj.coords] = obj
		obj.world = self
	
	# Update the position of an object int he world
	def updateObjectPosition(self, obj, newCoords):
		newCoords = (newCoords[0] % self.nRows, newCoords[1] % self.nCols)
		newSquare = self.M[newCoords]		# Object placed at new square
		if newSquare is None:
			self.M[obj.coords] = None
			self.M[newCoords] = obj
			obj.coords = newCoords
		elif newSquare.pushable:
		# Push the object and take the square	
			push = tuple(np.subtract(newSquare.coords, obj.coords))
			newSquare.coords = tuple(np.add(newSquare.coords,push))
			self.M[newSquare.coords] = newSquare
			self.M[newCoords] = obj
			self.M[obj.coords] = None
			obj.coords = newCoords
			
		
