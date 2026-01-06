##IMPORTS
from .textEditor import TEXT_EDITOR
from Data import LINKED_LIST

##EXPORTS
__all__ = [
	"STICKY_NOTE"
]

class STICKY_NOTE(TEXT_EDITOR):
	"""Handles the Contents of an individual note"""
	def __init__(self, root, ID):
		TEXT_EDITOR.__init__(self, root, ID)
		self.__root = root ##Canvas Object that notes will be written to
		self.myID = ID
		self.active = False ##The given note is active.
		self.toBeDeleted  = False
		self._activeError = False

		self.txtPad = 5

		##Text Box Widget Variables
		self.activeMove  = False
		self.lockBoxSize = False
		self.activeWidthChange = False
		self._moveAnchor = []
		self._textAnchor = []
		self.__moveContainerID = None
		self.__textContainerID = None
		self.myBbox = []		##(x1, y1, x2, y2)
		self.box_offset_x = 20	##The Box Pad in the x direction
		self.box_offset_y = 10	##The Box Pad in the y direction
		self.minBoxSize  = int(self._wrapLength/3)+self.box_offset_x

		##SAVE/LOAD from Files:
		self.stepCount = 0

	def deleteCanvasIDs(self):
		self.__root.delete(self.__textContainerID)
		self.__root.delete(self.__moveContainerID)
		self.__root.delete(self._textCanvasID)
		if self.isListening:
			self.stop_keyboard()
	
	def createNote(self, event):
		self.myBbox = [event.x, event.y-10, event.x+int(self._wrapLength/2)+self.box_offset_x, event.y+self.box_offset_y+self._myFontHeight]
		# self.coords = (event.x, event.y)
		
		##Creates Canvas Widgets 
		self.__moveContainerID = self.__root.create_rectangle(event.x, self.myBbox[1], self.myBbox[2], event.y)
		self.__textContainerID  = self.__root.create_rectangle(self.myBbox)
		self._textCanvasID = self.__root.create_text(event.x+self.txtPad, event.y+self.txtPad, anchor="nw", font=self.get_myFontPackage())
		self.initCursor((event.x+self.txtPad, event.y+self.txtPad))

		self.active = True
		self.start_keyboard()

	def autoChangeWidth(self):
		##If self.lockBoxSize is True. Then, Prevent any changes to box width
		if self.isListening and self.activeKeyPress and not self.lockBoxSize and self.minBoxSize < (self.myBbox[2]-self.myBbox[0]):
			##Remove old Canvas ID
			self.__root.delete(self.__textContainerID)
			self.__root.delete(self.__moveContainerID)

			##Adjust box Here
			defaultWidth = int(self._wrapLength/2)+self.box_offset_x

			# print("LongestLine", self.longestLine())
			if self._myFont.measure(self.longestLine()) >= int(0.75 * defaultWidth):
				self.changeBBox(2, self.myBbox[0]+self._myFont.measure(self.longestLine())+int(0.25 * defaultWidth))

			##Re-Create top box
			self.__moveContainerID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self.__textContainerID = self.__root.create_rectangle(self.myBbox)

	def autoChangeHeight(self):
		if (self.isListening and self.activeKeyPress) or self.activeWidthChange:
			##Remove old Canvas ID
			self.__root.delete(self.__textContainerID)
			self.__root.delete(self.__moveContainerID)

			##Adjust box Here
			if self._enterKeyActive:
				self.changeBBox(3, self.myBbox[1]+self.txtPad+((self.get_contentBreakdownLength()+2) * self._myFontHeight))
			elif len(self.get_contentBreakdown()) == 0:
				#Prevents the box from strinking when typing text into a blank sticky note
				pass
			else:
				self.changeBBox(3, self.myBbox[1]+self.txtPad+((self.get_contentBreakdownLength()+1) * self._myFontHeight))
			
			##Re-Create top box
			self.__moveContainerID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self.__textContainerID = self.__root.create_rectangle(self.myBbox)
	
	def wrapTextSmallerLive(self, contents:list, currLine:int):
		print(f"Contents: [", end="")
		for items in contents:
			try:
				print(f"{items.head.data}, ", end="")
			except AttributeError:
				print(f"NoneType, ", end="")
		print("]")
		try:
			##Removes any empty lines of text
			for index in range(len(contents)):
				if contents[index].isEmpty():
					contents.pop(index)
			textLength = self._myFont.measure(self.stringBuilder(contents[currLine]))
		except IndexError as E:
			if currLine == 0 and contents == []:
				return
			elif currLine > len(contents):
				print(f"IndexError @STICKY_NOTE.wrapTextSmallerLive() \n>> Index:{currLine} > {len(contents)}:Length of List <<\n")
			return			

		if textLength > self._wrapLength:
			##If currLine+1 doesn't exist, create it
			if len(contents) == currLine+1:
				self.add_contentToBreakdown() ##Creates new line
				contents = self.get_contentBreakdown() ##Updates current contents variable
			
			newLine = LINKED_LIST()
			curr = contents[currLine].findLastElement()
			if curr != None and self.wordBuilder(contents[currLine]).length > 1:
				##pops the last element if it's a white space
				##Until all tailing whitespaces are removed.
				while curr.data.isspace():
					print(f"Popping Whitespaces {curr.data}")
					contents[currLine].popElement() 
					curr = curr.prev
					if curr == None:
						return

				# print(f"Current: {lineContents.popElement()}")
				##Loops from end of list till whitespace
				while not curr.data.isspace():
					##sends end characters to start of next line
					newLine.add_head(contents[currLine].popElement().data)
					curr = curr.prev

			contents[currLine+1].add_head(" ")

			#If newLine != None: ##The loop should get skipped anyway if it's empty
			while not newLine.isEmpty():
				##pops the last element and adds it to the head of the next line.
				contents[currLine+1].add_head(newLine.popElement().data)

			##Updates text object
			self.set_contentBreakdown(contents)
			self.updateText()

		##Recursivley calls itself for the next line. 
		self.wrapTextSmallerLive(contents, currLine+1)
	
	def wrapTextLargerLive(self, contents:list, currLine:int):
		print(contents)
		try:
			##Removes any empty lines of text
			for index in range(len(contents)):
				if contents[index].isEmpty():
					contents.pop(index)

			if currLine >= len(contents):
				raise IndexError(f"Index:{currLine} >= {len(contents)}:Length of List")
			if currLine == 0:
				raise IndexError(f"Ingex:{currLine} - No Wrapping with line 0")
			textLength = self._myFont.measure(self.stringBuilder(contents[currLine-1])) #Length of previous line
		except IndexError as E:
			print(f"IndexError File @STICKY_NOTE.wrapTextLargerLive(index={currLine}) \n>> {E} <<\n")
			return

		# print(f"Wrap Length: {self._wrapLength} vs Text Line-{currLine}: {textLength}")
		if textLength < int(self._wrapLength*0.8):
			curr = contents[currLine].head
			if curr != None:
				print(f"Starting Char: {curr.data}")
				contents[currLine-1].add_tail(" ")
				if curr.data.isspace():
					contents[currLine].popElement(0)
					curr = curr.next
					if curr == None:
						return	

				while not curr.data.isspace():
					##Iterates through characters till it hits a white space
					# print(f"{curr.data}", end="")
					contents[currLine-1].add_tail(contents[currLine].popElement(0).data)
					
					##If this line becomes empty, remove it from list
					if contents[currLine].isEmpty():
						print("Popping an empty line.")
						contents.pop(currLine)

					##Steps to the next element
					curr = curr.next

					if curr == None:
						##Exits loop if True
						break
				# print(" :END of First Word")
				
				##Updates text object
				self.set_contentBreakdown(contents)
				self.updateText()
		
		self.wrapTextLargerLive(self.get_contentBreakdown(), currLine-1)
	
	def removeEmptyNote(self):
		# print(f"{self.myID} is active? {self.active}")
		if self.get_contents == "" and not self.active:
			self.toBeDeleted = True
			self.deleteCanvasIDs()

	def withinBounds(self, event):
		##Retruns True if mouse was clicked inside a text box, else returns false
		if self.myBbox[0] < event.x and event.x < self.myBbox[2]+5:
			#Mouse Possition on Click is between x1 and x2
			if self.myBbox[1] < event.y and event.y < self.myBbox[3]:
				#Mouse Possition on click is between y1 and y2
				return True
		return False
	
	def withinTopOfBox(self, pos):
		##Retruns True if mouse was clicked inside a text box, else returns false
		if self.myBbox[0] < pos[0] and pos[0] < self.myBbox[2]:
			#Mouse Possition on Click is between x1 and x2
			if self.myBbox[1] < pos[1] and pos[1] < (self.myBbox[1]+10):
				# print("Within top of Box")
				return True
		return False

	def withinSideOfBox(self, pos):
		##Retruns True if mouse was clicked inside a text box, else returns false
		if self.myBbox[2]-15 < pos[0] and pos[0] < self.myBbox[2]+10:
			#Mouse Possition on Click is between x1 and x2
			if self.myBbox[1] < pos[1] and pos[1] < (self.myBbox[3]):
				# print("Within right side of Box")
				return True
		return False

	def pressHoldWidthChange(self, mousePos):
		##Makes sure the box doesn't automatically change size if the user has specified a size
		self.lockBoxSize = True

		##Removes old Canvas Widgets
		self.__root.delete(self.__textContainerID)
		self.__root.delete(self.__moveContainerID)
		
		##Changes box size and wrap length
		growingBox = self.myBbox[2]<mousePos[0]
		# print("Grow" if growingBox else "Shrink") ##Debug.
		if self.minBoxSize < (mousePos[0]-self.myBbox[0]):
			self.myBbox = [self.myBbox[0], self.myBbox[1], mousePos[0], self.myBbox[3]]
			self._wrapLength = mousePos[0] - self.myBbox[0] - self.box_offset_x
			if not self.isEmpty_contentBreakdown(): #Start based on longest line or start from top to bottom
				if growingBox:
					##Growing box
					self.wrapTextLargerLive(self.get_contentBreakdown(), len(self.get_contentBreakdown())-1)
				else:
					##Shrinking box.
					self.wrapTextSmallerLive(self.get_contentBreakdown(), 0) #Start text wrapping with the first line of text.

		##Create New Canvas Widgets
		self.__textContainerID  = self.__root.create_rectangle(self.myBbox)
		self.__moveContainerID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
		
		if not self.activeWidthChange:
			self.activeWidthChange = True

	def pressHoldBoxMove(self, mousePos):
		##Remove previous Canvas Widgets
		if not self.activeMove:
			self._moveAnchor = [mousePos[0] - self.myBbox[0], mousePos[1] - self.myBbox[1], self.myBbox[2] - mousePos[0], self.myBbox[3] - mousePos[1]]
			self._textAnchor = [mousePos[0] - (self.myBbox[0]+self.txtPad), mousePos[1] - (self.myBbox[1]+10+self.txtPad)]
			self.activeMove = True
		else:
			self.__root.delete(self.__textContainerID)
			self.__root.delete(self.__moveContainerID)
			self.__root.delete(self._textCanvasID)

			if self._moveAnchor != []:
				self.myBbox = [mousePos[0]-self._moveAnchor[0], mousePos[1]-self._moveAnchor[1], mousePos[0]+self._moveAnchor[2], mousePos[1]+self._moveAnchor[3]]

			##Create New Canvas Widgets
			self.__textContainerID  = self.__root.create_rectangle(self.myBbox)
			self.__moveContainerID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self._textCanvasID = self.__root.create_text(mousePos[0]-self._textAnchor[0], mousePos[1]-self._textAnchor[1], text=self.get_contents(), anchor="nw", font=self.get_myFontPackage())

	def loadFromFile(self, currentItem):
		print("Re-impliment at a later date")
		pass
	
	def drawToScreen(self):
		if not self._activeError:
			self.__moveContainerID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self._textCanvasID	= self.__root.create_text(self.myBbox[0]+self.txtPad, self.myBbox[1]+self.txtPad+10, anchor="nw", font=self._myFont, text=self._contents)
			self.__textContainerID  = self.__root.create_rectangle(self.myBbox)
			self._currLine = len(self._contentLines) - 1
		else:
			print("Could not Draw sticky note to screen")

	def set_textID(self, ID):
		self._textCanvasID = ID

	def set_boxID(self, ID):
		self.__textContainerID = ID

	def get_myLinkedList(self):
		return self._linkedList

	def get_textID(self):
		return self._textCanvasID

	def get_boxID(self):
		return self.__textContainerID

	def changeBBox(self, index:int, newValue:int):
		"""
		| Changes specific elements of the bbox. Reduces the need to redeclare the bbox when only one or two elements change.
		"""
		self.myBbox[index] = newValue
		##Able to mainipulate the self.myBbox by changing one or all elements of the tuple
		##Dynamic in a way to know which elements to change
		##need to know if I'm increasing/decreasing, should this be in a list too?
		pass
		
