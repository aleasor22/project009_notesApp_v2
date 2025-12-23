##IMPORTS
import tkinter
from .menu import MENU
from Workspace import DOCUMENT


##Running the base application
class APP(MENU):
	"""Creates the Base window for this Project"""
	def __init__(self, width, height, titleString="Notes App [v0.0.68]"):
		MENU.__init__(self)
		##Private Variables
		self.__refreshRate = int(1000/60) ##In milliseconds (ms)

		##Setting up the Tkinter Window
		self._mainApp = tkinter.Tk()
		self._mainApp.title(titleString)
		self._mainApp.geometry(f"{width}x{height}")

		##Declaring Bindings
		self.createEvent("<Escape>", self.kill)

		##Workspace Declarations
		self.__workspace = {}

	def createWorkspace(self, key):
		self.__workspace[key] = DOCUMENT(self._mainApp, key)
		self.createEvent("<Button-1>", self.__workspace[key].onClick)

	def loadWorkspace(self, key):
		##Will be used to load in a workspace from files
		pass

	def startApp(self):
		self.createWorkspace("Canvas-#0")
		
		##Setting up the Tkinter Menus
		self.menuSetUp()
		self.createChildMenu("File", "Save", self.__workspace["Canvas-#0"].saveDocument)
		self.createChildMenu("File", "Open", self.__workspace["Canvas-#0"].openDocument)
		self.createChildMenu("Edit", "Clear Screen", self.__workspace["Canvas-#0"].clearWorkspace)
		self.childMenuPush()

		##Loads Last Save at launch
		try:
			self.__workspace["Canvas-#0"].openDocument()
		except FileNotFoundError:
			with open(self._fileLocation, "w") as f:
				f.write("")
		except:
			pass
		##Renders Window to Screen
		self._mainApp.mainloop()
	
	def get_refreshRate(self):
		return self.__refreshRate
	
	def set_refreshRate(self, fps):
		self.__refreshRate = int(fps)
	
	def set_activeCanvas(self, canvasObj):
		self._activeCanvas = canvasObj