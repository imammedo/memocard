import carddb
import xml.dom.minidom
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
		self.dom = xml.dom.minidom.parse('french.jml')
		self.cards = self.dom.getElementsByTagName('Card')
		self.index = 0

	def getCard(self):
		i = random.randint(0, self.cards.length)
		node = self.cards.item(i)
		i = i + 1
		try:
			c = jMemorizeCard(node.getAttribute('Frontside'),
				node.getAttribute('Backside'))
		except AttributeError, e:
			c = self.getCard();
		return c

# test
#db = jMemorizeDB()
#for i in range(0,3):
#	crd = db.getCard()
#	print 'Term: \n\t', crd.term()
#	print 'Def: \n\t', crd.definition()

