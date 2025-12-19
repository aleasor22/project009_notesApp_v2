##Relavant Imports
import tkinter.font as tkFont
from pynput import keyboard

class myString:
	def __init__(self):
		self._myString = ""
		self._wordsInString = []
	
	def set_myString(self, string:str):
		self._myString = string

	def get_myString(self):
		return self._myString

	def get_wordsInString(self):
		return self._wordsInString

	def get_indexOfWord(self, targetWord:str):
		"""Returns Index of Given Word, Returns None if not found."""
		for index in range(len(self._wordsInString)):
			if self._wordsInString[index] == targetWord:
				return index
		return None
	
class modMyString(myString):
	def __init__(self):
		myString.__init__(self)
	
	def sortMyString(self, newString:str = ""):
		try:
			if newString == "" and self._myString == "":
				raise AttributeError("No String to Manipulate")
			
			if newString != "":
				self._myString = newString
			
			currWord = ""
			for char in self._myString:
				if char.isspace() or char == ",":
					self._wordsInString.append(currWord)
					currWord = ""
					continue
				currWord += char
			
			print(f"Result: {self._wordsInString}")
		except AttributeError as E:
			print(f"Caught Error @modMyString.sortMyString()\n>>{E}")