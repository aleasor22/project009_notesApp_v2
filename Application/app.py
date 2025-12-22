##IMPORTS
import tkinter
from .menu import MENU


##Running the base application
class APP(MENU):
	"""Creates the Base window for this Project"""
	def __init__(self, width, height, titleString="Notes App [v0.0.65]"):
		MENU.__init__(self)
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
		# self.createChildMenu("Edit", "Clear Screen", self.clearScreen)
		self.childMenuPush()		

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
	
	def set_activeCanvas(self, canvasObj):
		self._activeCanvas = canvasObj