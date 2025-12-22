##IMPORTS
import tkinter
import tkinter.font as tkFont

class EVENTS:
	"""Handles Most Events within the project"""
	def __init__(self):
		self._mainApp = None

		# self._fileManager = FILE_MANAGER()
		# self._fileManager.set_fileLocation("testing.csv")
		# self._fileLocation = self._fileManager.get_fileLocation()

	def kill(self, event):
		self._mainApp.destroy()


	##---Basic Methods & Getters/Setters---##
	def test(self): 
		##used to test events - Often a placeholder
		print("Event Tested")
	
	def get_mainApp(self):
		return self._mainApp