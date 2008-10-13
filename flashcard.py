import gtk
import gobject

has_pynotify = False 

try:
	import pynotify
	if  pynotify.init("memocard"):
		print "pynotify initialized"
	else:
		print "there was a problem initializing the pynotify module"

	has_pynotify = True

	class CardGNotify(Card):
		def __init__(self, word, definition):
			self.word = word
			self.definition = definition
		def show(self):
			n = pynotify.Notification(self.word, self.definition)
			n.set_timeout(5000)
			n.show()
except:
	print "no pynotify loaded"

def show(word, definition):
	if has_pynotify == True:
		n = pynotify.Notification(word, definition)
		n.set_timeout(10000)
		n.show()
	else:
		msg = "%s\n%s" % (word, definition)
		win = gtk.Window(type=gtk.WINDOW_POPUP)
		#win = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
		win.add(gtk.Label(msg))
		win.set_decorated(False)
		win.set_gravity(gtk.gdk.GRAVITY_SOUTH_EAST)
		win.move(10,10)
		win.stick()
		win.show_all()
		gobject.timeout_add(10000, win.destroy)


