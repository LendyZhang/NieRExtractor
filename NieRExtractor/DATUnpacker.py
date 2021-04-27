# Utility for unpacking archive.
# Copyright (C) 2021 EMAX Studio, all rights reserved.

import os
import sys
import struct

class DATArchive:
	""" """
	class FileInfo:
		def __init__(self):
			self.offset = 0
			self.ext = ''
			self.name = ''
			self.size = 0

	def __init__(self):
		self.fileObject = None
		self.fileCount = 0
		self.fileTableOffset = 0
		self.extTableOffset = 0
		self.nameTableOffset = 0
		self.sizeTableOffset = 0
		self.fileInfos = []

	def Open(self, filePath):
		self.fileObject = open(filePath, 'rb')
		if self.ParseHeader():
			self.ParseFileInfos()
			return True
		else:
			return False

	def _ReadFloat(self):
		return struct.unpack('<f', self.fileObject.read(4))[0]

	def _ReadInt(self):
		return struct.unpack('<i', self.fileObject.read(4))[0]

	def ParseHeader(self):
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

	def ParseFileInfos(self):
		self.fileObject.seek(self.fileTableOffset)
		for index in range(0, self.fileCount):
			fi = self.FileInfo()
			fi.offset = self._ReadInt()
			self.fileInfos.append(fi)

		self.fileObject.seek(self.extTableOffset)
		for index in range(0, self.fileCount):
			self.fileInfos[index].ext = self.fileObject.read(4).decode('ascii')

		self.fileObject.seek(self.sizeTableOffset)
		for index in range(0, self.fileCount):
			self.fileInfos[index].size = self._ReadInt()

		self.fileObject.seek(self.nameTableOffset)
		nameAlignment = self._ReadInt()
		for index in range(0, self.fileCount):
			name = ''
			while True:
				partialName = self.fileObject.read(nameAlignment)
				name += partialName.decode('ascii')
				if partialName[-1] == 0:
					break
			self.fileInfos[index].name = name

	def GetFileCount(self):
		return self.fileCount

	def PrintArchiveInfo(self):
		print(
'''FileCount: %08x
FileTableOffset: %08x
ExtTableOffset:%08x
NameTableOffset:%08x
SizeTableOffset:%08x
'''%
			(self.fileCount, self.fileTableOffset, self.extTableOffset, self.nameTableOffset, self.sizeTableOffset)
		)

	def PrintFileInfo(self, index):
		print(
'''FileIndex: %d
FileName: %s
FileOffset: %08x
Size: %08x
Extension: %s
'''%
			(index, self.fileInfos[index].name, self.fileInfos[index].offset, self.fileInfos[index].size, self.fileInfos[index].ext)
		)

	def PrintFileInfos(self):
		for index in range(0, self.fileCount):
			self.PrintFileInfo(index)

class DATFile:
	def __init__(self, archive):
		pass

"""
def extract_file(fp, filename, FileOffset, Size, extract_dir):
	create_dir(extract_dir)
	fp.seek(FileOffset)
	FileContent = fp.read(Size)
	outfile = open(extract_dir + '/'+filename,'wb')
	print("extracting file %s to %s/%s"%(filename,extract_dir,filename))
	outfile.write(FileContent)
	outfile.close()
	if filename.find('wtp') > -1 :
		wtp_fp = open(extract_dir + '/'+filename,"rb")
		content = wtp_fp.read(Size)
		dds_group = content.split(b'DDS ')
		dds_group = dds_group[1:]
		for i in range(len(dds_group)):
			print("unpacking %s to %s/%s"%(filename,extract_dir ,filename.replace('.wtp','_%d.dds'%i)))
			dds_fp = open(extract_dir + '/'+filename.replace('.wtp','_%d.dds'%i), "wb")
			dds_fp.write(b'DDS ')
			dds_fp.write(dds_group[i])
			dds_fp.close()
		wtp_fp.close()
		#os.remove("%s/%s"%(extract_dir,filename))
	print("done")

def get_all_files(path):
	pass

def main(filename, extract_dir, ROOT_DIR):
	fp = open(filename,"rb")
	headers = read_header(fp)
	if headers:
		FileCount, FileTableOffset, ExtensionTableOffset,NameTableOffset,SizeTableOffset,UnknownOffset1C,Unknown20 = headers
		for i in range(FileCount):
			extract_dir_sub = ''
			index,Filename,FileOffset,Size,Extension = get_fileinfo(fp, i, FileTableOffset,ExtensionTableOffset, NameTableOffset,SizeTableOffset)
			if extract_dir != '':
				extract_dir_sub = extract_dir + '\\' + filename.replace(ROOT_DIR ,'') 
				extract_file(fp, Filename, FileOffset, Size, extract_dir_sub)


if __name__ == '__main__':
	extract_dir = ''
	dirname = ''
	useage = "\nUseage:\npython dat_unpacker.py your_dat_path your_extract_path"
	useage1 = "\nUseage:\nblender --background --python dat_unpacker.py your_dat_path your_extract_path"
	if len(sys.argv) < 3:
		print(useage)
		exit()
	if len(sys.argv) > 2:
		dir_name = sys.argv[1]
		extract_dir = sys.argv[2]
		print()
		if os.path.split(sys.argv[0])[-1].lower().find("blender") >-1:
			if len(sys.argv) < 6:
				print(useage1)
				exit()
			dir_name = sys.argv[4]
			extract_dir = sys.argv[5]
		if not os.path.exists(extract_dir):
			create_dir(extract_dir)
	ROOT_DIR = dir_name
	for dirpath,dirnames,filename in os.walk(dir_name):
		for file in filename:
			filename = "%s\%s"%(dirpath,file)
			main(filename, extract_dir, ROOT_DIR)
"""

if __name__ == '__main__':
	ar = DATArchive()
	ar.Open(sys.argv[1])
	ar.PrintArchiveInfo()
	ar.PrintFileInfos()
