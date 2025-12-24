##IMPORTS
from .textEditor import TEXT_EDITOR

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
		self.activeMove = False
		self.manualWidthSet = False
		self.manualChangeWidth = False
		self._moveAnchor = []
		self._textAnchor = []
		self.__moveCanvasID = None
		self.__boxCanvasID = None
		# self.coords  = (0, 0)       ##(x, y)
		self.myBbox = [] ##(x1, y1, x2, y2)
		self.box_offset_x = 20          ##The offset from original Top-Left position
		self.box_offset_y = 10

		##SAVE/LOAD from Files:
		self.stepCount = 0

	def deleteCanvasIDs(self):
		self.__root.delete(self.__boxCanvasID)
		self.__root.delete(self.__moveCanvasID)
		self.__root.delete(self._textCanvasID)
		if self.isListening:
			self.stop_Listening()
	
	def createNote(self, event):
		self.myBbox = [event.x, event.y-10, event.x+int(self._wrap/2)+self.box_offset_x, event.y+self.box_offset_y+self.myFontHeight]
		# self.coords = (event.x, event.y)
		
		##Creates Canvas Widgets 
		self.__moveCanvasID = self.__root.create_rectangle(event.x, self.myBbox[1], self.myBbox[2], event.y)
		self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
		self._textCanvasID = self.__root.create_text(event.x+self.text_offset, event.y+self.text_offset, anchor="nw", font=(self.myFont, self.myFontSize))#, width=100)
		
		self.active = True
		self.start_Listening()

	def changeWidth(self):
		##If self.manualWidthSet is True. Then, Prevent any changes to box width
		if self.isListening and self._activeKeyPress and not self.manualWidthSet:
			##Remove old Canvas ID
			self.__root.delete(self.__boxCanvasID)
			self.__root.delete(self.__moveCanvasID)

			##Adjust box Here
			defaultWidth = int(self._wrap/2)+self.box_offset_x

			if self.myFont.measure(self.longestLine()) >= int(0.75 * defaultWidth):
				self.changeBBox(2, self.myBbox[0]+self.myFont.measure(self.longestLine())+int(0.25 * defaultWidth))

			##Re-Create top box
			self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self.__boxCanvasID = self.__root.create_rectangle(self.myBbox)

	def changeHeight(self):
		if self.isListening and self._activeKeyPress:
			##Remove old Canvas ID
			self.__root.delete(self.__boxCanvasID)
			self.__root.delete(self.__moveCanvasID)

			##Adjust box Here
			self.changeBBox(3, self.myBbox[1]+self.text_offset+((len(self._contentLines)+1) * self.myFontHeight))
			
			##Re-Create top box
			self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self.__boxCanvasID = self.__root.create_rectangle(self.myBbox)
	
	def changeWrap(self):
		pass
	
	def removeEmptyNote(self):
		# print(f"{self.myID} is active? {self.active}")
		if self._contents == "" and not self.active:
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
				print("Within right side of Box")
				return True
		return False
		

	def pressHoldWidthChange(self, mousePos):
		self.__root.delete(self.__boxCanvasID)
		self.__root.delete(self.__moveCanvasID)
		
		self.myBbox = [self.myBbox[0], self.myBbox[1], mousePos[0], self.myBbox[3]]
		self._wrap = mousePos[0] - self.myBbox[0] - self.box_offset_x

		##Create New Canvas Widgets
		self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
		self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
		
		if not self.manualChangeWidth:
			self.manualChangeWidth = True
		self.manualWidthSet = True

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
			self._textCanvasID = self.__root.create_text(mousePos[0]-self._textAnchor[0], mousePos[1]-self._textAnchor[1], text=self._contents, anchor="nw", font=(self.myFont, self.myFontSize))

	def loadFromFile(self, currentItem):
		try:
			if currentItem.data == ":END":
				self.stepCount += 1
				currentItem = currentItem.next
				raise Exception("IGNORE")
				
			if self.stepCount == 0:
				# self._contents += currentItem.data
				if currentItem.next.data != ":END": ##Going to brick when currentItem.next == None
					self._contents += f"{currentItem.data}\n"
					self._contentLines.append(f"{currentItem.data}\n")
					self._contentLengthAtLine[len(self._contentLengthAtLine)] = len(self._contents)
				else:
					##When it's the last element before next data set
					self._contents += currentItem.data			
				# print(f"TEXT: {self._contents} | AT STEP: {stepCount}")
				# print(f"TEXT LIST: {self._contentLines}")
				# print(f"TEXT LENGTH: {self._contentLengthAtLine}")
			
			if self.stepCount == 1:
				self.myBbox.append(int(currentItem.data))
				# print(f"BBOX: {self.myBbox}")

		except AttributeError as E:
			print(f"Caught Error: {E}\n @noteWidget.loadFromFile()")
			self._activeError = True
		except Exception:
			pass
	
	def drawToScreen(self):
		if not self._activeError:
			self.__moveCanvasID = self.__root.create_rectangle(self.myBbox[0], self.myBbox[1], self.myBbox[2], self.myBbox[1]+10)
			self._textCanvasID	= self.__root.create_text(self.myBbox[0]+self.text_offset, self.myBbox[1]+self.text_offset+10, anchor="nw", font=self.myFont, text=self._contents)
			self.__boxCanvasID  = self.__root.create_rectangle(self.myBbox)
			self._currLine = len(self._contentLines)
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
	
	def get_contents(self):
		return self._contents

	def changeBBox(self, index:int, newValue:int):
		"""
		| Changes specific elements of the bbox. Reduces the need to redeclare the bbox when only one or two elements change.
		"""
		self.myBbox[index] = newValue
		##Able to mainipulate the self.myBbox by changing one or all elements of the tuple
		##Dynamic in a way to know which elements to change
		##need to know if I'm increasing/decreasing, should this be in a list too?
		pass
		
