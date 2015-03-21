#!/usr/bin/python

"""importing the re module and the Node and Tree classes from a separate place"""

import re
from new_tree import Node, Tree

global identifier_dictionary

identifier_dictionary = {
	'~':'tilda',
	'$':'dollar',
	'#':'hash',
	'&':'ampercent'
}

class Rules():
	"""This class is used for implementing all the LaTeX rules 
	on the incoming string"""


	"""This parameter is used to maintain the index/ position of 
	the parser in the overall string"""

	i = 0

	""" This parameter is used to check whether the control sequence
	tag is finished or not"""

	j = []

	""" This parameter is used to check whether the curly brace
	has closed or not"""

	k = []

	""" This parameter is used to check whether the square brace 
	has closed or not"""

	m = []

	def __init__(self, tex_string):
		self.string = tex_string
		self.broken_list = []
		self.treeCount = 0
		self.allTrees = {}
		self.present_node = None
		self._count = -1
		self._diction = {}
		self.latex_command = None

	def find_present_node(self, node):
		
		self._diction[len(self.j)] = node
		# for each in self._diction.keys():
		# 		print(self._diction[each].tag)


	def check_for_slash(self):
		""" We have an incoming control sequence tag which we 
		need to store"""

		# Because with every slash which is a control sequence, you
		# may/ may not have the squarebrace and curlybrace. That is why
		# 0 is inserted into those lists.

		self.j.append(1)
		self.k.append(0)
		self.m.append(0)


	def check_for_opening_curlybrace(self):
		self.k[-1] += 1
		#print('this is opening curlybrace')

	def check_for_closing_curlybrace(self):
		self.k[-1] -= 1

		if self.k[-1] == 0:
			print(len(self.j))
			del self._diction[len(self.j)]
			self.j.pop(-1)
			self.k.pop(-1)
			self.m.pop(-1)

			try:
				self.present_node = self._diction[max(self._diction.keys())]
			except ValueError:
				self.present_node = None
				self.present_tree.show()

		#print('this is closing curlybrace')

	def check_for_opening_squarebrace(self):
		self.m[-1] += 1
		#print('this is opening curlybrace')

	def check_for_closing_squarebrace(self):
		self.m[-1] -= 1
		#print('this is closing curlybrace')

	def check_for_space(self):
		pass

	def check_the_texString(self):

		while self.i < len(self.string):
			c = self.string[self.i]

			if c == '{':
				#print(c)
				self.broken_list.append(c)
				#alpha = self.opening_curlybrace()

			# elif c == ' ':
			# 	#print(c)
			# 	self.broken_list.append(c)
				
			elif c == '}':
				#print(c)
				self.broken_list.append(c)

			elif c == '\\':
				#print(c)
				self.broken_list.append(c)

			elif c == '~':
				#print(c)
				self.broken_list.append(c)
				
			elif c == ',':
				self.broken_list.append(c)
				#print(c)
				
			elif c == '[':
				self.broken_list.append(c)
				#print(c)
				
			elif c == ']':
				self.broken_list.append(c)
				#print(c)

			else:
				match_text = re.match("[\w]+", self.string[self.i:])
				if match_text:
					#print(match_text.group())
					self.broken_list.append(match_text.group())
					self.i += len(match_text.group()) - 1

			self.i += 1

		print(self.broken_list)

	def broken_list_check(self):
		""" Here we iterate through the broken list"""
		
		self._lastCall = None

		while self._count < len(self.broken_list) - 1:

			self._count += 1

			if self.broken_list[self._count] == '\\':
				self.check_for_slash()
				self._lastCall = 'slash'

			elif self.broken_list[self._count] == '{':

				if (self._count + 1) < len(self.broken_list) and (self.broken_list[self._count + 1]) == '\\':
					self.check_for_slash()
					self.check_for_opening_curlybrace()
					self._lastCall = 'slash'
					self.creating_trees(self.broken_list[self._count + 2])
					self._lastCall = 'open_curly'
					
					# this is assuming that space is not identified as a 
					# separator
					self._count += 2

				else:
					self.check_for_opening_curlybrace()
					self._lastCall = 'open_curly'

			elif self.broken_list[self._count] == '}':

				# The 'if' statement below handles the condition {}{} where 
				# multiple braces are coming. the 'else' statement is general
				# condition.

				if (self._count + 1) < len(self.broken_list) and (self.broken_list[self._count + 1]) == '{':
					self.k[-1] -= 1
				else:
					self.check_for_closing_curlybrace() 
				
				self._lastCall = 'close_curly'
				# self.check_for_closing_curlybrace()
				# self._lastCall = 'close_curly'


			elif self.broken_list[self._count] == '[':
				self.check_for_opening_squarebrace()
				self._lastCall = 'open_square'			

			elif self.broken_list[self._count] == ']':
				self.check_for_closing_squarebrace()
				self._lastCall = 'close_square'

			# elif self.broken_list[self._count] == ' ':
			# 	self._lastCall = 'space'			

			else:
				self.creating_trees(self.broken_list[self._count])

		self.present_tree.show()

	def creating_trees(self, list_value):
		"""this method is used for creating trees and associating nodes
		based on different conditions"""

		if self._lastCall == 'slash':
			self.latex_command = Node(list_value)

			if self.present_node == None:
				self.treeCount += 1
				tree_id = self.treeCount
				self.allTrees[tree_id] = Tree(tree_id)
				self.present_tree = self.allTrees[tree_id]
				self.present_tree.add_node(self.latex_command)

			else:
				self.present_tree.add_node(self.latex_command, self.present_node.identifier)
			
			self.find_present_node(self.latex_command)
			self.present_node = self._diction[max(self._diction.keys())]

		elif self._lastCall == 'open_curly':
			self.present_node.curlybrace_parameter.append(list_value)
			
		elif self._lastCall == 'close_curly':
			#self.present_node = self._diction[max(self._diction.keys())]
			self.present_node.curlybrace_parameter.append(list_value)			
			

if __name__ == '__main__':
	f = open('vitdoc.tex') 
	global tex_data
	tex_data = f.read()	
	print(tex_data)
	rul = Rules(tex_data)
	rul.check_the_texString()
	rul.broken_list_check()


