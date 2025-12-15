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
		self.__maxLength = 0
		##Start the Listenser
		self.__listener = keyboard.Listener(on_press=self.pressed, on_release=self.released)
		self.isListening = False
		self.myID = ID

		##Text Widget Variables
		self.__textCanvasID = None
		self.__wrap = 100
		self._backSpaceActive = False  ##Tracks if the backspace  has been hit while editing text
		self._lineCount = 1
		self.myFont = tkFont.nametofont("TkDefaultFont")
		self.myFontHeight = self.myFont.metrics('linespace')
		self.myFontLength = self.myFont.measure("")
		self.text_offset = 5
		self.contents = ""
		

		##Text Box Widget Variables
		self.__boxCanvasID = None
		self.coords	 = (0, 0)		##(x, y)
		self.my_bbox = (0, 0, 0, 0)	##(x1, y1, x2, y2)
		self.box_offset_x = 20			##The offset from original Top-Left position
		self.box_offset_y = 10

	def pressed(self, key):
		try:
			# print(f"Key Pressed: {key.char}") ##Used for Debug
			self.contents += key.char
		except AttributeError:
			# print(f"Key Pressed: {key}") ##Uded for Debug
			if key == key.enter:
				self.contents += "\n"
				self.adjustBox()
				
			if key == key.space:
				self.contents += " "
			if key == key.tab:
				self.contents += "\t"
			if key == key.backspace:
				# print(self.contents[self.__maxLength-1])
				self._backSpaceActive = True
				temp = self.contents
				if len(temp) > 0:
					self.contents = temp.rstrip(temp[self.__maxLength-1])

					if temp[self.__maxLength-1] == "\n":# and self._wrapedAtLine[self._lineCount]:
						self.adjustBox(-1)
						self._lineCount -= 1
					
		finally:
			##This logic happens no mater the above results
			self.myFontLength = self.myFont.measure(self.contents) ##Updates Total length of String, NOTE: DOESN'T KNOW ABOUT WRAPING OR NEWLINE CHARACTER
			# print(f"Add new Key to screen: {key}")
			print(self.myFontLength)

			self.__maxLength = len(self.contents)
			self.__root.itemconfigure(self.__textCanvasID, text=self.contents)

			##Resize box on wrap
			wrapText = (self.__wrap * self._lineCount)
			# print(self._wrapedAtLine)
			if self.myFontLength > wrapText and not self._backSpaceActive:
				self.contents += "\n"
				self._lineCount += 1
				self.adjustBox()
			else:
				self._backSpaceActive = False ##Only happens once my text width is under the wrap length
				

	def released(self, key):
		try:
			temp = key.char
		except AttributeError:
			if key == key.f1:
				print(self.contents)
		finally:
			##This logic happens no mater the above results
			pass
	
	def newNote(self, event):
		self.my_bbox = (event.x, event.y, event.x+self.__wrap+self.box_offset_x, event.y+self.box_offset_y+self.myFontHeight)
		self.coords = (event.x, event.y)
		
		##Creates Canvas Widgets 
		self.__boxCanvasID =  self.__root.create_rectangle(self.my_bbox)
		self.__textCanvasID = self.__root.create_text(event.x+self.text_offset, event.y+self.text_offset, anchor="nw", font=self.myFont)#, width=100)
		self.start_Listening()

	def adjustBox(self, addOrRemove=1):
		##Remove old Canvas ID
		self.__root.delete(self.__boxCanvasID)

		##Create New Box
		self.my_bbox = (self.my_bbox[0], self.my_bbox[1], self.my_bbox[2], self.my_bbox[3]+(addOrRemove * self.myFontHeight))
		self.__boxCanvasID = self.__root.create_rectangle(self.my_bbox)
		# self._lineCount += addOrRemove

	def set_textID(self, ID):
		self.__textCanvasID = ID

	def set_boxID(self, ID):
		self.__boxCanvasID = ID

	def get_textID(self):
		return self.__textCanvasID

	def get_boxID(self):
		return self.__boxCanvasID

	def delete(self, root):
		root.delete(self.__boxCanvasID)
		root.delete(self.__textCanvasID)

	def start_Listening(self):
		"""Starts associated keyboard.listener thread"""
		self.isListening = True
		self.__listener.start() ##Starts a tread to track for keyboards press/release actions

	def stop_Listening(self):
		"""Stops associated keyboard.listener thread"""
		self.isListening = False
		self.__listener.stop()
			

class noteBlock:
	"""This Handles Instances of the Note Widget"""
	def __init__(self, root):
		self.__root		= root  ##Allows the program to know what canvas item to place to
		self._newNote 	= False ##True when creating a new note
		self._activeNote = False ##True when any indidvidual note is in focus
		self.dictOfNotes = {} ##Key == bbox of a text box

	def create_note(self, event):
		if not self._newNote:
			##Fills in Default Data
			newKey = f"Note-#{len(self.dictOfNotes)}"
			self.dictOfNotes[newKey] = noteWidget(self.__root, newKey)
			self.dictOfNotes[newKey].newNote(event)

			self._activeNote = True
			self._newNote = True
		else:
			for key in self.dictOfNotes.keys():
				if self.dictOfNotes[key].isListening:
					self.dictOfNotes[key].stop_Listening()

	def edit_note(self):
		if self._activeNote:
			for key in self.dictOfNotes.keys():
				if self.dictOfNotes[key].isListening:
					# print(f"Start Listening @{self.dictOfNotes[key].myID}")
					break
			pass
		pass