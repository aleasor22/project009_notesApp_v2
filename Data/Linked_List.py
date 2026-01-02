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
		self.length = 0

	##Adding Elements to the list
	def add_head(self, data):
		if self.head != None:
			newData = NODE(data)
			newData.next = self.head
			self.head.prev = newData ##The old Head will have a .prev equal to new head.
			self.head = newData
		else:
			self.head = NODE(data)
		
		print("add_head - Prev =", self.head.prev)
		self.length += 1

	def add_tail(self, data):
		# print("Happens?")
		if self.head != None:
			# print(self.findLastElement().data, "END")
			lastElement = self.findLastElement()
			lastElement.next = NODE(data, lastElement)
		else:
			self.head = NODE(data)
		
		print("add_tail - Prev =", self.findLastElement().prev)
		self.length += 1

	def replaceElementAtIndex(self, data, index:int=-1):
		"""Replaces the element at a given index. If no  index is given, replace the last element"""
		#Original
		## prev -> target -> next

		#Replaced
		## prev -> newItem -> target.next

		if index == -1:
			target = self.findLastElement()
			if target == self.head:
				self.head = NODE(data, prev=target.prev)
				return
			
			newItem = NODE(data, prev=target.prev)
			target.prev.next = newItem ##Makes the previous element point to newItem
			newItem.next = target.next ##Makes the newItem point to old elements next point
			return
		else:
			target = self.findElementAtIndex(index)
			if index == self.length:
				raise IndexError(f"Can't be last element")
			if target == self.head:
				self.head = NODE(data, prev=target.prev)
				return

		newItem = NODE(data, prev=target.prev)
		print(f"Target: >>{target.data}<<")
		target.prev.next = newItem ##Makes the previous element point to newItem
		newItem.next = target.next ##Makes the newItem point to old elements next point
		target.next.prev = newItem ##Updates the next elements previous element to newItem
	
	
	def insertElementAtIndex(self, data, index:int=-1):
		if index == -1:
			self.add_head(data)
		
		new = NODE(data)
		target = self.findElementAtIndex(index)
		print(f"Target: {target.data}")
		target.prev.next = new
		new.next = target
		target.prev = new
		
		self.length += 1

	##Removes and returns popped element from the list
	def popElement(self, index:int=-1):
		"""Removes and Returns an element at the given index, Default is end of list"""
		if not self.isEmpty():
			#Pops last element in the list
			if index == -1:
				##Pops head if that's the only element
				if self.findLastElement() == self.head:
					oldHead = self.head
					self.head = None
					self.length = 0
					return oldHead

				##Pops last element in list
				lastElement = self.findLastElement()
				lastElement.prev.next = None
				self.length -= 1
				return lastElement
			elif index == 0:
				##Pops head of list
				oldHead = self.head
				self.head = self.head.next
				self.length -= 1
				return oldHead
			else:
				##Pops element at a given index
				target = self.findElementAtIndex(index)
				target.prev.next = target.next
				self.length -= 1
				return target
	
		return None

	def findElementsInRange(self, start:int=0, end:int=-1, step:int=1):
		"""Returns a linked list of the elements specified in range(start, end) end is inclusive"""
		##By Default, iterate to end of list
		if end == -1:
			end = self.length-1

		try:
			if start < 0 or start > self.length-1:
				raise IndexError(f"Start index out of range: {start}")
			elif end < 0 or end > self.length-1:
				raise IndexError(f"End index out of range: {end}")
			elif step != 1 and step != -1:
				raise IndexError(f"Incorrect Step size: {step}\nMust be -1 or 1")

			newList = LINKED_LIST()
			curr = self.findElementAtIndex(start)

			##Determins if the system is looping front to back or back to front.
			##Recursion?
			if step == 1:
				myBool = curr != self.findElementAtIndex(end).next
			else:
				myBool = curr != self.findElementAtIndex(end).prev

			while myBool:
				if curr == None:
					break

				newList.add_tail(curr.data)

				if step == 1:
					curr = curr.next
					myBool = curr != self.findElementAtIndex(end).next
				elif step == -1:
					curr = curr.prev
					myBool = curr != self.findElementAtIndex(end).prev

			return newList
			
		except IndexError as E:
			print(f"Error @LINKED_LIST.findElementsInRange\n>> {E} <<")
			return None
		except AttributeError as E:
			print(f"Error @LINKED_LIST.findElementsInRange\n>> {E} <<")
			return None

	def findElementAtIndex(self, index:int=-1):
		if index == -1:
			return self.findLastElement()
		elif index >= self.length:
			raise IndexError(f"IndexError:  Index of '{index}' is out of Range\n@LINKED_LIST.findElementAtIndex")
		elif self.isEmpty():
			raise IndexError(f"IndexError: List is Empty\n@LINKED_LIST.findElementAtIndex")

		curr = self.head
		elementCount = 0
		while curr != None:
			if elementCount == index:
				return curr
			
			##Next element in list
			curr = curr.next
			elementCount += 1
		
	def findLastElement(self):
		try:
			if self.isEmpty():
				raise IndexError(f"IndexError: List is Empty\n@LINKED_LIST.findElementAtIndex")
			curr = self.head
			while curr.next != None:
				curr = curr.next
			return curr
		except AttributeError as E:
			return self.head

	def isEmpty(self):
		if self.head == None:
			return True
		return False

	def printList(self):
		curr = self.head
		while curr != None:
			if curr.next == None:
				print(curr.data, end=" :END")
			else:
				print(curr.data, end="->")
			curr = curr.next
		print()

##Used for Testing Linked_List Features
# test = LINKED_LIST()

# test.add_head("END")
# test.add_head(10)
# test.add_head(5)
# test.add_head(39)
# test.add_head(23)
# test.add_head(40)
# test.add_head("Start")

# print("Original")
# test.printList()

# # print(test.findElementAtIndex().data)
# # print(test.popElement().data)
# print(test.popElement(0).data)
# test.insertElementAtIndex("new", 2)
# myRange =  test.findElementsInRange(test.length-1, 3, step=-1)
# print("myRange: ")
# myRange.printList()

# print("Post-Edits")
# test.printList()