##Relavant Imports
import tkinter.font as tkFont
from pynput import keyboard
from Data import LINKED_LIST

##EXPORTS
__all__ = [
	"TEXT_EDITOR",
	"stringInfo"
]

class stringInfo:
	def __init__(self, fontSize:int=11):
		##Holds the Contents of the text for on screen
		self._contents = "" ## Houses the entire string. From start to finish of text
		self._currLine = 0	## The current total line number. NOTE: May get phased out.
		self._contentLines = []	## The ._contents string is split by line.
		self._longestLine  = 0	## Temporary variable that houses the current longest line. NOTE: May get Phased out.
		self._contentLengthAtLine = {0:0} ## Stores how long the line is (character count). NOTE: Item 0:0 should never get removed
		
		##Font Data
		self.myFontSize = fontSize
		self.myFont = tkFont.nametofont("TkDefaultFont")
		self.myFontHeight = self.myFont.metrics('linespace')
		self.myFontLength = self.myFont.measure("")

class TEXT_EDITOR(stringInfo):
	"""Used to edit/change text in any object that needs text."""
	def __init__(self, childsRoot, childID, fontSize:int=9):
		stringInfo.__init__(self, fontSize)
		##Related Data
		self.__root = childsRoot ##This is the root canvas of the object that needs the Text Editor
		self._childID = childID ## This represents the type of text box that I'm writing to. 
		self._linkedList = LINKED_LIST()

		##Input Keyboard Listener
		self.__listener = None
		self.isListening = False
		
		##Text Widget Data
		self._textCanvasID = None
		self._wrap = 200
		self._backSpaceActive = False  ##Tracks if the backspace  has been hit while editing text
		self._isHotKeyPressed = False
		self._hotKeyList = [
			keyboard.Key.alt_gr,
			keyboard.Key.alt_l,
			keyboard.Key.ctrl_l,
			keyboard.Key.ctrl_r,
			keyboard.Key.esc
		]
	
	def pressed(self, key):
		try:
			# print(f"Key Pressed: {key.char}") ##Used for Debug
			if not self._isHotKeyPressed:
				self._contents += key.char
		except AttributeError:
			# print(f"Key Pressed: {key}") ##Used for Debug
			if key in self._hotKeyList:
				# print(f"Ignore this: {key}")
				self._isHotKeyPressed = True
			if key == key.enter:
				self.onEnterPress()
			if key == key.space:
				self._contents += " "
			if key == key.tab:
				self.onTabPress()
			if key == key.backspace:
				self._backSpaceActive = True
				self.onBackSpace()
		finally:
			##This logic happens no mater the above results
			self.myFontLength = self.myFont.measure(self._contents) ##Updates Total length of String, NOTE: DOESN'T KNOW ABOUT WRAPING OR NEWLINE CHARACTER
			self.__root.itemconfigure(self._textCanvasID, text=self._contents)
			# print(f"Add new Key to screen: {key}")
			
			##Resize box on wrap
			toWrap = self.myFont.measure(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
			if toWrap > self._wrap and not self._backSpaceActive:
				self._contents += "\n"
				self._contentLengthAtLine[len(self._contentLengthAtLine)] = len(self._contents)
				self._contentLines.append(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
				self._currLine += 1
				print(self._contentLines, "append")
			else:
				##Only happens when my text width is under the wrap length
				self._backSpaceActive = False

	def released(self, key):
		try:
			temp = key.char
		except AttributeError:
			if key in self._hotKeyList:
				# print(f"Ignore this: {key}")
				self._isHotKeyPressed = False
		finally:
			##This logic happens no mater the above results
			pass

	def onEnterPress(self, ):
		print(self._childID, " = Child ID")
		if "Canvas" in self._childID:
			print("Nothing Happens")
			self.stop_Listening()
		else:
			self._contents += "\n"
			self._contentLengthAtLine[len(self._contentLengthAtLine)] = len(self._contents)
			self._contentLines.append(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
			self._currLine += 1
			print(self._contentLines, "append")

	def onTabPress(self):
		self._contents += "\t"

	def onBackSpace(self, ):
		temp = self._contents
		if len(temp) > 0:
			self._contents = temp.rstrip(temp[len(self._contents)-1])
			
			if temp[len(self._contents)-1] == "\n":# and len(self._contents) > 0:
				if len(self._contentLines) >= 0:
					self._contentLengthAtLine.popitem()
					self._contentLines.pop()
					self._currLine -= 1
					print(self._contentLengthAtLine, "pop")
			
			##Reset variables if self._contents string is empty
			if len(self._contents) == 0:
				self._contentLengthAtLine = {0:0}
				self._contentLines = []
				self._currLine = 0
				print(self._contentLengthAtLine, "pop")

	def longestLine(self):
		##Compare current line with other lines. Determine if the current is the longest
		maxLength = self.myFont.measure(self.stringWithinRange(self._contentLengthAtLine[self._currLine], len(self._contents)))
		for line in self._contentLines:
			if maxLength < self.myFont.measure(line):
				maxLength = self.myFont.measure(line)
		return maxLength
	
	def stringWithinRange(self, lowerBound, upperBound):
		newString = ""
		for index in range(len(self._contents)):
			if lowerBound <= index and index <= upperBound:
				newString += self._contents[index]
			
			if index > upperBound:
				break
		
		return newString

	def start_Listening(self):
		"""Starts associated keyboard.listener thread"""
		self.__listener = keyboard.Listener(on_press=self.pressed, on_release=self.released)
		self.isListening = True
		self.__listener.start() ##Starts a tread to track for keyboards press/release actions

	def stop_Listening(self):
		"""Stops associated keyboard.listener thread"""
		if self.__listener != None:
			self.isListening = False
			self.__listener.stop()
		else:
			print("No listener to stop.")
		
	def addToContents(self, line:str):
		self._contents += f"{line} "
		print(self._contents, "TESTING CONTENTS")
		