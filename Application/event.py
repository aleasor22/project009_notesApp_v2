##IMPORTS
import tkinter
import tkinter.font as tkFont
from .hotkeys import HOTKEYS

class EVENTS(HOTKEYS):
	"""Handles Most Events within the project"""
	def __init__(self):
		HOTKEYS.__init__(self)
		self._mainApp = None
		self._settingsPopup = None

		self._mousePosition = (0, 0)

	def kill(self):
		if self._settingsPopup != None:
			self._settingsPopup.destroy()
		self._mainApp.destroy()

	def currMousePosition(self, event):
		self._mousePosition = (event.x, event.y)

	def createEvent(self, binding, function, root=None):
		if root == None:
			root = self._mainApp
		root.bind(binding, function)

	def addEvent(self, binding, function):
		self._mainApp.bind_all(binding, function, add="+")

	##---Basic Methods & Getters/Setters---##
	def test(self): 
		##used to test events - Often a placeholder
		print("Event Tested")
	
	def get_mousePos(self):
		return self._mousePosition
	
	def get_mainApp(self):
		return self._mainApp