##IMPORTS
import tkinter.font as tkFont
from pynput import keyboard
from Data import LINKED_LIST

##EXPORTS
__all__ = [
	"TEXT_EDITOR",
	"STRING_EDITOR"
]

class STRING_EDITOR:
	def __init__(self, fontSize:int=11):
		##String Information:
		self.__contents 	= ""
		self.__contentBreakdown = [] ##Houses linked lists of each line.
		self._currentLine 	= 0		 ##Holds the currently active line.
		self._textCanvasID  = None
		self._wrapLength	= 200
		self.toWrap		= False
		self.finishedWord = False

		##Font Information:
		self._myFont		= tkFont.nametofont("TkDefaultFont")
		self._myFontSize	= fontSize
		self._myFontHeight	= self._myFont.metrics('linespace')

	def writeToContents(self):
		"""This will handle reading self.__contentBreakdown into self.__contents. This needs to be done before writing to screen"""
		self.__contents = ""
		for line in self.__contentBreakdown:
			self.__contents += self.stringBuilder(line)
			self.__contents += "\n"
			# print("Contents:", self.__contents)
		
		return self.__contents

	def appendContentBreakdown(self, char:str):
		if self.__contentBreakdown == [] or char == "\n":
			##Create new linked list, if ._contentBreakdown is empty or a newline is created.
			self.__contentBreakdown.append(LINKED_LIST())
			if char != "\n":
				self.__contentBreakdown[self._currentLine].add_tail(char)
			self._currentLine = len(self.__contentBreakdown)-1
			# print(f"char passed: >> {char} <<")
		else:
			self.__contentBreakdown[self._currentLine].add_tail(char)

	def popContentBreakdown(self, index:int=-1):
		if self.__contentBreakdown[self._currentLine].head == None and self._currentLine > 0:
			print("head empty")
			self.__contentBreakdown.pop()
			self._currentLine = len(self.__contentBreakdown)-1
		self.__contentBreakdown[len(self.__contentBreakdown)-1].popElement()
	
	def wrapWord(self, ):
		if len(self.__contentBreakdown) > 0:
			currentLength = self._myFont.measure(self.stringBuilder(self.__contentBreakdown[self._currentLine]))
			if not self._backSpaceActive:
				if self._wrapLength < currentLength:
					self.toWrap = True
					print("Wrap possible")
			# else:
			# 	self.toWrap = False

	def longestLine(self):
		try:
			LONGEST_LINE = self.stringBuilder(self.__contentBreakdown[0])
			CURRENT_LINE = ""

			for line in self.__contentBreakdown:
				CURRENT_LINE = self.stringBuilder(line)
				if self._myFont.measure(LONGEST_LINE) < self._myFont.measure(CURRENT_LINE):
					# print(f"stringA({CURRENT_LINE}) is larger than stringB({LONGEST_LINE})")
					LONGEST_LINE = CURRENT_LINE
			# print(f"Longest Line: {LONGEST_LINE}")
			return LONGEST_LINE
		except IndexError as E:
			print(f"Error @STRING_EDITOR.longetsLine()\n>> {E} <<\n")
			return ""
	
	def wordBuilder(self, string:LINKED_LIST):
		curr = string.head
		# print(curr.data)
		wordList = LINKED_LIST()
		currWord = ""
		while curr != None:
			if curr.data.isspace():
				if currWord != "":
					wordList.add_tail(currWord)
					currWord = ""
				else: ##skips white space.
					currWord = ""
				curr = curr.next
				continue
			if curr.next == None:
				currWord += curr.data
				wordList.add_tail(currWord)
				curr = curr.next
				continue

			currWord += curr.data
			curr = curr.next
		wordList.printList()
		return wordList

	def stringBuilder(self, list:LINKED_LIST):
		try:
			curr = list.head
			line = ""
			while curr != None:
				# print("Data:", curr.data) ##For Debugging
				line += curr.data
				curr = curr.next
			return line
		except TypeError as E:
			print(f"TypeError File @STRING_EDITOR.stringBuilder()\n>> {E} <<\n>> curr.data == NODE obj. <<")
			print(f">> Returns '{line}' <<")
			return line
		except AttributeError as E:
			print(f"AttributeError File @STRING_EDITOR.stringBuilder()\n >> {E} <<")
			print(f">> Returns '{line}' <<")
			return line
	
	##Setters/Getters
	def set_contents(self, content:str):
		self.__contents = content
	
	def set_contentBreakdown(self, breakdown:LINKED_LIST):
		self.__contentBreakdown = breakdown
		self._currentLine = len(breakdown)-1

	def add_contentToBreakdown(self, data=None):
		self.__contentBreakdown.append(LINKED_LIST())

		if data != None: ##Adds data if something was passed through
			self.__contentBreakdown[-1].add_head(data)
		
		self._currentLine = len(self.__contentBreakdown)-1

	def get_contents(self):
		return self.__contents
	
	def isEmpty_contentBreakdown(self):
		if self.__contentBreakdown == []:
			return True
		return False
	
	def get_contentBreakdown(self, index:int=-1):
		try:
			if index == -1:
				raise IndexError
			return self.__contentBreakdown[index]
		except IndexError as E:
			return self.__contentBreakdown
	
	def get_contentBreakdownLength(self):
		return len(self.__contentBreakdown)

	def get_myFontPackage(self):
		return (self._myFont, self._myFontSize)

	def get_myFontHeight(self):
		return self._myFontHeight


