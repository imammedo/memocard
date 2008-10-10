import pynotify


if  pynotify.init("New mail trayicon"):
	print "pynotify initialized"
else:
	print "there was a problem initializing the pynotify module"

class Card:
	def __init__(self, word, definition):
		self.word = word
		self.definition = definition
	def show(self):
		n = pynotify.Notification(self.word, self.definition)
		n.set_timeout(5000)
		n.show()

