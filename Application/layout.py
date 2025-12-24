##IMPOTS
import tkinter
from Workspace.textEditor import stringInfo

##EXPORTS
__all__ = [
	"DOC_NAVIGATION",
	"DIV_NAVIGATION"
]

class layoutInfo(stringInfo):
	def __init__(self, parent):
		stringInfo.__init__(self)
		self._parent = parent ##The container that a Layout item was placed to. 
		self._canvasObj = None

		self._activeItems = {} ##Key = Document title, Value = Document Object
		self._itemPosition = {} ##Key = Document Object, Value = Position of Document Reference
		self._itemCanvasID = {} ##Key = Document Title, Value = Canvas IDs of document text object

		self._xOffSet = 10
		self._yNextSpot = 5

	def get_canvasObj(self):
		return self._canvasObj

class DOC_NAVIGATION(layoutInfo):
	def __init__(self, parent, width):
		layoutInfo.__init__(self, parent)
		##Private Varibles
		self._width = (width * 0.15)
		self._canvasObj = tkinter.Canvas(parent, bg="dark grey", width=self._width)
		self.__activeDocument = ""

		##Public Variabels

		##Config
		self._canvasObj.grid(column=1, row=1, sticky="NSWE")
		self._parent.columnconfigure(1, weight=4)
	
	def newDocument(self, title:str, documentObject):
		##Creating navigation item
		if title == "":
			# print("title Was blank")
			title = "Blank Document"
			documentObject.lastTitle = title
			documentObject.set_title(title)
		self.__activeDocument = documentObject
		# print(f"Title: {title}\nObject: {documentObject}")

		self._activeItems[title] = documentObject
		self._itemPosition[documentObject] = (0, self._yNextSpot-5, self._width, self._yNextSpot+self.myFontHeight+5)
		self._canvasObj.create_rectangle(self._itemPosition[documentObject])

		##Displaying Item on Screen
		self._itemCanvasID[title] = self._canvasObj.create_text(self._xOffSet, self._yNextSpot, anchor="nw", font=(self.myFont, self.myFontSize))
		self._canvasObj.itemconfigure(self._itemCanvasID[title], text=title)

		##Final Events
		self._activeItems[title].lastTitle = title
		self._yNextSpot += (self.myFontHeight+10)

	def updateTitle(self, oldTitle:str, newTitle:str):
		# print(f"Title at call: {oldTitle} & {newTitle}")
		##Save to cache
		tempActiveDict = self._activeItems[oldTitle]
		tempItemID	= self._itemCanvasID[oldTitle]

		##Remove old items
		del self._activeItems[oldTitle]
		del self._itemCanvasID[oldTitle]

		##Saves object back to new title name
		self._activeItems[newTitle] = tempActiveDict
		self._itemCanvasID[newTitle] = tempItemID

		##Updates the Document Navigation string
		self._canvasObj.itemconfigure(self._itemCanvasID[newTitle], text=newTitle)
		self._activeItems[newTitle].lastTitle = newTitle
	
	def onClick(self, event):
		clickedDocument = self.selectDocument(event)
		if clickedDocument != self.__activeDocument and clickedDocument != None:
			# print("Different Document")
			##Hide and deactivate the last active document
			self.__activeDocument.get_canvasObj().grid_remove()
			self.__activeDocument.stop_Listening()
			self.__activeDocument.activeDoc = False

			##Show and activate the new current document
			clickedDocument.get_canvasObj().grid()
			clickedDocument.activeDoc = True

			##Save the new current document to .__activeDocument
			self.__activeDocument = clickedDocument
		# print(f"Clicked on {clickedDocument.get_title()}")

	def selectDocument(self, event):
		for key, bbox in self._itemPosition.items():
			if bbox[0] <= event.x and event.x <= bbox[2]:
				if bbox[1] <= event.y and event.y <= bbox[3]:
					return key
		return None


##FUTURE
class DIV_NAVIGATION(layoutInfo):
	def __init__(self, parent, height):
		layoutInfo.__init__(self, parent)
		##Private Varibles
		self._height = (height * 0.05)
		self._canvasObj = tkinter.Canvas(parent, bg="dark grey", height=self._height)

		##Public Variabels

		##Config
		self._canvasObj.grid(column=0, row=0, columnspan=2, sticky="WE")
		