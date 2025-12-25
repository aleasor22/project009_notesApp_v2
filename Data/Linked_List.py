##IMPORTS:
import numpy as NP

__all__ = [
	"LINKED_LIST"
]

class NODE:
	def __init__(self, data, prev=None):
		self.data = data
		self.next = None
		self.prev = prev

class LINKED_LIST:
	def __init__(self):
		self.head = None

	##Adding Elements to the list
	def add_head(self, data):
		if self.head != None:
			newData = NODE(data)
			newData.next = self.head
			newData.next.prev = newData ##The old Head will have a .prev equal to new head.
			self.head = newData
		else:
			self.head = NODE(data)

	def add_tail(self, data):
		# print("Happens?")
		if self.head != None:
			# print(self.findLastElement().data, "END")
			lastElement = self.findLastElement()
			lastElement.next = NODE(data, lastElement)
		else:
			self.head = NODE(data)
	
	##Removes and returns popped element from the list
	def popElement(self, index:int=-1):
		#Pops last element in the list
		try:
			if index == -1:
				if self.findLastElement() == self.head:
					self.popElement(0)
					raise AttributeError("IGNORE")
				
				lastElement = self.findLastElement()
				lastElement.prev.next = None
				return lastElement
			elif index == 0:
				oldHead = self.head
				self.head = self.head.next
				return oldHead
			else:
				target = self.findElementAtIndex(index)
				target.prev.next = target.next
				return target
		except AttributeError as E:
			# print(f"Error #LINKED_LIST.popELement({index})\n>> {E} <<\n")
			return None
			
	def replaceElementAtInddex(self, data, index:int=-1):
		pass

	def findElementAtIndex(self, index:int=-1):
		if index == -1:
			return self.findLastElement()

		curr = self.head
		elementCount = 0
		while curr != None:
			if elementCount == index:
				return curr
			
			##Next element in list
			curr = curr.next
			elementCount += 1
		
	def findLastElement(self):
		curr = self.head
		while curr.next != None:
			curr = curr.next
		return curr

	def printList(self):
		curr = self.head
		while curr != None:
			print(curr.data, end=" -> ")
			curr = curr.next
		print()

##Used for Testing Linked_List Features
# test = LINKED_LIST()

# test.add_head(10)
# test.add_head(5)
# test.add_head(39)
# test.add_head(23)

# print("Original")
# test.printList()

# # print(test.findElementAtIndex().data)
# # print(test.popElement().data)
# print(test.popElement(0).data)

# print("Post-Edits")
# test.printList()