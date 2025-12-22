##IMPORTS

__all__ = [
	"FILE_MANAGER",
]

class fileInfo:
	def __init__(self, ):
		self._rootFolder = "Data/Local_Notes/" ##Default root
		self._fileName = ""
		self._fileLocation = self._rootFolder+self._fileName
	
	def changeRootDirectory(self, ):#rootFolder:str, title:str):
		## Opens a file manager pop-up
		## Records the folder that was selected
		## Changes ._rootFolder accordingly.
		## Updates ._fileLocation
		pass

	def changeFileName(self, newName:str):
		## RESEARCH: Does python have built in methods to change file names
		## If not, Save current file to a "cache"
		## Remove old file
		## Create New file with name: "newName"
		## Write "cache" to file
		## Save & Close file.
		## Update ._fileName & ._fileLocation
		pass

	def set_fileLocation(self, newName:str):
		self._fileName = newName
		self._fileLocation = self._rootFolder + newName
	
	def set_noteBlock(self, object):
		self._noteBlock = object
	
	def get_fileLocation(self):
		return self._fileLocation

class FILE_MANAGER(fileInfo):
	def __init__(self):
		fileInfo.__init__(self)
		pass

	def saveNote(self, ):
		pass

	def openNote(self, ):
		pass
	