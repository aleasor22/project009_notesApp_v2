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
		self.active = False
		self.toBeDeleted  = False
		self._activeError = False

		self.text_offset = 5

		##Text Box Widget Variables
		self.activeMove  = False
		self.lockBoxSize = False
		self.activeWidthChange = False
		self._moveAnchor = []
		self._textAnchor = []
		self.__moveCanvasID = None
		self.__boxCanvasID = None
		self.myBbox = []		##(x1, y1, x2, y2)
		self.box_offset_x = 20	##The Box Pad in the x direction
		self.box_offset_y = 10	##The Box Pad in the y direction
		self.minBoxSize  = int(self._wrapLength/3)+self.box_offset_x

		##SAVE/LOAD from Files:
		self.stepCount = 0

	def deleteCanvasIDs(self):
		self.__root.delete(self.__boxCanvasID)
		self.__root.delete(self.__moveCanvasID)
		self.__root.delete(self._textCanvasID)
		if self.isListening:
			self.stop_keyboard()
	
	def createNote(self, event):
		self.myBbox = [event.x, event.y-10, event.x+int(self._wrapLength/2)+self.box_offset_x, event.y+self.box_offset_y+self._myFontHeight]
		# self.coords = (event.x, event.y)
		
		##Creates Canvas Widgets 
		self.__moveCanvasID = self.__root.create_rectangle(event.x, self.myBbox[1], self.myBbox[2], event.y)
		self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
		self._textCanvasID = self.__root.create_text(event.x+self.text_offset, event.y+self.text_offset, anchor="nw", font=self.get_myFontPackage())
		
		self.active = True
		self.start_keyboard()

	def autoChangeWidth(self):
		##If self.lockBoxSize is True. Then, Prevent any changes to box width
		if self.isListening and self._activeKeyPress and not self.lockBoxSize and self.minBoxSize < (self.myBbox[2]-self.myBbox[0]):
			##Remove old Canvas ID
			self.__root.delete(self.__boxCanvasID)
			self.__root.delete(self.__moveCanvasID)

			##Adjust box Here
			defaultWidth = int(self._wrapLength/2)+self.box_offset_x

			# print("LongestLine", self.longestLine())
			if self._myFont.measure(self.longestLine()) >= int(0.75 * defaultWidth):
				self.changeBBox(2, self.myBbox[0]+self._myFont.measure(self.longestLine())+int(0.25 * defaultWidth))

			##Re-Create top box
			self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self.__boxCanvasID = self.__root.create_rectangle(self.myBbox)

	def autoChangeHeight(self):
		if (self.isListening and self._activeKeyPress) or self.activeWidthChange:
			##Remove old Canvas ID
			self.__root.delete(self.__boxCanvasID)
			self.__root.delete(self.__moveCanvasID)

			##Adjust box Here
			if self._enterKeyActive:
				self.changeBBox(3, self.myBbox[1]+self.text_offset+((self.get_contentBreakdownLength()+2) * self._myFontHeight))
			elif len(self.get_contentBreakdown()) == 0:
				#Prevents the box from strinking when typing text into a blank sticky note
				pass
			else:
				self.changeBBox(3, self.myBbox[1]+self.text_offset+((self.get_contentBreakdownLength()+1) * self._myFontHeight))
			
			##Re-Create top box
			self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self.__boxCanvasID = self.__root.create_rectangle(self.myBbox)
	
	def findLastWord(self, lineContents:LINKED_LIST):
		words = self.wordBuilder(lineContents)
		word = words.findLastElement().data
		sendNext = LINKED_LIST()
		if words.length > 1 and word != None:
			print(f"Last Word: {word}")
			print(f"Last Word length: {len(word)}")
			
			curr = lineContents.findLastElement()
			if curr.data == "\n": ##if last element is "\n" ignore it and remove it from list
				lineContents.popElement()
				curr = curr.prev
				
			stopElement = lineContents.findElementAtIndex(lineContents.length-len(word))
			if stopElement != None:
				print("Popped Elements: ", end="")
				while curr != stopElement.prev:
					sendNext.add_head(lineContents.popElement().data)
					curr = curr.prev
				sendNext.printList()
				# print(" :END")
		
		if sendNext.isEmpty():
			return None
		return sendNext
	
	def wrapTextLive(self, contents:list, currLine:int):
		try:
			textLength = self._myFont.measure(self.stringBuilder(contents[currLine]))
		except IndexError as E:
			# print(f"Error @STICKY_NOTE.wrapTextLive() \n>> {E} <<\n")
			return

		if  textLength > self._wrapLength:
			##If currLine+1 doesn't exist, create it
			if len(contents) == currLine+1:
				self.add_contentToBreakdown() ##Creates new line
				contents = self.get_contentBreakdown() ##Updates current contents variable

			lastWordList = self.findLastWord(contents[currLine]) ##Returns Linked List 
			if lastWordList != None:
				contents[currLine+1].add_head(" ") ##adds an ending whitespace to next line, for each word to be appended
				contents[currLine].popElement() ##Removes tailing whitespaceof current line before wrapping.
				
				##Adds wrapped word to the start of the next word, loops through each character.
				while not lastWordList.isEmpty():
					contents[currLine+1].add_head(lastWordList.popElement().data)

				contents[currLine].add_tail("\n")
				if contents[currLine+1].findLastElement().data.isspace():
					contents[currLine+1].popElement() ##Removes tailing whitespace of next line

				# print(f"is lastWrodList empty? {"yes" if lastWordList.isEmpty() else "No"}")
				contents[currLine].printList()	##DEBUGGING
				contents[currLine+1].printList()##DEBUGGING
				
				##Updates text object
				self.set_contentBreakdown(contents)
				# self.autoChangeHeight()
				self.updateText()

		self.wrapTextLive(contents, currLine+1)

	
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
		if self.myBbox[2]-15 < pos[0] and pos[0] < self.myBbox[2]+5:
			#Mouse Possition on Click is between x1 and x2
			if self.myBbox[1] < pos[1] and pos[1] < (self.myBbox[3]):
				# print("Within right side of Box")
				return True
		return False

	def pressHoldWidthChange(self, mousePos):
		##Makes sure the box doesn't automatically change size if the user has specified a size
		self.lockBoxSize = True

		##Removes old Canvas Widgets
		self.__root.delete(self.__boxCanvasID)
		self.__root.delete(self.__moveCanvasID)
		
		##Changes box size and wrap length
		if self.minBoxSize < (mousePos[0]-self.myBbox[0]):
			self.myBbox = [self.myBbox[0], self.myBbox[1], mousePos[0], self.myBbox[3]]
			self._wrapLength = mousePos[0] - self.myBbox[0] - self.box_offset_x
			if not self.isEmpty_contentBreakdown(): #Start based on longest line or start from top to bottom
				self.wrapTextLive(self.get_contentBreakdown(), 0) #Start text wrapping with the first line of text.

		##Create New Canvas Widgets
		self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
		self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
		
		if not self.activeWidthChange:
			self.activeWidthChange = True

	def pressHoldBoxMove(self, mousePos):
		##Remove previous Canvas Widgets
		if not self.activeMove:
			self._moveAnchor = [mousePos[0] - self.myBbox[0], mousePos[1] - self.myBbox[1], self.myBbox[2] - mousePos[0], self.myBbox[3] - mousePos[1]]
			self._textAnchor = [mousePos[0] - (self.myBbox[0]+self.text_offset), mousePos[1] - (self.myBbox[1]+10+self.text_offset)]
			self.activeMove = True
		else:
			self.__root.delete(self.__boxCanvasID)
			self.__root.delete(self.__moveCanvasID)
			self.__root.delete(self._textCanvasID)

			if self._moveAnchor != []:
				self.myBbox = [mousePos[0]-self._moveAnchor[0], mousePos[1]-self._moveAnchor[1], mousePos[0]+self._moveAnchor[2], mousePos[1]+self._moveAnchor[3]]

			##Create New Canvas Widgets
			self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
			self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self._textCanvasID = self.__root.create_text(mousePos[0]-self._textAnchor[0], mousePos[1]-self._textAnchor[1], text=self._contents, anchor="nw", font=self.get_myFontPackage())

	def loadFromFile(self, currentItem):
		print("Re-impliment at a later date")
		pass
	
	def drawToScreen(self):
		if not self._activeError:
			self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self._textCanvasID	= self.__root.create_text(self.myBbox[0]+self.text_offset, self.myBbox[1]+self.text_offset+10, anchor="nw", font=self._myFont, text=self._contents)
			self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
			self._currLine = len(self._contentLines) - 1
		else:
			print("Could not Draw sticky note to screen")

	def set_textID(self, ID):
		self._textCanvasID = ID

	def set_boxID(self, ID):
		self.__boxCanvasID = ID

	def get_myLinkedList(self):
		return self._linkedList

	def get_textID(self):
		return self._textCanvasID

	def get_boxID(self):
		return self.__boxCanvasID

	def changeBBox(self, index:int, newValue:int):
		"""
		| Changes specific elements of the bbox. Reduces the need to redeclare the bbox when only one or two elements change.
		"""
		self.myBbox[index] = newValue
		##Able to mainipulate the self.myBbox by changing one or all elements of the tuple
		##Dynamic in a way to know which elements to change
		##need to know if I'm increasing/decreasing, should this be in a list too?
		pass
		
