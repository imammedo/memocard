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


import gtk
import carddb
import xml.dom.minidom
from xml import xpath
import random

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
		self.doc = xml.dom.minidom.parse('french.jml')
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

	def getMenu(self, topMenu, node = None):
		if node == None:
			node = self.doc.documentElement

		nodes = xpath.Evaluate('./Category[@name]',
				node)
		if len(nodes) == 0:
			return None

		menu = gtk.Menu()
		menu.connect('button-press-event', self.setFilter)
		for n in nodes:
			menuItem = gtk.MenuItem(n.getAttribute('name'))
			menuItem.connect('activate', self.prepareFilter)
			menuItem.set_data('cardNode', n)
			menuItem.set_data('topMenu', topMenu)
			menuItem.connect('button-press-event', self.setFilter)
			menu.append(menuItem)
			submenu = self.getMenu(topMenu, n)
			if submenu != None:
				menuItem.set_submenu(submenu)
				submenu.set_data('topMenu',topMenu)

		return menu

	def prepareFilter(self, widget):
		self.filter = widget.get_data('cardNode')
		self.cards = self.filter.getElementsByTagName('Card')
		print 'Set filter by node: ', self.filter.getAttribute('name')

	def setFilter(self, widget, event):
		if isinstance(widget, gtk.Menu):
			widget.popdown()
			m = widget.get_data('topMenu')
			if m != None:
				m.popdown()
		elif isinstance(widget, gtk.MenuItem):
			widget.activate()

