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




# test
#db = jMemorizeDB()
#db.getMenu()

#for i in range(0,3):
#	crd = db.getCard()
#	print 'Term: \n\t', crd.term()
#	print 'Def: \n\t', crd.definition()

