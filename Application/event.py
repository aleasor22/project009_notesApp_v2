##IMPORTS
import tkinter
import tkinter.font as tkFont
from Data.File_Manager import FILE_MANAGER
from Workspace.noteObject import *

class EVENTS:
	"""Handles Most Events within the project"""
	def __init__(self):
		self._mainApp = None
		self._activeCanvas = None
		self.__noteBlock = None

		self._fileManager = FILE_MANAGER()
		self._fileManager.set_fileLocation("testing.csv")
		self._fileLocation = self._fileManager.get_fileLocation()

	def kill(self, event):
		self._mainApp.destroy()	
	
	def save(self): ##Using the CSV format (Comma Separated Values)
		dictOfNotes = self.__noteblock.dictOfNotes
		with open(self._fileLocation, "w") as file:
			for noteObj in dictOfNotes.values():
				if len(noteObj.get_contents()) == 0:
					##Ignores Empty Notes When Saving
					continue
				noteObj.saveToFile(file)

	def open(self):
		# self.__noteblock.clearScreen()
		dictOfNotes = self.__noteBlock.dictOfNotes
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


	##---Basic Methods & Getters/Setters---##
	def test(self): 
		##used to test events - Often a placeholder
		print("Event Tested")

	def get_activeCanvas(self):
		return self._activeCanvas
	
	def get_mainApp(self):
		return self._mainApp
	
	def set_noteBlock(self, data):
		self.__noteBlock = data

	def get_fileManager(self):
		return self._fileManager