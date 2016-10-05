import numpy as np
from abc import ABCMeta, abstractmethod

# Objects in the World
class object:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, i, j, nType):
		self.i = i
		self.j = j
		self.nType = nType


# Define a box which occupies a square in the map
# 	(i, j) : position
			
class box(object):
	def __init__(self, i, j):				
		object.__init__(self, i, j, 1)


# Define a robot which occupies a square in the map
#	(i, j)	: position
#	d 		: distance vision
		
class robot(object):
	def __init__(self, i, j, d):
		object.__init__(self, i, j, 2)
		self.d = d		
								
											
# Define a 2D world nRows x nCols
class world:
	def __init__(self, nRows, nCols):	
		
		self.nRows = nRows
		self.nCols = nCols
		self.M = np.zeros((nRows, nCols))
		
	def addObject(self, obj):
		obj.i %= self.nRows
		obj.j %= self.nCols
		self.M[obj.i, obj.j] = obj.nType
		
