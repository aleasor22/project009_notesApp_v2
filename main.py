##Imports
from Application import APP

##Declaring the Program
Window = APP(width=1280, height=720)

def refresh():
	##Controls What to do each time the Window Refreshes
	Window.updates()
	#
	##End of refresh
	Window.get_mainApp().after(Window.get_refreshRate(), refresh)

refresh()
Window.startApp()
