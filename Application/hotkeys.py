##Imports
from pynput import keyboard, mouse

class HOTKEYS:
	def __init__(self):
		## Default Hotkeys
		self.__hotKeys = {
			"Copy" :	"<ctrl>+c",
			"Paste":	"<ctrl>+v",
			"Undo" :	"<ctrl>+z",
			"Redo" :	"<ctrl>+y",
			"Save" :	"<ctrl>+s",
			"Open" :	"<ctrl>+o",
		}
		self.__hotKeyCommands = {}
		self.__hotkeyListener = None

		## Mouse Inputs
		self.__mousePressCommands = {
			"M1" : [],
			"M2" : [],
			"M3" : []
		}
		self.__activeMouseButton = {
			"M1" : False,
			"M2" : False, 
			"M3" : False
			
		}
		self.__mouseListener = None

	def onMove(self, x, y):
		# print(f"Mouse Position: ({x}, {y})")
		pass
	
	def onClick(self, x, y, button, pressed):
		if pressed:
			if button == button.left:
				self.__activeMouseButton["M1"] = True
			if button == button.right:
				self.__activeMouseButton["M2"] = True
			if button == button.middle:
				self.__activeMouseButton["M3"] = True
			# print(f"Mouse Buttons: {self.__activeMouseButton}")
		else:			
			self.__activeMouseButton["M1"] = False
			self.__activeMouseButton["M2"] = False
			self.__activeMouseButton["M3"] = False
			# print(f"Mouse Buttons: {self.__activeMouseButton}")
	
	def onScroll(self, x, y, dx, dy):
		print('Scrolled {0} at {1}'.format(
			'down' if dy < 0 else 'up',
			(x, y)))
	
	def addButtonCommand(self, buttonPress, function):
		self.__mousePressCommands[buttonPress].append(function)

	def addHotkeyCommand(self, key:str, function, shortcut:str=""):
		try:
			##If Shortcut exists - add new command
			if key in self.__hotKeys.keys():
				self.__hotKeyCommands[self.__hotKeys[key]] = function
			##If shortcut deson't exists - set the keybind and the funciton
			elif key not in self.__hotKeys.keys() and shortcut != "":
				self.__hotKeys[key] = shortcut
				self.__hotKeyCommands[shortcut] = function
			else:
				raise AttributeError("Key didn't exist then, when creating was not given a key binding")
		except KeyError as E:
			print(f"Key Error @HOTKEYS.addCommand(): {E}")
			print(f">>Key: {key}\n>>Function: {function}\n>>Shortcut: {shortcut}\n")
		except AttributeError as E:
			print(f"Attribute Error @HOTKEYS.addCommand(): {E}")
			print(f">>Key: {key}\n>>Function: {function}\n>>Shortcut: {shortcut}\n")
			
	##Start/Stop/Restart keyboard Listener
	def restart_hotKeyListener(self):
		self.stop_hotKeyListener() ##Closes original listener
		self.start_hotKeyListener() 
	
	def start_hotKeyListener(self):
		self.__hotkeyListener = keyboard.GlobalHotKeys(self.__hotKeyCommands)
		self.__hotkeyListener.start()
	
	def stop_hotKeyListener(self):
		if self.__hotkeyListener != None:
			self.__hotkeyListener.stop()
	
	##Start/Stop Mouse Listener	
	def start_mouseListener(self):
		self.__mouseListener = mouse.Listener(on_move=self.onMove, on_click=self.onClick)#, on_scroll=self.onScroll)
		self.__mouseListener.start()
		pass

	def stop_mouseListener(self):
		if self.__mouseListener != None:
			self.__mouseListener.stop()
		pass
	
	def get_isMouseButtonPressed(self, button:str):
		return self.__activeMouseButton[button]