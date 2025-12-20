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

		##Public Variables
		self.title = None
		self.date = None
		self.time = None

		##Setting up Canvas Object
		self.__canvasObject.grid(column=0, row=0, sticky="NSWE")
		self.__parent.columnconfigure(0, weight=10)
		self.__parent.rowconfigure(0, weight=10)
	
	def get_canvasObj(self):
		return self.__canvasObject