class TEXT_BITMAPS:
	"""Hosts the buttons that manipulate Specific text features. EX: BOLD, Italics, Underline, etc."""
	def __init__(self):

		pass


class TEXT_EDITOR(STRING_EDITOR):
	"""Used to edit/change text in any object that needs text."""
	def __init__(self, childsRoot, childID, fontSize:int=9):
		STRING_EDITOR.__init__(self, fontSize)
		##Text Editing
		self.__root = childsRoot
		self.__childID = childID
		
		##Keyboard Listener Information
		self.__listener	 = None
		self.isListening = False
		self._hotKeyList = [
			keyboard.Key.alt_gr,
			keyboard.Key.alt_l,
			keyboard.Key.ctrl_l,
			keyboard.Key.ctrl_r,
			# keyboard.Key.shift,
			keyboard.Key.esc
		]
		self._isHotKeyPressed = False
		self._backSpaceActive = False
		self._enterKeyActive  = False
		self.activeKeyPress	  = False
		self.spaceActive	  = False
		self._isCapsLocked	  = False

	##Actions when listening to the Keyboard.
	def pressed(self, key):
		try:
			# print(f"Key Pressed: {key.char}") ##Used for Debug
			if not self._isHotKeyPressed:
				self.activeKeyPress = True
				self.finishedWord = False
				if self._isCapsLocked:
					self.appendContentBreakdown(key.char.upper())
				else:
					self.appendContentBreakdown(key.char)
		except AttributeError:
			# print(f"Key Pressed: {key}") ##Used for Debug
			self.activeKeyPress = True
			if key in self._hotKeyList:
				# print(f"Ignore this: {key}")
				self._isHotKeyPressed = True
			if key == key.enter:
				##When "Enter" is pressed
				self._enterKeyActive = True
				self.appendContentBreakdown("\n")
				pass
			if key == key.space:
				self.spaceActive = True
				self.finishedWord = True
				if not self.toWrap:
					self.appendContentBreakdown(" ")
			if key == key.tab:
				##When "Tab" is pressed
				self.appendContentBreakdown("\t")
				pass
			if key == key.backspace:
				##When "Backspace" is pressed
				self._backSpaceActive = True
				self.popContentBreakdown()
			if key == key.caps_lock:
				if not self._isCapsLocked:
					self._isCapsLocked = True
				elif self._isCapsLocked:
					self._isCapsLocked = False
		except IndexError as E:
			print(f"Caught Error in TEXT_EDITOR.pressed:\n>> {E} <<\n")
		finally:
			## The last thing I want to do whenever a key is pressed.
			# print(f"Key Pressed: {key}") ##Used for  Debug
			self.updateText()
			self.wrapWord()

	def released(self, key):
		try:
			self.activeKeyPress = False
			temp = key.char
		except AttributeError:
			if key in self._hotKeyList:
				self._isHotKeyPressed = False
			if key == key.space:
				self.spaceActive = False
			if key == key.backspace:
				self._backSpaceActive = False
			if key == key.enter:
				self._enterKeyActive = False
		finally:
			##This logic happens no mater the above results
			pass

	def updateText(self):
		if self._textCanvasID != None:
			self.__root.itemconfigure(self._textCanvasID, text=self.writeToContents())
		else:
			print("Do I want to create text here?")

	##Start/Stop Keyboard Listener
	def start_keyboard(self):
		"""Starts associated keyboard.listener thread"""
		if not self.isListening: ##Makes sure a listener hasn't already started.
			self.__listener = keyboard.Listener(on_press=self.pressed, on_release=self.released)
			self.isListening = True
			self.__listener.start() ##Starts a tread to track the keyboard inputs

	def stop_keyboard(self):
		"""Stops associated keyboard.listener thread"""
		if self.__listener != None: ## Only Stops a listener if one exists
			self.isListening = False
			self.__listener.stop() ##Stops the thread that tracked the keyboard inputs