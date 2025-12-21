##IMPORTS
from Note_Object.noteObject import noteWidget

__all__ = [
	"FILE_MANAGER",
]

class fileInfo:
	def __init__(self, ):
		self._rootFolder = "Data/Local_Notes/" ##Default root
		self._fileName = ""
		self._fileLocation = self._rootFolder+self._fileName

		self._noteBlock = None ##Note Block Object
	
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
	
	def save(self): ##Using the CSV format (Comma Separated Values)
		dictOfNotes = self._noteBlock.dictOfNotes
		with open(self._fileLocation, "w") as file:
			for noteObj in dictOfNotes.values():
				if len(noteObj.get_contents()) == 0:
					##Ignores Empty Notes When Saving
					continue
				noteObj.saveToFile(file)

	def open(self):
		# self._noteBlock.clearScreen()
		dictOfNotes = self._noteBlock.dictOfNotes
		stepCount = 0
		with open(self._fileLocation) as file:
			currWord = ""
			for line in file:
				if (line[0]+line[1] != "//"):
					newKey = f"Note-#{len(dictOfNotes)}"
					dictOfNotes[newKey] = noteWidget(self._activeCanvas, newKey)
					for char in line:
						if char == "," or char == "\n":
							# currWord += ","
							dictOfNotes[newKey].get_myLinkedList().add_tail(currWord)
							# stepCount = dictOfNotes[newKey].loadFromFile(stepCount, currWord)
							currWord = ""
							continue
						currWord += char
					dictOfNotes[newKey].loadFromFile()
					# print(f"\nPost Creation - {newKey}: \n>>", end=" ")
					# dictOfNotes[newKey].get_myLinkedList().printList()
