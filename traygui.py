import gtk
import gobject

import trayicon

import flashcard
import carddb
import jmemorize_db

class TrayApp:
	angle = 0

	def __init__(self):
		# add handler
		self.icon = trayicon.getIcon()
		menu = gtk.Menu()
		menuItem = gtk.MenuItem('run')
		menuItem.connect('activate', self.click_cb)
		menu.append(menuItem)
		menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		menuItem.connect('activate', self.quit_cb, self.icon)
		menu.append(menuItem)

		self.icon.connect('popup-menu', self.popup_menu_cb, menu)
		self.icon.show()

		self.db = jmemorize_db.jMemorizeDB()
		"Add Filter menu Item if backend provides it"
		try:
			flt_menu = self.db.getMenu(menu)
			if flt_menu != None:
				menuItem = gtk.MenuItem('Filter')
				menuItem.set_submenu(flt_menu)
				menu.prepend(menuItem)
		except Exception, e:
			print "Get Cards filter failed: ", e


	def popup_menu_cb(self, widget, button, time, data = None):
		if data:
			data.show_all()
			data.popup(None, None, None, 3, time)

	def click_cb(self, widget):
		term = self.db.getCard()
		flashcard.show(term.tterm, term.tdef)
		gobject.timeout_add(60000,self.click_cb, 0)

	def quit_cb(self, widget, data):
		if data:
			data.hide()
		gtk.main_quit()

	def run(self):
		gtk.main()

