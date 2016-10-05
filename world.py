import numpy as np
from abc import ABCMeta, abstractmethod

# Objects in the World
class object:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, i, j, nType, pushable=False):
		self.i = i
		self.j = j
		self.pushable = pushable
		self.world = None
			


# Define a box which occupies a square in the map
# 	(i, j) : position
			
class box(object):
	def __init__(self, i, j, pushable=False):				
		object.__init__(self, i, j, 1, pushable)


# Define a robot which occupies a square in the map
#	(i, j)	: position
#	d 		: distance vision
		
class robot(object):
	def __init__(self, i, j, d):
		object.__init__(self, i, j, 2)
		self.d = d
		
	def move1UP(self):
		self.world.updateObjectPosition(self, self.i-1, self.j)
		
	def move1DOWN(self):
		self.world.updateObjectPosition(self, self.i+1, self.j)
		
	def move1LEFT(self):
		self.world.updateObjectPosition(self, self.i, self.j-1)
		
	def move1RIGHT(self):
		self.world.updateObjectPosition(self, self.i, self.j+1)
	
	# Array sensors contains the output of the 4 robot's sensors (1 on, -1 off)
	# 	sensors[0] : Top sensor
	#	sensors[1] : Bottom sensor
	#	sensors[2] : Left sensor
	#	sensors[3] : Right sensor
	def updateSensors(self):
		self.sensors = -np.ones(4)
		print self.world.M
		for v in range(1, self.d+1):
			if self.i>0 and self.world.M[self.i - v, self.j] is not None:
				self.sensors[0] = 1
			elif self.i<self.world.nRows-1 and self.world.M[self.i + v, self.j] is not None:
				self.sensors[1] = 1
			elif self.j>0 and self.world.M[self.i, self.j - v] is not None:
				self.sensors[2] = 1
			elif self.j<self.world.nCols-1 and self.world.M[self.i, self.j + v] is not None:
				self.sensors[3] = 1
			
								
											
# Define a 2D world nRows x nCols
class world:
	def __init__(self, nRows, nCols):	
		
		self.nRows = nRows
		self.nCols = nCols
		self.M = np.empty((nRows, nCols), dtype=object)
		
	def addObject(self, obj):
		obj.i %= self.nRows
		obj.j %= self.nCols
		self.M[obj.i, obj.j] = obj
		obj.world = self
		
	def updateObjectPosition(self, obj, newI, newJ):
		newI %= self.nRows
		newJ %= self.nCols
		if self.M[newI, newJ] is None:
			self.M[obj.i, obj.j] = None
			self.M[newI, newJ] = obj
			obj.i = newI
			obj.j = newJ
		#~ elif self.M[newI, newJ].pushable:
		# TODO: Push the object and take the square	
				
		
