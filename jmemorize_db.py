#!/usr/bin/python
# vim: set fileencoding=utf-8

#    Copyright © 2008 Igor Mammedov,
#    Contact email: igor@mammed.net
#
#    This file is part of MemoCard.
#
#    MemoCard is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MemoCard is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MemoCard.  If not, see <http://www.gnu.org/licenses/>.


import carddb
import xml.dom.minidom
from xml import xpath
import random
import zipfile

class jMemorizeCard(carddb.Card):
	def __init__(self, tterm, tdef):
		self.tterm = tterm
		self.tdef = tdef
	def term(self):
		return self.tterm
	def definition(self):
		return self.tdef


class jMemorizeDB(carddb.db):
	def __init__(self):
		#self.doc = xml.dom.minidom.parse('french.jml')
		#self.cards = self.doc.getElementsByTagName('Card')
		#self.index = 0
		pass

	def open_db(self, db_file):
		if zipfile.is_zipfile(db_file):
			try:
				z = zipfile.ZipFile(db_file, "r")
				for filename in z.namelist():
					bytes = z.read(filename)
					print filename
					print len(bytes)
					self.doc = xml.dom.minidom.parseString(bytes)
			except Exception, e:
				print e
				return
		else:
			self.doc = xml.dom.minidom.parse(db_file)

		self.cards = self.doc.getElementsByTagName('Card')
		self.index = 0

	def getCard(self, is_random = True):

		if is_random == True:
			index = random.randint(0, self.cards.length)

		node = self.cards.item(index)
		index = index + 1
		try:
			c = jMemorizeCard(node.getAttribute('Frontside'),
				node.getAttribute('Backside'))
		except AttributeError, e:
			c = self.getCard();
		return c

	def getFilter(self, node = None):
		if node == None:
			node = self.doc.documentElement

		nodes = xpath.Evaluate('./Category[@name]',
				node)
		if len(nodes) == 0:
			return None

		level = []
		for n in nodes:
			elem = {}
			elem['name'] = n.getAttribute('name')
			elem['data'] = n
			sublevel = self.getFilter(n)
			if sublevel != None:
				elem['sublevel'] = sublevel
			level.append(elem)
		return level

	def setFilter(self, branch_node):
		self.filter = branch_node
		self.cards = self.filter.getElementsByTagName('Card')

	def getFilterDescription(self):
		'''Returns list of selected categories in db'''
		try:
			node = self.filter
		except:
			return []

		selector = [ self.filter.getAttribute('name') ]
		while node.parentNode.nodeName == 'Category':
			node = node.parentNode
			selector.append(node.getAttribute('name'))
		return selector

