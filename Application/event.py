##IMPORTS
import tkinter
import tkinter.font as tkFont

class EVENTS:
	"""Handles Most Events within the project"""
	def __init__(self):
		self._mainApp = None

		self._activeEvents = {}


	def kill(self, event):
		self._mainApp.destroy()

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
	
	def get_mainApp(self):
		return self._mainApp