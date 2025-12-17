##Imports
import tkinter
from pynput import keyboard
from noteObject import *

class Events:
	"""Handles Most Events within the project"""
	def __init__(self):
		self._mainApp = None
		self._mainCanvas = None

		self.__mouseX = 0
		self.__mouseY = 0
		self.clickCounter = 0

	def kill(self, event):
		self._mainApp.destroy()

	def onClick(self, event):
		self.clickCounter += 1

	def updateMousePosition(self, event):
		self.__mouseX = event.x
		self.__mouseY = event.y
		# print(self.__mouseX, self.__mouseY)
	
	def get_mousePosition(self):
		return (self.__mouseX, self.__mouseY)
	
	def get_mainCanvas(self):
		return self._mainCanvas
	
	def get_mainApp(self):
		return self._mainApp

##Running the base application
class App(Events):
	"""Creates the Base window for this Project"""
	def __init__(self, width, height, titleString="Notes App [v0.0.31]"):
		Events.__init__(self)
		##Private Variables
		self.__refreshRate = int(1000/60) ##In milliseconds (ms)

		##Setting up the Tkinter Window
		self._mainApp = tkinter.Tk()
		self._mainApp.title(titleString)
		self._mainApp.geometry(f"{width}x{height}")

		##Setting up the Main Canvas
		self._mainCanvas = tkinter.Canvas(self._mainApp, bg="gray")#,cursor="xterm")
		self._mainCanvas.grid(column=0, row=0, sticky="NSWE")
		self._mainApp.columnconfigure(0, weight=10)
		self._mainApp.rowconfigure(0, weight=10)


		##Declaring Bindings
		self._mainApp.bind_all("<Escape>", self.kill)
		self._mainApp.bind_all("<Motion>", self.updateMousePosition)

	def startApp(self):
		##Renders Window to Screen
		self._mainApp.mainloop()
	
	def get_refreshRate(self):
		return self.__refreshRate
	
	def set_refreshRate(self, fps):
		self.__refreshRate = int(fps)


##Running the Program
Window = App(width=500, height=500)
Notes = noteBlock(Window.get_mainCanvas())

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


