##IMPORTS
import tkinter
import tkinter.font as tkFont

__all__ = [
	"Document_Object",
]

class Document_Object:
	def __init__(self, parent):
		##Private Variables
		self.__parent = parent
		self.__canvasObject = tkinter.Canvas(parent, bg="gray")
		self.__titleBlockZone = [0, 0, 400, 80]

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
		self.__canvasObject.create_rectangle(self.__titleBlockZone) ##Rough outline of where the title block goes. 
		self.__canvasObject.create_line(20, 70, 380, 70)


		pass

	def onClick(self, event):
		if self.__titleBlockZone[0] <= event.x and event.x <= self.__titleBlockZone[2]:
			if self.__titleBlockZone[1] <= event.y and event.y <= self.__titleBlockZone[3]:
				print("INSIDE TITLE BLOCK")
				self.titleActive = True
			