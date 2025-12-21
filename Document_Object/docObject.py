##IMPORTS
import tkinter
import tkinter.font as tkFont
from Data.Text_Editor import TEXT_EDITOR

__all__ = [
	"Document_Object",
]

class Document_Object(TEXT_EDITOR):
	def __init__(self, parent):
		##Private Variables
		self.__parent = parent
		self.__canvasObject = tkinter.Canvas(parent, bg="gray")
		self.__titleExists = False
		TEXT_EDITOR.__init__(self, self.__canvasObject, "Canvas-#0", 16)

		##Canvas IDs
		self.__titleBlockZone	 = [0, 0, 250, 80]
		self.__titleZoneCanvasID = self.__canvasObject.create_rectangle(self.__titleBlockZone) ##Rough outline of where the title block goes. 
		self.__titleLinePosition = [20, 70, 230, 70]
		self.__titleLineCanvasID = self.__canvasObject.create_line(self.__titleLinePosition)
	
		##Public Variables
		self.title = None
		self.date = None
		self.time = None
		self.titleActive = False

		##Setting up Canvas Object
		self.__canvasObject.grid(column=0, row=0, sticky="NSWE")
		self.__parent.columnconfigure(0, weight=10)
		self.__parent.rowconfigure(0, weight=10)
		
		#CUSTOM SETUPS
		self.createTitleBlock()
	
	def get_canvasObj(self):
		return self.__canvasObject
	
	def createTitleBlock(self, ):
		if not self.isListening and not self.__titleExists:
			self._textCanvasID = self.__canvasObject.create_text(self.__titleLinePosition[0], self.__titleLinePosition[1]-self.myFontHeight-10, anchor="nw", font=(self.myFont, self.myFontSize))
			self.__titleExists = True

	def onClick(self, event):
		if self.__titleBlockZone[0] <= event.x and event.x <= self.__titleBlockZone[2]:
			if self.__titleBlockZone[1] <= event.y and event.y <= self.__titleBlockZone[3]:
				# print("INSIDE TITLE BLOCK")
				self.createTitleBlock() ##Creates title block text, otherwise
				self.start_Listening()
				self.titleActive = True
			else:
				self.stop_Listening()
				self.titleActive = False
		else:
			self.stop_Listening()
			self.titleActive = False