##IMPORTS
from Data import LINKED_LIST

##EXPORTS
__all__ = [
	"FILES",
]

class fileInfo:
	def __init__(self, fileName:str):
		self.__rootFolder = "Data/Local_Notes/" ##Default root
		self.__fileName = fileName
		self.__fileExtension = ".csv"
		self.__fileLocation = self.__rootFolder+self.__fileName+self.__fileExtension
	
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
		self.__fileName = newName
		self.__fileLocation = self._rootFolder + newName + self.__fileExtension
	
	def get_fileLocation(self):
		return self.__fileLocation

class FILES(fileInfo):
	def __init__(self, fileName:str):
		fileInfo.__init__(self, fileName)
		self.__myFile = None

	def createFile(self):
		if self.__myFile == None:
			self.__myFile = open(self.get_fileLocation(), "w")
		else:
			print("A file is already in use.")

	def closeFile(self):
		if self.__myFile != None:
			self.__myFile.close()
		self.__myFile = None

	def writeDocumentTitle(self, title):
		self.__myFile.write(f"{title}\n")

	def writeContentsToFile(self, contents:str, drawnBox:list):
		##Write contents to file
		for char in contents:
			if  char == "\n":
				self.__myFile.write(",")
				continue
			self.__myFile.write(char)
		self.__myFile.write(",:END,")

		##Write the visual box to file
		for coord in drawnBox:
			self.__myFile.write(f"{coord},")
		self.__myFile.write(":ENDLINE\n")

	def readFile(self, ):
		linkedList = LINKED_LIST()
		with open(self.get_fileLocation()) as file:
			currWord = ""
			for line in file:
				for char in line:
					if char == "," or char == "\n":
						linkedList.add_tail(currWord)
						currWord = ""
						continue
					currWord += char
		# linkedList.printList()

		return linkedList
				


	# def open(self):
	# 	# self.__noteblock.clearScreen()
	# 	dictOfNotes = self.__noteBlock.dictOfNotes
	# 	stepCount = 0
	# 	with open(self.__fileLocation) as file:
	# 		currWord = ""
	# 		for line in file:
	# 			if (line[0]+line[1] != "//"):
	# 				newKey = f"Note-#{len(dictOfNotes)}"
	# 				dictOfNotes[newKey] = noteWidget(self._activeCanvas, newKey)
	# 				for char in line:
	# 					if char == "," or char == "\n":
	# 						# currWord += ","
	# 						dictOfNotes[newKey].get_myLinkedList().add_tail(currWord)
	# 						# stepCount = dictOfNotes[newKey].loadFromFile(stepCount, currWord)
	# 						currWord = ""
	# 						continue
	# 					currWord += char
	# 				dictOfNotes[newKey].loadFromFile()
	# 				# print(f"\nPost Creation - {newKey}: \n>>", end=" ")
	# 				# dictOfNotes[newKey].get_myLinkedList().printList()

	# 