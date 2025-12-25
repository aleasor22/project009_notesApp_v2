##Imports
import _tkinter
from Application import APP

##Declaring the Program
Window = APP(width=1280, height=720)

def refresh():
	##Controls What to do each time the Window Refreshes
	Window.navigationUpdates()
	Window.stickyNoteUpdates()
	try:
		if Window.get_isMouseButtonPressed("M1"):
			# print(Window.get_isMouseButtonPressed("M1"))
			Window.get_workspace().noteMove(Window.get_mousePos())
			Window.get_workspace().manualChangeWidth(Window.get_mousePos())
			
		##Can't  use "else:" due to workspace's not being declaired when refresh() starts
		elif not Window.get_isMouseButtonPressed("M1") and Window.get_workspace() != None:
			Window.get_workspace().noteMoveOff()
			Window.get_workspace().manualWidthOff()
	except _tkinter.TclError as E:
		print(f"Canvas Object Error:\n>> {E}")

	##End of refresh
	Window.get_mainApp().after(Window.get_refreshRate(), refresh)

refresh()
Window.startApp()
