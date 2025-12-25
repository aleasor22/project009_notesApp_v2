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
		##String Information:
		self.__contents = ""
		self._contentBreakdown = [] ##Houses linked lists of each line.
		self._currentLine = 0		##Holds the currently active line.

		##Font Information:
		self._myFont		= tkFont.nametofont("TkDefaultFont")
		self._myFontSize	= fontSize
		self._myFontHeight	= self._myFont.metrics('linespace')

	def writeToContents(self):
		"""This will handle reading self._contentBreakdown into self.__contents. This needs to be done before writing to screen"""
		self.__contents = ""
		for line in self._contentBreakdown:
			self.__contents += self.stringBuilder(line)
			# print("Contents:", self.__contents)
		
		return self.__contents

	def appendContentBreakdown(self, char:str):
		if self._contentBreakdown == [] or char == "\n":
			##Create new linked list, if ._contentBreakdown is empty or a newline is created.
			self._contentBreakdown.append(LINKED_LIST())
			self._contentBreakdown[self._currentLine].add_tail(char)
			self._currentLine = len(self._contentBreakdown)-1
			# print(f"char passed: >> {char} <<")
		else:
			self._contentBreakdown[self._currentLine].add_tail(char)

	def popContentBreakdown(self, index:int=-1):
		if self._contentBreakdown[self._currentLine].head == None and self._currentLine > 0:
			print("head empty")
			self._contentBreakdown.pop()
			self._currentLine = len(self._contentBreakdown)-1
		self._contentBreakdown[len(self._contentBreakdown)-1].popElement()

	def longestLine(self):
		try:
			LONGEST_LINE = self.stringBuilder(self._contentBreakdown[0])
			CURRENT_LINE = ""

			for line in self._contentBreakdown:
				CURRENT_LINE = self.stringBuilder(line)
				if self._myFont.measure(LONGEST_LINE) < self._myFont.measure(CURRENT_LINE):
					# print(f"stringA({CURRENT_LINE}) is larger than stringB({LONGEST_LINE})")
					LONGEST_LINE = CURRENT_LINE
			# print(f"Longest Line: {LONGEST_LINE}")
			return LONGEST_LINE
		except IndexError as E:
			print(f"Error @stringInfo.longetsLine()\n>> {E} <<\n")
			return ""

	def stringBuilder(self, string:LINKED_LIST):
		curr = string.head
		line = ""
		while curr != None:
			line += curr.data
			curr = curr.next
		return line

	##Setters/Getters
	def set_contents(self, content):
		self.__contents = content

	def get_contents(self):
		return self.__contents

	def get_myFontPackage(self):
		return (self._myFont, self._myFontSize)

	def get_myFontHeight(self):
		return self._myFontHeight


class TEXT_BITMAPS:
	"""Hosts the buttons that manipulate Specific text features. EX: BOLD, Italics, Underline, etc."""
	def __init__(self):

		pass


class TEXT_EDITOR(stringInfo):
	"""Used to edit/change text in any object that needs text."""
	def __init__(self, childsRoot, childID, fontSize:int=9):
		stringInfo.__init__(self, fontSize)
		##Text Editing
		self.__root = childsRoot
		self.__childID = childID
		self._textCanvasID  = None
		self._wrapLength	= 200
		
		##Keyboard Listener Information
		self.__listener	 = None
		self.isListening = False
		self._hotKeyList = [
			keyboard.Key.alt_gr,
			keyboard.Key.alt_l,
			keyboard.Key.ctrl_l,
			keyboard.Key.ctrl_r,
			keyboard.Key.esc
		]
		self._isHotKeyPressed = False
		self._backSpaceActive = False
		self._enterKeyActive  = False
		self._activeKeyPress  = False

	##Actions when listening to the Keyboard.
	def pressed(self, key):
		try:
			# print(f"Key Pressed: {key.char}") ##Used for Debug
			if not self._isHotKeyPressed:
				self._activeKeyPress = True
				self.appendContentBreakdown(key.char)
		except AttributeError:
			# print(f"Key Pressed: {key}") ##Used for Debug
			self._activeKeyPress = True
			if key in self._hotKeyList:
				# print(f"Ignore this: {key}")
				self._isHotKeyPressed = True
			if key == key.enter:
				##When "Enter" is pressed
				self._enterKeyActive = True
				self.appendContentBreakdown("\n")
				pass
			if key == key.space:
				##When "Space" is pressed
				self.appendContentBreakdown(" ")
				pass
			if key == key.tab:
				##When "Tab" is pressed
				self.appendContentBreakdown("\t")
				pass
			if key == key.backspace:
				##When "Backspace" is pressed
				self._backSpaceActive = True
				self.popContentBreakdown()
		except IndexError as E:
			print(f"Caught Error in TEXT_EDITOR.pressed:\n>>{E}\n")
		finally:
			## The last thing I want to do whenever a key is pressed.
			# print(f"Key Pressed: {key}") ##Used for  Debug
			if self._textCanvasID != None:
				self.__root.itemconfigure(self._textCanvasID, text=self.writeToContents())
			pass

	def released(self, key):
		try:
			self._activeKeyPress = False
			temp = key.char
		except AttributeError:
			if key in self._hotKeyList:
				self._isHotKeyPressed = False
			if key == key.backspace:
				self._backSpaceActive = False
			if key == key.enter:
				self._enterKeyActive = False
		finally:
			##This logic happens no mater the above results
			pass
	
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