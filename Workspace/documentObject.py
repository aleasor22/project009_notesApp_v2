##IMPORTS
import tkinter
import tkinter.font as tkFont
from .textEditor import TEXT_EDITOR
from .fileManager import FILES
from .noteObject import *

##EXPORTS
__all__ = [
	"DOCUMENT",
]

class DOCUMENT(TEXT_EDITOR, FILES):
	def __init__(self, root, ID:str, width):
		"""Creates a workspace that allows the user to write notes to screen. Requires the root Tkinter Object"""
		##Canvas Variables
		self.__parent = root ##The Root Tkinter object
		self.__canvasObject = tkinter.Canvas(root, bg="gray", width=(width * 0.85))
		TEXT_EDITOR.__init__(self, self.__canvasObject, ID, 16)
		FILES.__init__(self, "divider1")

		##Sticky Note Varibles
		self.existingNotes = {}			##The Sticky_Note object with associatedd Key
		self._activeNoteName = ""		##The name of the note that's in focus
		self._activeNoteMove = False	##True when a box is being moved
		self.__GLOBAL_MOVE_ID = ""

		##Canvas IDs
		self.__titleBlockZone	 = [0, 0, 250, self._myFontHeight+40]
		self.__titleZoneCanvasID = self.__canvasObject.create_rectangle(self.__titleBlockZone) ##Rough outline of where the title block goes. 
		self.__titleLinePosition = [20, self._myFontHeight+30, 230, self._myFontHeight+30]
		self.__titleLineCanvasID = self.__canvasObject.create_line(self.__titleLinePosition)
	
		##Public Variables
		self.myID = ID
		self.date = None
		self.time = None
		self.activeDoc = False
		self.lastTitle = "Blank"
		
		##Setting up Canvas Object
		self.__canvasObject.grid(column=0, row=1, sticky="NSWE")
		self.__parent.columnconfigure(0, weight=10)
		self.__parent.rowconfigure(1, weight=10)
		
		#CUSTOM SETUPS
		self._textCanvasID = self.__canvasObject.create_text(self.__titleLinePosition[0], self.__titleLinePosition[1]-self._myFontHeight-10, anchor	= "nw",	font=self.get_myFontPackage())

	##EVENT METHODS	
	def onClick(self, event):
		if self.withinTitleBlock(event):
			print("Edit the Title Block")
			##Set Title Block as active
			if not self.isListening:
				self.start_keyboard()

			##De-activate Current Sticky Note.
			if self._activeNoteName != "":
				self.existingNotes[self._activeNoteName].stop_keyboard()
				self.existingNotes[self._activeNoteName].active = False
				self._activeNoteName = ""
		else:
			# print("Create/Edit a Note")
			self.stop_keyboard()

			##Refresh Dictionary
			for key, value in self.existingNotes.items():
				if value.toBeDeleted:
					# print(f"Deleted key: {key}")
					del self.existingNotes[key]
					break

			##Handles the Sticky Notes
			newKey = f"Note-#{len(self.existingNotes)}"
			keyCounter = 0
			#if new key already exists make a different one till it's not in existing.
			while newKey in self.existingNotes.keys():
				newKey = f"Note-#{keyCounter}"
				keyCounter += 1
			
			print("Notes Dict", self.existingNotes)
			if (len(self.existingNotes) > 0):
				self._activeNoteName = ""
				for value in self.existingNotes.values():
					if value.withinBounds(event):
						print(f"Editing Note: {value.myID}")
						self._activeNoteName = value.myID
						value.active = True ##Sets note as active
						value.start_keyboard() ##Allows editing the note
					else:
						value.active = False
						value.stop_keyboard()

				if self._activeNoteName == "": ##If a note's not getting edited
					print(f"Creating New Note: {newKey}")
					self.createNote(newKey, event)
			else:
				print(f"Creating New Note: {newKey}")
				self.createNote(newKey, event)
					
			##For Debuging
			# print(f"Existing Notes: {self.existingNotes}")
			print(f"Active Note: {self._activeNoteName}")
			# print(f"Active Move: {self._activeNoteMove}")
	
	def manualChangeWidth(self, mousePos):
		for value in self.existingNotes.values():
			if (value.withinSideOfBox(mousePos) or value.activeWidthChange) and value.myID == self.__GLOBAL_MOVE_ID:
				print(f"within right side of note: {value.myID}")
				self.__canvasObject.config(cursor="sb_h_double_arrow")
				value.pressHoldWidthChange(mousePos)
			elif value.withinSideOfBox(mousePos) and not value.activeWidthChange and self.__GLOBAL_MOVE_ID == "":
				self.__GLOBAL_MOVE_ID = value.myID
	
	def manualWidthOff(self):
		for value in self.existingNotes.values():
			value.activeWidthChange = False
		self.__canvasObject.config(cursor="arrow")
		self.__GLOBAL_MOVE_ID = ""

	def noteMove(self, mousePos=None):
		for value in self.existingNotes.values():
			if (value.withinTopOfBox(mousePos) or value.activeMove) and value.myID == self.__GLOBAL_MOVE_ID:
				print(f"within note: {value.myID}")
				self.__canvasObject.config(cursor="fleur")
				value.pressHoldBoxMove(mousePos)
			elif value.withinTopOfBox(mousePos) and not value.activeMove and self.__GLOBAL_MOVE_ID == "":
				self.__GLOBAL_MOVE_ID = value.myID
	
	def noteMoveOff(self):
		for value in self.existingNotes.values():
			value.activeMove = False
		self.__canvasObject.config(cursor="arrow")
		self.__GLOBAL_MOVE_ID = ""

	def createNote(self, newKey, event):
		self.existingNotes[newKey] = STICKY_NOTE(self.__canvasObject, newKey)
		self.existingNotes[newKey].createNote(event) ##Creates a blank note & Sets it as active
		self._activeNoteName = newKey
	
	def clearWorkspace(self):
		for value in self.existingNotes.values():
			value.deleteCanvasIDs()
		self.existingNotes = {}
	
	def saveDocument(self, event=None):
		print("Saving Document")
		##Creating File
		self.createFile()

		##Writing to file
		self.writeDocumentTitle(self._contents)
		for stickyNote in self.existingNotes.values():
			self.writeContentsToFile(stickyNote.get_contents(), stickyNote.myBbox)
		
		##Closing file after writting
		self.closeFile()
	
	def openDocument(self):
		dataFromFile = self.readFile()

		##Sets Title.
		self._contents = dataFromFile.head.data
		self.__canvasObject.itemconfigure(self._textCanvasID, text=self._contents)
		
		##Sets Sticky Notes
		curr = dataFromFile.head.next
		##Create the first one
		newKey = f"Note-#{len(self.existingNotes)}"
		self.existingNotes[newKey] = STICKY_NOTE(self.__canvasObject, newKey)

		while curr != None:
			if curr.data == ":ENDLINE" and curr.next != None:
				newKey = f"Note-#{len(self.existingNotes)}"
				self.existingNotes[newKey] = STICKY_NOTE(self.__canvasObject, newKey)
			else:
				self.existingNotes[newKey].loadFromFile(curr)
			curr = curr.next
				
		for value in self.existingNotes.values():
			# print(f"{value.myID} will be drawn to screen")
			value.drawToScreen()

	##GETTERS/SETTERS
	def withinTitleBlock(self, event):
		if self.__titleBlockZone[0] <= event.x and event.x <= self.__titleBlockZone[2]:
			if self.__titleBlockZone[1] <= event.y and event.y <= self.__titleBlockZone[3]:
				# print(f"Within Block: {self.myID}")
				return True
		return False
	
	def get_canvasObj(self):
		return self.__canvasObject
	
	def set_title(self, title:str):
		self._contents = title
		self.__canvasObject.itemconfigure(self._textCanvasID, text=title)

	def get_title(self):
		return self.get_contents()