##IMPORTS
import tkinter
from .menu import MENU
from .files import FILES
from Workspace import DOCUMENT


##Running the base application
class APP(MENU, FILES):
	"""Creates the Base window for this Project"""
	def __init__(self, width, height, titleString="Notes App [v0.0.67]"):
		MENU.__init__(self)
		FILES.__init__(self)
		##Private Variables
		self.__refreshRate = int(1000/60) ##In milliseconds (ms)

		##Setting up the Tkinter Window
		self._mainApp = tkinter.Tk()
		self._mainApp.title(titleString)
		self._mainApp.geometry(f"{width}x{height}")

		##Declaring Bindings
		self._mainApp.bind_all("<Escape>", self.kill)

		##Workspace Declarations
		self.__workspace = {}

	def createWorkspace(self, key):
		self.__workspace[key] = DOCUMENT(self._mainApp, key)
		self._mainApp.bind_all("<Button-1>", self.__workspace[key].onClick)
		pass
	
	def loadWorkspace(self, key):
		##Will be used to load in a workspace from files
		pass

	def startApp(self):
		self.createWorkspace("Canvas-#0")
		
		##Setting up the Tkinter Menus
		self.menuSetUp()
		# self.createChildMenu("File", "Save", self.save)
		# self.createChildMenu("File", "Open", self.open)
		self.createChildMenu("Edit", "Clear Screen", self.__workspace["Canvas-#0"].clearWorkspace)
		self.childMenuPush()

		##Loads Last Save at launch
		try:
			self.open()
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