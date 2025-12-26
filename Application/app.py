##IMPORTS
import tkinter
from .menu import MENU
from .layout import *
from Workspace import DOCUMENT


##Running the base application
class APP(MENU):
	"""Creates the Base window for this Project"""
	def __init__(self, width, height, titleString="Notes App [v0.0.73-3]"):
		MENU.__init__(self)
		##Private Variables
		self.__refreshRate = int(1000/60) ##In milliseconds (ms)
		self.__screenWidth = width
		self.__screenHeight = height

		##Setting up the Tkinter Window
		self._mainApp = tkinter.Tk()
		self._mainApp.title(titleString)
		self._mainApp.geometry(f"{width}x{height}")

		##Public Variables
		self.shutdown = False

		##Workspace Declarations
		self.__docLayout = DOC_NAVIGATION(self._mainApp, width)
		self.__divLayout = DIV_NAVIGATION(self._mainApp, height)
		self.__workspace = {}
		self.createEvent("<Motion>", self.currMousePosition)
		self.createEvent("<Button-1>", self.__docLayout.onClick, root=self.__docLayout.get_canvasObj())

	def createWorkspace(self, key):
		##Sets all existing canvas items as inactive
		for value in self.__workspace.values():
			value.get_canvasObj().grid_remove()
			value.stop_Listening()
			value.activeDoc = False
		
		self.__workspace[key] = DOCUMENT(self._mainApp, key, self.__screenWidth)
		fontInfo = self.__workspace[key].get_myFontPackage()
		self.__docLayout.set_fontInfo(fontInfo[0], fontInfo[1])
		self.__workspace[key].activeDoc = True
		self.__docLayout.newDocument(self.__workspace[key].get_title(), self.__workspace[key])
		self.createEvent("<Button-1>", self.__workspace[key].onClick, root=self.__workspace[key].get_canvasObj())

	def startApp(self):
		self.createWorkspace("Canvas-#0")

		##Setting Up Global Hotkeys
		self.addHotkeyCommand("Exit", self.kill, "<esc>")
		# self.addHotkeyCommand("Save", self.__workspace["Canvas-#0"].saveDocument)
		# self.addHotkeyCommand("Open", self.__workspace["Canvas-#0"].openDocument)
		self.start_hotKeyListener()
		self.start_mouseListener()

		##Setting up the Tkinter Menus
		self.menuSetUp()
		self.createChildMenu("File", "Save", self.__workspace["Canvas-#0"].saveDocument)
		self.createChildMenu("File", "Open", self.__workspace["Canvas-#0"].openDocument)
		self.createChildMenu("File", "New",  lambda:self.createWorkspace(key=f"Canvas-#{len(self.__workspace)}"))
		self.createChildMenu("Edit", "Clear Screen", self.__workspace["Canvas-#0"].clearWorkspace)
		self.childMenuPush()

		##Loads Last Save at launch
		try:
			# self.__workspace["Canvas-#0"].openDocument()
			pass
		except FileNotFoundError:
			with open(self._fileLocation, "w") as f:
				f.write("")
		except:
			pass
		
		##Filling out Layouts post file read.
		self.__docLayout.updateTitle(self.__workspace["Canvas-#0"].lastTitle, self.__workspace["Canvas-#0"].get_title())

		##Renders Window to Screen
		self._mainApp.bind("<Destroy>", self.onClose)
		self._mainApp.mainloop()
	
	def onClose(self, event):
		self.shutdown = True
		# if event.widget == self._mainApp:
		# 	for value in self.__workspace.values():
		# 		value.saveDocument()
	
	def navigationUpdates(self, ):
		for value in self.__workspace.values():
			# print(value.activeDoc, ":", value.myID)
			if value.activeDoc:
				activeTitle = value.get_title()
				if "Blank" in value.lastTitle and value.get_title() == "":
					activeTitle = value.lastTitle
					# print(activeTitle)
				elif value.lastTitle != activeTitle:
					# print(f"lastTitle vs activeTitle: {value.lastTitle} == {activeTitle}")
					if value.get_title() == "":
						activeTitle = "Blank"
					self.__docLayout.updateTitle(value.lastTitle, activeTitle)
					value.lastTitle = activeTitle
	
	def stickyNoteUpdates(self):
		workspace = self.get_workspace()
		if workspace != None:
			for sticky_note in workspace.existingNotes.values():
				sticky_note.changeWidth()
				sticky_note.changeHeight()
				sticky_note.removeEmptyNote()
	
	def get_refreshRate(self):
		return self.__refreshRate
	
	def set_refreshRate(self, fps):
		self.__refreshRate = int(fps)
	
	##NOTE This will only return the active canvas.
	def get_workspace(self):
		for value in self.__workspace.values():
			if value.activeDoc:
				return value
		return None