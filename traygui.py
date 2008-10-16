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
import gobject

from trayicon import TrayIcon

import flashcard
import carddb
import jmemorize_db

class TrayApp:
	slide_interval = 60000
	flip = False

	def __init__(self):
		self.icon = TrayIcon()
		self.icon.connect('activate', self.slide_show_cb)

		# Build menu
		menu = gtk.Menu()
		menuItem = gtk.MenuItem('Start/Stop slide show')
		menuItem.connect('activate', self.slide_show_cb)
		self.slide_show_mode = False
		menu.append(menuItem)
		menuItem = gtk.CheckMenuItem('Flip cards')
		menuItem.connect('activate', self.flip_cb)
		menu.append(menuItem)
		menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		menuItem.connect('activate', self.quit_cb, self.icon)
		menu.append(menuItem)

		self.icon.connect('popup-menu', self.popup_menu_cb, menu)
		self.icon.show()

		# Init cards database
		self.db = jmemorize_db.jMemorizeDB()

		# Add Filter menu Item if backend provides it
		try:
			flt_menu = self.db.getMenu(menu)
			if flt_menu != None:
				menuItem = gtk.MenuItem('Filter')
				menuItem.set_submenu(flt_menu)
				menu.prepend(menuItem)
		except Exception, e:
			print "Unable to get Filter menu from DB: ", e

	def popup_menu_cb(self, widget, button, time, data = None):
		if data:
			data.show_all()
			data.popup(None, None, None, 3, time)

	def slide_show_cb(self, widget):
		if self.slide_show_mode == False:
			self.icon.slideshow()
			self.slide_show_mode = True
			self.slide_show()
			gobject.timeout_add(self.slide_interval,self.slide_show)
		else:
			self.icon.pause()
			self.slide_show_mode = False

	def slide_show(self):
		term = self.db.getCard()
		if self.flip == True:
			flashcard.show(term.tdef, term.tterm)
		else:
			flashcard.show(term.tterm, term.tdef)
		return self.slide_show_mode

	def flip_cb(self, widget):
		if self.flip == True:
			self.flip = Flase
		else:
			self.flip = True

	def quit_cb(self, widget, data):
		if data:
			data.hide()
		gtk.main_quit()

	def run(self):
		gtk.main()

