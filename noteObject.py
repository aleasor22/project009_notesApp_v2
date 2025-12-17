import tkinter
import tkinter.font as tkFont 
from pynput import keyboard
from PIL import ImageFont

__all__ = [
	"noteWidget",
	"noteBlock"
]

class noteWidget:
	"""Handles the Contents of an individual note"""
	def __init__(self, root, ID):
		self.__root = root
		##Start the Listenser
		self.__listener = None
		self.isListening = False
		self.myID = ID
		self.active = False

		##Text Widget Variables
		self.__textCanvasID = None
		self.__wrap = 200
		self._backSpaceActive = False  ##Tracks if the backspace  has been hit while editing text
		self.myFont = tkFont.nametofont("TkDefaultFont")
		self.myFontHeight = self.myFont.metrics('linespace')
		self.myFontLength = self.myFont.measure("")
		self.text_offset = 5

		##String Manipulations
		self._contents = ""
		self._currLine = 0
		self._contentLines = []
		self._longestLine  = 0
		self._contentLengthAtLine = {0:0}  

		##Text Box Widget Variables
		self.__moveCanvasID = None
		self.__boxCanvasID = None
		# self.coords  = (0, 0)       ##(x, y)
		self.myBbox = (0, 0, 0, 0) ##(x1, y1, x2, y2)
		self.box_offset_x = 20          ##The offset from original Top-Left position
		self.box_offset_y = 10


	def pressed(self, key):
		try:
			# print(f"Key Pressed: {key.char}") ##Used for Debug
			self._contents += key.char
		except AttributeError:
			# print(f"Key Pressed: {key}") ##Used for Debug
			if key == key.enter:
				self._contents += "\n"
				self._contentLengthAtLine[len(self._contentLengthAtLine)] = len(self._contents)
				self._contentLines.append(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
				self._currLine += 1
				print(self._contentLines, "append")
				self.adjustBox()
				
			if key == key.space:
				self._contents += " "
			if key == key.tab:
				self._contents += "\t"
			if key == key.backspace:
				self._backSpaceActive = True
				self.onBackSpace()
		finally:
			##This logic happens no mater the above results
			self.myFontLength = self.myFont.measure(self._contents) ##Updates Total length of String, NOTE: DOESN'T KNOW ABOUT WRAPING OR NEWLINE CHARACTER
			# print(f"Add new Key to screen: {key}")
			self.__root.itemconfigure(self.__textCanvasID, text=self._contents)
			
			self.adjustBox(expand="x-dir")

			##Resize box on wrap
			toWrap = self.myFont.measure(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
			if toWrap > self.__wrap and not self._backSpaceActive:
				self._contents += "\n"
				self._contentLengthAtLine[len(self._contentLengthAtLine)] = len(self._contents)
				self._contentLines.append(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
				self._currLine += 1
				print(self._contentLines, "append")
				self.adjustBox()
			else:
				##Only happens when my text width is under the wrap length
				self._backSpaceActive = False

	def released(self, key):
		try:
			temp = key.char
		except AttributeError:
			if key == key.f1:
				print(self._contents)
		finally:
			##This logic happens no mater the above results
			pass
	
	def onBackSpace(self, ):
		temp = self._contents
		if len(temp) > 0:
			self._contents = temp.rstrip(temp[len(self._contents)-1])
			
			if temp[len(self._contents)-1] == "\n":# and len(self._contents) > 0:
				self.adjustBox(-1)
				if len(self._contentLines) >= 0:
					self._contentLengthAtLine.popitem()
					self._contentLines.pop()
					self._currLine -= 1
					self.adjustBox(-1)
					print(self._contentLengthAtLine, "pop")
			else:
				self.adjustBox(-1, "x-dir")
			
			##Reset variables if self._contents string is empty
			if len(self._contents) == 0:
				self._contentLengthAtLine = {0:0}
				self._contentLines = []
				self._currLine = 0
				print(self._contentLengthAtLine, "pop")
	
	def newNote(self, event):
		self.myBbox = (event.x, event.y-10, event.x+int(self.__wrap/2)+self.box_offset_x, event.y+self.box_offset_y+self.myFontHeight)
		# self.coords = (event.x, event.y)
		
		##Creates Canvas Widgets 
		self.__moveCanvasID = self.__root.create_rectangle(event.x, self.myBbox[1], self.myBbox[2], event.y)
		self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
		self.__textCanvasID = self.__root.create_text(event.x+self.text_offset, event.y+self.text_offset, anchor="nw", font=self.myFont)#, width=100)
		self.start_Listening()

	def adjustBox(self, addOrRemove=1, expand="y-dir"):
		##Remove old Canvas ID
		self.__root.delete(self.__boxCanvasID)
		# print(f"Modifier: {addOrRemove}")

		##Create New Box
		if expand == "y-dir":
			self.myBbox = (self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[3]+(addOrRemove * self.myFontHeight))
		elif expand == "x-dir":
			self.__root.delete(self.__moveCanvasID)
			currentBoxWidth = (self.myBbox[2] - self.myBbox[0])

			##Need to Increase the width when the longest line is at 75% of current size, until max size reached
			atMaxSize = (currentBoxWidth >= self.__wrap+self.text_offset)
			increaseSize = (int(0.75 * currentBoxWidth))
			if self.longestLine() >= increaseSize and not atMaxSize:
				self.myBbox = (self.myBbox[0], self.myBbox[1], self.myBbox[2]+(self.myFont.measure(len(self._contents)-1)), self.myBbox[3])
				# print("Get Bigger")

			##Need to Decrease the width when the longest line is at 65% of current size, until min size reached
			atMinSize = (currentBoxWidth <= int(self.__wrap/2)+self.text_offset)
			decreaseSize = (int(0.6 * currentBoxWidth))
			if self.longestLine() >= decreaseSize and self._backSpaceActive and not atMinSize:
				self.myBbox = (self.myBbox[0], self.myBbox[1], self.myBbox[2]-(self.myFont.measure(len(self._contents)-1)), self.myBbox[3])
				# print("Get Smaller")

			##Re-Create top box
			self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)

		##Re-create box around text
		self.__boxCanvasID = self.__root.create_rectangle(self.myBbox)
		# self._lineCount += addOrRemove

	def stringWithinRange(self, lowerBound, upperBound):
		newString = ""
		for index in range(len(self._contents)):
			if lowerBound <= index and index <= upperBound:
				newString += self._contents[index]
			
			if index > upperBound:
				break
		
		return newString

	def longestLine(self):
		##Compare current line with other lines. Determine if the current is the longest
		maxLength = self.myFont.measure(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
		for line in self._contentLines:
			if maxLength < self.myFont.measure(line):
				maxLength = self.myFont.measure(line)
		return maxLength

	def withinBounds(self, event):
		##Retruns True if mouse was clicked inside a text box, else returns false
		if self.myBbox[0] < event.x and event.x < self.myBbox[2]:
			#Mouse Possition on Click is between x1 and x2
			if self.myBbox[1] < event.y and event.y < self.myBbox[3]:
				#Mouse Possition on click is between y1 and y2
				return True
		return False
	
	def withinTopOfBox(self, event):
		##Retruns True if mouse was clicked inside a text box, else returns false
		if self.myBbox[0] < event.x and event.x < self.myBbox[2]:
			#Mouse Possition on Click is between x1 and x2
			if self.myBbox[1] < event.y and event.y < self.myBbox[3]:
				# print("Within top of Box")
				return True
		return False

	def moveBox(self, event):
		##Remove previous Canvas Widgets
		self.__root.delete(self.__boxCanvasID)
		self.__root.delete(self.__textCanvasID)

		##Needs to move Box & Text with mouse
		# Event .x/.y is based on current mouse position
		# Re-Write these cordinates into the new my_bbox

		##Create New Canvas Widgets
		self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
		# self.__textCanvasID = self.__root.create_text(text=self._contents)
		
	def set_textID(self, ID):
		self.__textCanvasID = ID

	def set_boxID(self, ID):
		self.__boxCanvasID = ID

	def get_textID(self):
		return self.__textCanvasID

	def get_boxID(self):
		return self.__boxCanvasID

	def changeBBox(self, modds: list, addOrRemove: list):
		##Able to mainipulate the self.myBbox by changing one or all elements of the tuple
		##Dynamic in a way to know which elements to change
		##need to know if I'm increasing/decreasing, should this be in a list too?
		
		pass

	def start_Listening(self):
		"""Starts associated keyboard.listener thread"""
		self.__listener = keyboard.Listener(on_press=self.pressed, on_release=self.released)
		self.isListening = True
		self.__listener.start() ##Starts a tread to track for keyboards press/release actions

	def stop_Listening(self):
		"""Stops associated keyboard.listener thread"""
		self.isListening = False
		self.__listener.stop()
		
class noteBlock:
	"""This Handles Instances of the Note Widget"""
	def __init__(self, root):
		self.__root = root				##Allows the program to know what canvas item to place to
		self._activeNoteName = ""		##The name of the note that's in focus
		self._activeNoteMove = False	##True when a box is being moved
		self.dictOfNotes = {}			##Key == bbox of a text box

	def onClick(self, event):
		print(f"Active Note: {self._activeNoteName}")
		print(f"Active Move: {self._activeNoteMove}")
		if not self._activeNoteMove:
			for object in self.dictOfNotes.values():
				if object.withinTopOfBox(event):
					self.__root.bind("<Motion>", object.moveBox)
					self._activeNoteName = object.myID
					self._activeNoteMove = True
		
		if self._activeNoteName == "": ##Checks if a note is active
			if len(self.dictOfNotes) > 0:
				self.edit_note(event)
				if self._activeNoteName == "":
					self.create_note(event)
			else:
				self.create_note(event)
		else:
			##Clears the active note if outside of bounds
			if not self.dictOfNotes[self._activeNoteName].withinBounds(event):
				self.dictOfNotes[self._activeNoteName].stop_Listening()
				self.dictOfNotes[self._activeNoteName].active = False
				self._activeNoteName = ""
				##Checks to see if another note was clicked. Only after clicking off the previously active note
				self.edit_note(event) ##Tries to edit first
				if self._activeNoteName == "":
					self.create_note(event) ##If no edits, create a new note instead
	
	def create_note(self, event):
		print("Creating a new Note")
		##Fills in Default Data
		newKey = f"Note-#{len(self.dictOfNotes)}"
		self.dictOfNotes[newKey] = noteWidget(self.__root, newKey)
		self.dictOfNotes[newKey].newNote(event)
		self.dictOfNotes[newKey].active = True
		self._activeNoteName = newKey

	def edit_note(self, event):
		##Determins if a note is to become active
		for key in self.dictOfNotes.keys():
			if self.dictOfNotes[key].withinBounds(event):
				print(f"Edit this box: dictOfNotes[{key}] = {self.dictOfNotes[key]}")
				self.dictOfNotes[key].active = True
				self._activeNoteName = key
				break

		##Reactivate the keyboard listener.
		if self._activeNoteName != "":
			self.dictOfNotes[self._activeNoteName].start_Listening()
