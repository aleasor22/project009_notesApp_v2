##IMPORTS
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
		self._contentLines = [""]	## The ._contents string is split by line.
		self._longestLine  = 0	## Temporary variable that houses the current longest line. NOTE: May get Phased out.
		
		##Font Data
		self.myFontSize = fontSize
		self.myFont = tkFont.nametofont("TkDefaultFont")
		self.myFontHeight = self.myFont.metrics('linespace')
		self.myFontLength = self.myFont.measure("")

	def get_fontInfo(self):
		return (self.myFont, self.myFontSize)
		
	
class TEXT_BITMAPS:
	"""Hosts the buttons that manipulate Specific text features. EX: BOLD, Italics, Underline, etc."""
	def __init__(self):

		pass


class TEXT_EDITOR(stringInfo):
	"""Used to edit/change text in any object that needs text."""
	def __init__(self, childsRoot, childID, fontSize:int=9):
		stringInfo.__init__(self, fontSize)
		##Related Data
		self.__root = childsRoot ##This is the root canvas of the object that needs the Text Editor
		self._childID = childID ## This represents the type of text box that I'm writing to.

		##Input Keyboard Listener
		self.__listener = None
		self.isListening = False
		
		##Text Widget Data
		self._textCanvasID = None
		self._wrap = 200
		self._backSpaceActive = False  ##Tracks if the backspace  has been hit while editing text
		self._isHotKeyPressed = False
		self._activeKeyPress  = False
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
			self._activeKeyPress = True
			if not self._isHotKeyPressed:
				activeKey = key.char
				self.appendCurrentLine(activeKey)
				self._contents += activeKey
		except AttributeError:
			# print(f"Key Pressed: {key}") ##Used for Debug
			if key in self._hotKeyList:
				# print(f"Ignore this: {key}")
				self._isHotKeyPressed = True
			if key == key.enter:
				self.onEnterPress()
			if key == key.space:
				self.appendCurrentLine(" ")
				self._contents += " "
			if key == key.tab:
				self.onTabPress()
			if key == key.backspace:
				self._backSpaceActive = True
				self.onBackSpace()
		except IndexError as E:
			print(f"Caught Error in TEXT_EDITOR.pressed:\n>>{E}\n")
		finally:
			##This logic happens no mater the above results
			self.myFontLength = self.myFont.measure(self._contents) ##Updates Total length of String, NOTE: DOESN'T KNOW ABOUT WRAPING OR NEWLINE CHARACTER
			self.__root.itemconfigure(self._textCanvasID, text=self._contents)
			# print(f"Add new Key to screen: {key}")
			
			##Resize box on wrap
			# print(f"self._contents = {self._contents} <<\n")
			toWrap = self.myFont.measure(self._contentLines[self._currLine])
			# print(toWrap > self._wrap, ":toWrap bool")
			if toWrap > self._wrap and not self._backSpaceActive:
				self.onEnterPress()
				print(f"Wrap happened w/ keypress: {key}")
			print(self._contentLines, "append")

	def released(self, key):
		try:
			self._activeKeyPress = False
			temp = key.char
		except AttributeError:
			if key in self._hotKeyList:
				# print(f"Ignore this: {key}")
				self._isHotKeyPressed = False
			if key == key.backspace:
				self._backSpaceActive = False
		finally:
			##This logic happens no mater the above results
			pass

	def onEnterPress(self, ):
		# print(self._childID, " = Child ID")
		if "Canvas" in self._childID:
			# print("Nothing Happens")
			self.stop_Listening()
		else:
			self.appendCurrentLine("\n")
			self._contents += "\n"
			self._currLine += 1
			# print(self._contentLines, "append")

	def onTabPress(self):
		self._contents += "\t"

	def onBackSpace(self, ):
		temp = self._contents
		if len(self._contentLines) > 0:
			tempLine = self._contentLines[self._currLine]
		if len(temp) > 0 and tempLine != None:
			self._contents = temp.rstrip(self.get_lastChar_inString(temp))
			print(f"Length of line: {len(self._contentLines[self._currLine])}")
			if len(self._contentLines[self._currLine]) > 0:
				self._contentLines[self._currLine] = tempLine.rstrip(self.get_lastChar_inCurrentLine())
			
			if self.get_lastChar_inString(temp) == "\n" or len(self._contentLines[self._currLine]) == 0:
				if len(self._contentLines) >= 0:
					test = self._contentLines.pop()
					self._currLine -= 1
					print(f"This was popped: {test}")
			
			##Reset variables if self._contents string is empty
			if len(self._contents) == 0:
				self._contentLines = [""]
				self._currLine = 0

		# self._backSpaceActive = False

	def longestLine(self):
		##Compare current line with other lines. Determine if the current is the longest
		longestLine = len(self._contentLines[0])
		longestLineIndex = 0
		for index in range(len(self._contentLines)):
			if longestLine < len(self._contentLines[index]):
				longestLine = len(self._contentLines[index])
				longestLineIndex = index
		return self._contentLines[longestLineIndex]
	
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
		if not self.isListening: ##Makes sure a listener hasn't already started.
			self.__listener = keyboard.Listener(on_press=self.pressed, on_release=self.released)
			self.isListening = True
			self.__listener.start() ##Starts a tread to track for keyboards press/release actions

	def stop_Listening(self):
		"""Stops associated keyboard.listener thread"""
		if self.__listener != None:
			self.isListening = False
			self.__listener.stop()
		# else:
		# 	print("No listener to stop.")
		
	def addToContents(self, line:str):
		self._contents += f"{line} "
		# print(self._contents, "TESTING CONTENTS")
	
	def appendCurrentLine(self, key:str):
		self._contentLines[self._currLine] += key
		if key == "\n":
			self._contentLines.append("") ##starts the line element
	
	def get_lastChar_inCurrentLine(self):
		try:
			return self._contentLines[self._currLine][len(self._contentLines[self._currLine])-1]
		except IndexError as E:
			print(f"String Index: {len(self._contentLines[self._currLine])-1}")
			print(f"Index Error @lastChar_inCurrentLine\n\t>> {E} <<\n")

	def get_lastChar_inString(self, string:str=""):
		try:
			if string == "":
				string = self._contents
			return string[len(string)-1]
		except IndexError as E:
			print(f"\nIndex Error @lastChar_inString\n>> {string} <<\n")