import gtk

import trayicon

#import flashcard
import carddb
import jmemorize_db

class TrayApp:
	angle = 0

	def __init__(self):
		# add handler
		menu = gtk.Menu()
		menuItem = gtk.MenuItem('run')
		menuItem.connect('activate', self.click_cb)
		menu.append(menuItem)

		self.icon = trayicon.getIcon()
		self.icon.connect('popup-menu', self.popup_menu_cb, menu)
		self.icon.show()

		self.db = jmemorize_db.jMemorizeDB()

	def popup_menu_cb(self, widget, button, time, data = None):
		#if button == 3:
		if data:
			data.show_all()
			data.popup(None, None, None, 3, time) 
		
	def click_cb(self, widget):
		term = self.db.getCard()
		win = gtk.Window()
		win.maximize()
		win.show()
		#gobject.timeout_add(1000,self.click_cb2)

	def run(self):
		gtk.main()

