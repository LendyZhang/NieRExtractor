# Utility for importing mesh data from WMB file.
# Copyright (C) 2021 EMAX Studio, all rights reserved.

import os
import sys
import struct
import Utility

class Bone:
	r""" Describes a bone in the skeleton.
	"""

	def __init__(self):
		self.localTransform = Transform3()
		self.worldTransform = Transform3()



class Skeleton:
	r""" Describes a skeleton in the mesh.
	"""

	def __init__(self):
		self.boneCount = 0
		self.bones = []



class Mesh:
	r""" Describes a mesh.
	"""

	def __init__(self):
		self.boundingBox = Utility.AABB3()
		self.skeleton = Skeleton()
		self.subMeshCount = 0
		self.subMeshes = []

	def Import(self, fileObject):
		pass



class WMBImporter:
	r""" Utility for importing mesh data from WMB file.
	"""

	def __init__(self):
		pass

	def _ParseHeader(self, fo):

	def _ReadFloat(self, fo):
		return struct.unpack('<f', fo.read(4))[0]

	def _ReadInt(self):
		return struct.unpack('<i', fo.read(4))[0]
