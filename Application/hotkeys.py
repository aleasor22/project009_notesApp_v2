##Imports
from pynput import keyboard

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
			
	
	def restart_hotKeyListener(self):
		self.stop_hotKeyListener() ##Closes original listener
		self.start_hotKeyListener() ##Starts new listener - with new set of commands.
	
	def start_hotKeyListener(self):
		self.__hotkeyListener = keyboard.GlobalHotKeys(self.__hotKeyCommands)
		self.__hotkeyListener.start()
	
	def stop_hotKeyListener(self):
		if self.__hotkeyListener != None:
			self.__hotkeyListener.stop()