##Imports
from Application import APP

##Declaring the Program
Window = APP(width=500, height=500)

def refresh():
	##Controls What to do each time the Window Refreshes
	#
	##End of refresh
	Window.get_mainApp().after(Window.get_refreshRate(), refresh)

refresh()
Window.startApp()
