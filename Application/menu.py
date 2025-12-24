##IMPORTS
import tkinter
from .event import EVENTS

##Handles creation of a popup tk-Window
class POPUP():
	def __init__(self, myTitle:str):
		##Sets up the Pop-up
		self.root = tkinter.Tk()
		self.root.title(myTitle)
		self.root.geometry("500x500")

	##Pushes the Popup to display on screen
	def runPopUp(self):
		self.root.mainloop()

class MENU(EVENTS):
	def __init__(self):
		EVENTS.__init__(self)
		self.__mainMenu = None

		##Parent Menu Dropdowns
		self._parentMenus = {
			"File":		None,
			"Edit":		None,
			"View":		None,
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
			if key == "Settings":
				continue
			self._parentMenus[key] = tkinter.Menu(self.__mainMenu, tearoff=False)
			self.__mainMenu.add_cascade(label=key, menu=self._parentMenus[key])
		
		# self._parentMenus["Settings"] = tkinter.Menu(self.__mainMenu, )
		self.__mainMenu.add_command(label="Settings", command=self.settingsPopup)

		self._mainApp.config(menu=self.__mainMenu)
	
	def settingsPopup(self):
		settings = POPUP("Settings")
		self._settingsPopup = settings.root
		settings.runPopUp()

	def createChildMenu(self, root:str, childLabel:str, function):
		self._childMenus[root].append((childLabel, function))
	
	def childMenuPush(self):
		for key, value in self._childMenus.items():
			if len(value) > 0:
				##tuple = ("Menu Label", function)
				for tuple in value:
					self._parentMenus[key].add_cascade(label=tuple[0], command=tuple[1])
