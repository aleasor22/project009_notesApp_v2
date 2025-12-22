##IMPORTS
import tkinter
import tkinter.font as tkFont
from .textEditor import TEXT_EDITOR
from .noteObject import *

##EXPORTS
__all__ = [
	"DOCUMENT",
]

class DOCUMENT(STICKY_NOTE, TEXT_EDITOR):
	def __init__(self, parent):
		##Private Variables
		self.__parent = parent
		self.__canvasObject = tkinter.Canvas(parent, bg="gray")
		self.__titleExists = False
		TEXT_EDITOR.__init__(self, self.__canvasObject, "Canvas-#0", 16)

		##Canvas IDs
		self.__titleBlockZone	 = [0, 0, 250, 80]
		self.__titleZoneCanvasID = self.__canvasObject.create_rectangle(self.__titleBlockZone) ##Rough outline of where the title block goes. 
		self.__titleLinePosition = [20, 70, 230, 70]
		self.__titleLineCanvasID = self.__canvasObject.create_line(self.__titleLinePosition)
	
		##Public Variables
		self.title = None
		self.date = None
		self.time = None
		self.titleActive = False

		##Setting up Canvas Object
		self.__canvasObject.grid(column=0, row=0, sticky="NSWE")
		self.__parent.columnconfigure(0, weight=10)
		self.__parent.rowconfigure(0, weight=10)
		
		#CUSTOM SETUPS
		self.createTitleBlock()
	
	def get_canvasObj(self):
		return self.__canvasObject
	
	def clearDocWorkspace(self):
		print("Need to get All active Canvas IDs")
		# self.__noteBlock.clearScreen()
		with open(self._fileManager.get_fileLocation(), "w") as file:
			file.write("")
	
	def createTitleBlock(self, ):
		if not self.isListening and not self.__titleExists:
			self._textCanvasID = self.__canvasObject.create_text(self.__titleLinePosition[0], self.__titleLinePosition[1]-self.myFontHeight-10, anchor="nw", font=(self.myFont, self.myFontSize))
			self.__titleExists = True

	def onClick(self, event):
		if self.__titleBlockZone[0] <= event.x and event.x <= self.__titleBlockZone[2]:
			if self.__titleBlockZone[1] <= event.y and event.y <= self.__titleBlockZone[3]:
				# print("INSIDE TITLE BLOCK")
				self.createTitleBlock() ##Creates title block text, otherwise
				self.start_Listening()
				self.titleActive = True
			else:
				self.stop_Listening()
				self.titleActive = False
		else:
			self.stop_Listening()
			self.titleActive = False


##BELOW WILL BE MIGRATED INTO "DOCUMENT" CLASS
# class STICKY_NOTE:
# 	"""This Handles Instances of the Note Widget"""
# 	def __init__(self, parent):
# 		self.__parent = parent ##Parent Canvas Object
# 		self.__root = parent.get_canvasObj() ##Allows the program to know what canvas item to place to
# 		self._activeNoteName = ""		##The name of the note that's in focus
# 		self._activeNoteMove = False	##True when a box is being moved
# 		self.dictOfNotes = {}			##Key == bbox of a text box

# 	def onClick(self, event):
# 		# if not self._activeNoteMove:
# 		# 	for object in self.dictOfNotes.values():
# 		# 		if object.withinTopOfBox(event):
# 		# 			self.__root.bind("<Motion>", object.moveBox)
# 		# 			self._activeNoteName = object.myID
# 		# 			self._activeNoteMove = True
# 		print(self.__parent.titleActive, "Parent Title Active?")
# 		if not self.__parent.titleActive: ##Prevents making a new Note when clicking on title block
# 			if self._activeNoteName == "": ##Checks if a note is active
# 				if len(self.dictOfNotes) > 0:
# 					self.edit_note(event)
# 					if self._activeNoteName == "":
# 						self.create_note(event)
# 				else:
# 					self.create_note(event)
# 			else:
# 				##Clears the active note if outside of bounds
# 				if not self.dictOfNotes[self._activeNoteName].withinBounds(event):
# 					self.dictOfNotes[self._activeNoteName].stop_Listening()
# 					self.dictOfNotes[self._activeNoteName].active = False
# 					self._activeNoteName = ""
# 					##Checks to see if another note was clicked. Only after clicking off the previously active note
# 					self.edit_note(event) ##Tries to edit first
# 					if self._activeNoteName == "":
# 						self.create_note(event) ##If no edits, create a new note instead
		
# 			##For Debuging
# 			print(f"Active Note: {self._activeNoteName}")
# 			print(f"Active Move: {self._activeNoteMove}")
# 		else:
# 			##Makes sure all other notes aren't listening for key presses
# 			for value in self.dictOfNotes.values():
# 				value.stop_Listening()
# 				value.active = False

	
# 	def clearScreen(self):
# 		for values in self.dictOfNotes.values():
# 			values.deleteCanvasIDs()
# 		self.dictOfNotes = {}
# 		self._activeNoteName = ""

	##NOTE: this may migrate into "STICKY_NOTE" class
# 	def create_note(self, event):
# 		print("Creating a new Note")
# 		##Fills in Default Data
# 		newKey = f"Note-#{len(self.dictOfNotes)}"
# 		self.dictOfNotes[newKey] = noteWidget(self.__root, newKey)
# 		self.dictOfNotes[newKey].newNote(event)
# 		self.dictOfNotes[newKey].active = True
# 		self._activeNoteName = newKey

	##NOTE: this may migrate into "STICKY_NOTE" class
# 	def edit_note(self, event):
# 		##Determins if a note is to become active
# 		for key in self.dictOfNotes.keys():
# 			if self.dictOfNotes[key].withinBounds(event):
# 				print(f"Edit this box: dictOfNotes[{key}] = {self.dictOfNotes[key]}")
# 				self.dictOfNotes[key].active = True
# 				self._activeNoteName = key
# 				break

# 		##Reactivate the keyboard listener.
# 		if self._activeNoteName != "":
# 			self.dictOfNotes[self._activeNoteName].start_Listening()