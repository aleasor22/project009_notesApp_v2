##Relavant Imports
import tkinter.font as tkFont
from pynput import keyboard
from .Linked_List import LINKED_LIST

__all__ = [
	"TEXT_EDITOR",
]

class TEXT_EDITOR:
	"""Used to edit/change text in any object that needs text."""
	def __init__(self, childsRoot):
		self.__root = childsRoot ##This is the root canvas of the object that needs the Text Editor
		self.__listener = None
		self.isListening = False

		self._linkedList = LINKED_LIST()
		
		self.myFont = tkFont.nametofont("TkDefaultFont")
		self.myFontHeight = self.myFont.metrics('linespace')
		self.myFontLength = self.myFont.measure("")
		
		##Text Widget Variables
		self._textCanvasID = None
		self._wrap = 200
		self._backSpaceActive = False  ##Tracks if the backspace  has been hit while editing text
		
		##String Manipulations
		self._contents = ""
		self._currLine = 0
		self._contentLines = []
		self._longestLine  = 0
		self._contentLengthAtLine = {0:0}
	
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
			self.__root.itemconfigure(self._textCanvasID, text=self._contents)
			# print(f"Add new Key to screen: {key}")
			
			self.adjustBox(expand="x-dir")

			##Resize box on wrap
			toWrap = self.myFont.measure(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
			if toWrap > self._wrap and not self._backSpaceActive:
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

	def start_Listening(self):
		"""Starts associated keyboard.listener thread"""
		self.__listener = keyboard.Listener(on_press=self.pressed, on_release=self.released)
		self.isListening = True
		self.__listener.start() ##Starts a tread to track for keyboards press/release actions

	def stop_Listening(self):
		"""Stops associated keyboard.listener thread"""
		self.isListening = False
		self.__listener.stop()