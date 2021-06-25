# Utility for unpacking DAT archive of NieR: Automata.
# Author: Lendy Zhang <lendyzhang@gmail.com>
# Copyright (C) 2021 EMAX Studio, all rights reserved.

import os
import sys
import struct

class DATArchive:
	r""" DAT archive is the basic unit of the virtual file system in NieR: Automata.
	It contains the file allocation table and the contents of a group of files.
	This utility can be used to query information of the DAT archive, and extract files from it.
	"""

	def __init__(self):
		self.fileObject = None
		self.fileCount = 0
		self.fileTableOffset = 0
		self.extTableOffset = 0
		self.nameTableOffset = 0
		self.sizeTableOffset = 0
		self.files = []

	def Open(self, filePath):
		self.fileObject = open(filePath, 'rb')
		if self._ParseHeader():
			self._ParseFileTable()
			return True
		else:
			return False

	def _ParseHeader(self):
		if self.fileObject.read(4) == b'DAT\x00':
			self.fileCount = self._ReadInt()
			self.fileTableOffset = self._ReadInt()
			self.extTableOffset = self._ReadInt()
			self.nameTableOffset = self._ReadInt()
			self.sizeTableOffset = self._ReadInt()
			# Skip two unknown integers.
			self._ReadInt()
			self._ReadInt()
			return True
		else:
			print('Incorrect archive format.')
			return False

	def _ParseFileTable(self):
		self.fileObject.seek(self.fileTableOffset)
		for index in range(0, self.fileCount):
			datFile = DATFile(self)
			datFile.offset = self._ReadInt()
			self.files.append(datFile)

		self.fileObject.seek(self.extTableOffset)
		for index in range(0, self.fileCount):
			self.files[index].ext = self.fileObject.read(4).decode('ascii').rstrip('\x00')

		self.fileObject.seek(self.sizeTableOffset)
		for index in range(0, self.fileCount):
			self.files[index].size = self._ReadInt()

		self.fileObject.seek(self.nameTableOffset)
		nameAlignment = self._ReadInt()
		for index in range(0, self.fileCount):
			name = ''
			while True:
				partialName = self.fileObject.read(nameAlignment)
				name += partialName.decode('ascii').rstrip('\x00')
				if partialName[-1] == 0:
					break
			self.files[index].name = name

	def GetFileCount(self):
		return self.fileCount

	def PrintArchiveInfo(self):
		print('FileCount: %d' % self.fileCount)
		print('FileTableOffset: %08x' % self.fileTableOffset)
		print('ExtTableOffset: %08x' % self.extTableOffset)
		print('NameTableOffset: %08x' % self.nameTableOffset)
		print('SizeTableOffset: %08x' % self.sizeTableOffset)

	def PrintFileInfo(self, index):
		print('FileIndex: %d' % index)
		print('FileName: %s' % self.files[index].name)
		print('FileOffset: %08x' % self.files[index].offset)
		print('FileSize: %08x' % self.files[index].size)
		print('FileExt: %s' % self.files[index].ext)

	def PrintFileInfos(self):
		for index in range(0, self.fileCount):
			self.PrintFileInfo(index)

	def Extract(self, targetDir, unpackWTP=True):
		print('Extracting all files to %s...' % targetDir)
		for index in range(0, self.fileCount):
			self.files[index].Extract(targetDir, unpackWTP)

	def _ReadFloat(self):
		return struct.unpack('<f', self.fileObject.read(4))[0]

	def _ReadInt(self):
		return struct.unpack('<i', self.fileObject.read(4))[0]

class DATFile:
	r""" Describes a file in DAT archive.
	"""

	def __init__(self, archive):
		self.archive = archive
		self.offset = 0
		self.ext = ''
		self.name = ''
		self.size = 0

	def Extract(self, targetDir, unpackWTP=True):
		if not os.path.exists(targetDir):
			os.makedirs(targetDir)

		fileObject = self.archive.fileObject
		fileObject.seek(self.offset)
		content = fileObject.read(self.size)

		print('Extracting %s...' % self.name, end='')
		fo = open(targetDir + '/' + self.name, 'wb')
		fo.write(content)
		fo.close()
		print('Done')

		if unpackWTP and self.ext == 'wtp':
			index = 0
			prevOffset = 0
			while True:
				print('Unpacking DDS file %d from %s...' % (index, self.name), end='')
				offset = content.find(b'DDS ', prevOffset + 4)
				fo = open(targetDir + '/' + self.name.replace('.wtp', '_%d.dds' % index), 'wb')
				fo.write(content[prevOffset:] if offset == -1 else content[prevOffset:offset])
				fo.close()
				print('Done')

				if offset == -1:
					break
				else:
					index += 1
					prevOffset = offset

def main():
	if len(sys.argv) > 2:
		ar = DATArchive()
		ar.Open(sys.argv[2])

		if sys.argv[1].casefold() == 'info':
			ar.PrintArchiveInfo()
			ar.PrintFileInfos()
			return

		elif sys.argv[1].casefold() == 'extract':
			targetDir = '.'
			if len(sys.argv) > 3:
				targetDir = sys.argv[3]
			ar.Extract(targetDir)
			return

	print('Utility for unpacking DAT archive of NieR: Automata.')
	print('')
	print('Usage: python3 DATUnpacker.py COMMAND [ARGUMENTS]')
	print('')
	print('Commands:')
	print('    info    Prints information of the specified archive.')
	print('            Example: python3 DATUnpacker.py info pl0000.dat')
	print('')
	print('    extract Extracts files in the specified archive to the specified directory.')
	print('            Example: python3 DATUnpacker.py extract pl0000.dat ./output')

if __name__ == '__main__':
	main()
