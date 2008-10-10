import gtk
import egg.trayicon
import gobject
import threading

import flashcard
import carddb
import jmemorize_db

class TrayApp:
	angle = 0

	def __init__(self):
		self.icon = egg.trayicon.TrayIcon("mail-message-new")
		eventbox = gtk.EventBox()
		self.icon.add(eventbox)

		icon_theme = gtk.icon_theme_get_default()
		try:
			self.icon_pixbuf = icon_theme.load_icon("mail-message-new", gtk.ICON_SIZE_SMALL_TOOLBAR, 0)
		except gobject.GError, exc:
			print "can't load icon", exc

		self.img = gtk.Image()
		self.img.set_from_pixbuf(self.icon_pixbuf)
		eventbox.add(self.img)

		# add handler
		eventbox.connect("button-release-event", self.click_cb)

		# start animation
		gobject.timeout_add(5,self.rotate_cb)
		gobject.threads_init()

		self.db = jmemorize_db.jMemorizeDB()

	def rotate_cb(self):
		self.angle = self.angle +90
		alpha_pixbuf = self.icon_pixbuf.rotate_simple(self.angle)
		self.img.set_from_pixbuf(alpha_pixbuf)
		#gobject.timeout_add(800,self.rotate_cb)
	
	def click_cb(self, widget, event):
		while gtk.events_pending():
			gtk.main_iteration()
		gobject.timeout_add(1000,self.click_cb2)

	def click_cb2(self):
		term = self.db.getCard()
		c = flashcard.Card(term.term(),term.definition())
		c.show()
		gobject.timeout_add(20000,self.click_cb2)

	def run(self):
		mainloop = gobject.MainLoop()
		self.icon.show_all()
		mainloop.run()


