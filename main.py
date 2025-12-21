##Imports
import tkinter
from pynput import keyboard
from Note_Object.noteObject import *
from Document_Object import *
from Data import *

class Events:
	"""Handles Most Events within the project"""
	def __init__(self):
		self._mainApp = None
		self._activeCanvas = None
		self.__noteBlock = None

		self._fileManager = FILE_MANAGER()
		self._fileManager.set_fileLocation("testing.csv")

	def kill(self, event):
		self._mainApp.destroy()

	##---Basic Methods & Getters/Setters---##
	def test(self): 
		##used to test events - Often a placeholder
		print("Event Tested")

	def get_activeCanvas(self):
		return self._activeCanvas
	
	def get_mainApp(self):
		return self._mainApp
	
	def get_fileManager(self):
		return self._fileManager

class Menu(Events):
	def __init__(self):
		Events.__init__(self)
		self.__mainMenu = None

		##Parent Menu Dropdowns
		self._parentMenus = {
			"File":		None, 
			"Edit":		None, 
			"View":		None, 
			"Setting":	None, 
			"Help":		None, 
		}
		self._childMenus = {
			"File":	[], 
			"Edit":	[], 
			"View":	[],			
		}
		# self._defaultCommand = {
		# 	"Settings": self.default,
		# 	"Help":		self.default,
		# }
	
	def menuSetUp(self):
		self.__mainMenu = tkinter.Menu(self._mainApp)

		for key in self._parentMenus.keys():
			self._parentMenus[key] = tkinter.Menu(self.__mainMenu, tearoff=False)
			self.__mainMenu.add_cascade(label=key, menu=self._parentMenus[key])
		
		self._mainApp.config(menu=self.__mainMenu)

	def createChildMenu(self, root:str, childLabel:str, function):
		self._childMenus[root].append((childLabel, function))
	
	def childMenuPush(self):
		for key, value in self._childMenus.items():
			if len(value) > 0:
				##tuple = ("Menu Label", function)
				for tuple in value:
					self._parentMenus[key].add_cascade(label=tuple[0], command=tuple[1])

##Running the base application
class App(Menu):
	"""Creates the Base window for this Project"""
	def __init__(self, width, height, titleString="Notes App [v0.0.63]"):
		Menu.__init__(self)
		##Private Variables
		self.__refreshRate = int(1000/60) ##In milliseconds (ms)

		##Setting up the Tkinter Window
		self._mainApp = tkinter.Tk()
		self._mainApp.title(titleString)
		self._mainApp.geometry(f"{width}x{height}")

		##Setting up the Tkinter Menus
		self.menuSetUp()
		self.createChildMenu("File", "Save", self._fileManager.save)
		self.createChildMenu("File", "Open", self._fileManager.open)
		# self.createChildMenu("Edit", "Clear Screen", self.clearScreen)
		self.childMenuPush()		

		##Declaring Bindings
		self._mainApp.bind_all("<Escape>", self.kill)

	def startApp(self):
		##Loads Last Save at launch
		try:
			self._fileManager.open()
		except FileNotFoundError:
			with open(self._fileLocation, "w") as f:
				f.write("")

		##Renders Window to Screen
		self._mainApp.mainloop()
	
	def get_refreshRate(self):
		return self.__refreshRate
	
	def set_refreshRate(self, fps):
		self.__refreshRate = int(fps)
	
	def set_activeCanvas(self, canvasObj):
		self._activeCanvas = canvasObj


##Running the Program
Window = App(width=500, height=500)
Document = Document_Object(parent=Window.get_mainApp())
Notes = noteBlock(Document)

Window.set_activeCanvas(Document.get_canvasObj())
Window.get_fileManager().set_noteBlock(Notes)

##Event Handling
Document.get_canvasObj().bind("<Button-1>", Document.onClick)
Document.get_canvasObj().bind("<Button-1>", Notes.onClick, add="+")

def refresh():
	##Controls What to do each time the Window Refreshes
	#
	##End of refresh
	Window.get_mainApp().after(Window.get_refreshRate(), refresh)

refresh()
Window.startApp()


