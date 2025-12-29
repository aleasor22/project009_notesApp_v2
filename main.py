##Imports
import _tkinter
from Application import APP

##Declaring the Program
Window = APP(width=1280, height=720)

def refresh():
	##Controls What to do each time the Window Refreshes
	try:
		## Refresh Calls
		if Window.startUpComplete and not Window.shutdown: #Post Startup Refresh.
			Window.navigationUpdates()
			Window.stickyNoteUpdates()

			##Action's based on Mouse Button 1 pressed
			if Window.get_isMouseButtonPressed("M1"):
				# print(Window.get_isMouseButtonPressed("M1"))
				Window.get_workspace().noteMove(Window.get_mousePos())
				Window.get_workspace().manualChangeWidth(Window.get_mousePos())
			else:
				Window.get_workspace().noteMoveOff()
				Window.get_workspace().manualWidthOff()
				
	except _tkinter.TclError as E:
		print(f"Canvas Object Error:\n>> {E}")

	##End of refresh
	Window.get_mainApp().after(Window.get_refreshRate(), refresh)

refresh()
Window.startApp()
