##IMPORTS
import tkinter
import tkinter.font as tkFont
from .textEditor import TEXT_EDITOR
from .noteObject import *

##EXPORTS
__all__ = [
	"DOCUMENT",
]

class DOCUMENT(TEXT_EDITOR):
	def __init__(self, root, ID:str):
		"""Creates a workspace that allows the user to write notes to screen. Requires the root Tkinter Object"""
		##Canvas Variables
		self.__parent = root ##The Root Tkinter object
		self.__canvasObject = tkinter.Canvas(root, bg="gray")
		TEXT_EDITOR.__init__(self, self.__canvasObject, ID, 16)

		##Sticky Note Varibles
		self.existingNotes = {}
		self._activeNoteName = ""		##The name of the note that's in focus
		self._activeNoteMove = False	##True when a box is being moved

		##Canvas IDs
		self.__titleBlockZone	 = [0, 0, 250, 80]
		self.__titleZoneCanvasID = self.__canvasObject.create_rectangle(self.__titleBlockZone) ##Rough outline of where the title block goes. 
		self.__titleLinePosition = [20, 70, 230, 70]
		self.__titleLineCanvasID = self.__canvasObject.create_line(self.__titleLinePosition)
	
		##Public Variables
		self.myID = ID
		self.title = None
		self.date = None
		self.time = None
		
		##Setting up Canvas Object
		self.__canvasObject.grid(column=0, row=0, sticky="NSWE")
		self.__parent.columnconfigure(0, weight=10)
		self.__parent.rowconfigure(0, weight=10)
		
		#CUSTOM SETUPS
		self._textCanvasID = self.__canvasObject.create_text(self.__titleLinePosition[0], self.__titleLinePosition[1]-self.myFontHeight-10, anchor	= "nw",	font	= (self.myFont, self.myFontSize))

	##SETUP METHODS
	def onClick(self, event):
		if self.withinTitleBlock(event):
			print("Edit the Title Block")
			##Set Title Block as active
			self.start_Listening()

			##De-activate Current Sticky Note.
			self.existingNotes[self._activeNoteName].stop_Listening()
			self.existingNotes[self._activeNoteName].active = False
			self._activeNoteName = ""
		else:
			print("Create/Edit a Note")
			self.stop_Listening()

			##Handles the Sticky Notes
			newKey = f"Note-#{len(self.existingNotes)}"
			if (len(self.existingNotes) > 0):
				for value in self.existingNotes.values():
					if value.withinBounds(event):
						self._activeNoteName = value.myID
						value.active = True ##Sets note as active
						value.start_Listening() ##Allows editing the note
						break
					else:
						self._activeNoteName = ""
						value.stop_Listening()
						value.active = False
				
				if self._activeNoteName == "":
					self.existingNotes[newKey] = STICKY_NOTE(self.__canvasObject, newKey)
					self.existingNotes[newKey].createNote(event) ##Creates a blank note & Sets it as active
					self._activeNoteName = newKey
			else:
				self.existingNotes[newKey] = STICKY_NOTE(self.__canvasObject, newKey)
				self.existingNotes[newKey].createNote(event) ##Creates a blank note & Sets it as active
				self._activeNoteName = newKey
			
		
			##For Debuging
			# print(f"Existing Notes: {self.existingNotes}")
			print(f"Active Note: {self._activeNoteName}")
			# print(f"Active Move: {self._activeNoteMove}")

	##EVENT METHODS	
	def clearWorkspace(self):
		for value in self.existingNotes.values():
			value.deleteCanvasIDs()
		self.existingNotes = {}

	##GETTERS/SETTERS
	def withinTitleBlock(self, event):
		if self.__titleBlockZone[0] <= event.x and event.x <= self.__titleBlockZone[2]:
			if self.__titleBlockZone[1] <= event.y and event.y <= self.__titleBlockZone[3]:
				return True
		return False
	
	def get_canvasObj(self):
		return self.__canvasObject