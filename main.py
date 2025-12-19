##Imports
import tkinter
from pynput import keyboard
from noteObject import *

class Events:
	"""Handles Most Events within the project"""
	def __init__(self):
		self._mainApp = None
		self._mainCanvas = None
		self.__noteBlock = None

		self._fileLocation = "history/test.csv"

	def kill(self, event):
		self._mainApp.destroy()

	def clearScreen(self):
		self.__noteBlock.clearScreen()
		with open(self._fileLocation, "w") as file:
			file.write("")
	
	def save(self): ##Using the CSV format (Comma Separated Values)
		dictOfNotes = self.__noteBlock.dictOfNotes
		with open(self._fileLocation, "w") as file:
			for noteObj in dictOfNotes.values():
				if len(noteObj.get_contents()) == 0:
					##Ignores Empty Notes When Saving
					continue
				noteObj.saveToFile(file)

	def open(self):
		self.__noteBlock.clearScreen()
		dictOfNotes = self.__noteBlock.dictOfNotes
		stepCount = 0
		with open(self._fileLocation) as file:
			currWord = ""
			for line in file:
				if (line[0]+line[1] != "//"):
					newKey = f"Note-#{len(dictOfNotes)}"
					dictOfNotes[newKey] = noteWidget(self._mainCanvas, newKey)
					for char in line:
						if char == "," or char == "\n":
							stepCount = dictOfNotes[newKey].loadFromFile(stepCount, currWord)
							currWord = ""
							continue
						currWord += char

	##---Basic Methods & Getters/Setters---##
	def test(self): 
		##used to test events - Often a placeholder
		print("Event Tested")

	def get_mainCanvas(self):
		return self._mainCanvas
	
	def get_mainApp(self):
		return self._mainApp
	
	def set_noteData(self, data):
		self.__noteBlock = data

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
	def __init__(self, width, height, titleString="Notes App [v0.0.43]"):
		Menu.__init__(self)
		##Private Variables
		self.__refreshRate = int(1000/60) ##In milliseconds (ms)

		##Setting up the Tkinter Window
		self._mainApp = tkinter.Tk()
		self._mainApp.title(titleString)
		self._mainApp.geometry(f"{width}x{height}")

		##Setting up the Tkinter Menus
		self.menuSetUp()
		self.createChildMenu("File", "Save", self.save)
		self.createChildMenu("File", "Open", self.open)
		self.createChildMenu("Edit", "Clear Screen", self.clearScreen)
		self.childMenuPush()		

		##Setting up the Main Canvas
		self._mainCanvas = tkinter.Canvas(self._mainApp, bg="gray")#,cursor="xterm")
		self._mainCanvas.grid(column=0, row=0, sticky="NSWE")
		self._mainApp.columnconfigure(0, weight=10)
		self._mainApp.rowconfigure(0, weight=10)


		##Declaring Bindings
		self._mainApp.bind_all("<Escape>", self.kill)

	def startApp(self):
		##Loads Last Save at launch
		try:
			self.open()
		except FileNotFoundError:
			with open(self._fileLocation, "w") as f:
				f.write("")

		##Renders Window to Screen
		self._mainApp.mainloop()
	
	def get_refreshRate(self):
		return self.__refreshRate
	
	def set_refreshRate(self, fps):
		self.__refreshRate = int(fps)


##Running the Program
Window = App(width=500, height=500)
Notes = noteBlock(Window.get_mainCanvas())
Window.set_noteData(Notes)

Window.get_mainCanvas().bind("<Button-1>", Notes.onClick)

def refresh():
	##Controls What to do each time the Window Refreshes
	#
	#
	#
	##End of refresh
	Window.get_mainApp().after(Window.get_refreshRate(), refresh)

refresh()
Window.startApp()


