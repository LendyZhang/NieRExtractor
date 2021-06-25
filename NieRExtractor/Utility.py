# Utilities for NieR Extractor.
# Copyright (C) 2021 EMAX Studio, all rights reserved.

class Vector3:
	r""" Three-dimensional vector.
	"""

	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0



class AABB3:
	r""" Three-dimensional axis-aligned bounding box.
	"""

	def __init__(self):
		self.minimum = Vector3()
		self.maximum = Vector3()



class Transform3:
	r""" Three-dimensional transformation.
	"""

	def __init__(self):
		self.position = Vector3()
		self.rotation = Vector3()
		self.scale = Vector3()
