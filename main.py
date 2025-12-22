##Imports
from Workspace.documentObject import *
from Workspace.dividerObject import *
from Workspace.noteObject import noteBlock
from Application import APP
from Data import *

##Declaring the Program
Window = APP(width=500, height=500)
Document = Document_Object(parent=Window.get_mainApp())
Notes = noteBlock(Document)


Window.set_activeCanvas(Document.get_canvasObj())
Window.set_noteBlock(Notes)

##Event Handling
Document.get_canvasObj().bind("<Button-1>", Document.onClick)
Document.get_canvasObj().bind("<Button-1>", Notes.onClick, add="+")

def refresh():
	##Controls What to do each time the Window Refreshes
	#
	##End of refresh
	Window.get_mainApp().after(Window.get_refreshRate(), refresh)

refresh()
Window.startApp()


