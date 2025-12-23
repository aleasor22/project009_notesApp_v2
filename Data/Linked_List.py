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
# test.add_tail("Last 1")
# test.add_head(39)
# test.add_head(23)
# test.add_tail("Last 2")

# test.printList()