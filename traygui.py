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
import ConfigParser

from trayicon import TrayIcon

import flashcard
import carddb
import jmemorize_db

class TrayApp:

	def get_default_config(self):
		config = ConfigParser.RawConfigParser()
		config.add_section('GUI')
		config.set('GUI', 'CardWindowY', '15')
		config.set('GUI', 'CardWindowY', '15')
		config.add_section('Learning')
		config.set('Learning', 'SlideTimeout', '10')
		config.set('Learning', 'SlideInterval', '40')
		config.set('Learning', 'FlipSides', 'false')
		config.set('Learning', 'DefaultDB', 'french.jml')
		return config

	def __init__(self):
		self.config = ConfigParser.RawConfigParser()
		try:
			self.config.readfp(open('memocard.cfg'))
		except:
			self.config = self.get_default_config()

		self.flip = self.config.getboolean('Learning', 'FlipSides')

		self.icon = TrayIcon()
		self.icon.connect('activate', self.slide_show_cb)

		# Build menu
		menu = gtk.Menu()
		self.topMenu = menu
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
		self.db.open_db(self.config.get('Learning', 'DefaultDB'))

		# Add Filter menu Item if backend provides it
		try:
			flt = self.db.getFilter()
			flt_menu = self.build_FilterMenu(flt)
			if flt_menu != None:
				menuItem = gtk.MenuItem('Filter')
				menuItem.set_submenu(flt_menu)
				menu.prepend(menuItem)
				menu.connect('hide', self.setToolTip_from_filter)
		except Exception, e:
			print "Unable to get Filter menu from DB: ", e

	def build_FilterMenu(self, filter):
		menu = gtk.Menu()
		menu.connect('button-press-event', self.Filter_Menu_Hide_cb)
		for n in filter:
			menuItem = gtk.MenuItem(n['name'])
			menuItem.set_data('topMenu', self.topMenu)
			menuItem.set_data('data', n['data'])
			menuItem.connect('activate', self.setFilter)
			menuItem.connect('button-press-event',
					self.Filter_Menu_Hide_cb)
			menu.append(menuItem)
			if 'sublevel' in n:
				submenu = self.build_FilterMenu(n['sublevel'])
				if submenu != None:
					menuItem.set_submenu(submenu)
					submenu.set_data('topMenu', self.topMenu)
		return menu

	def setFilter(self, widget):
		'''
		Sets filter in DB using 'data' from activated menuItem
		'''
		self.db.setFilter(widget.get_data('data'))

	def Filter_Menu_Hide_cb(self, widget, event):
		'''
		Makes MenuItem with submenu clickable, hides menu after
		clicking on such item and provides activate signal for leaf
		MenuItems because they do not emmit activate signal when
		button-press-event event is connected to them
		'''
		if isinstance(widget, gtk.Menu):
			widget.popdown()
			m = widget.get_data('topMenu')
			if m != None:
				m.popdown()
		elif isinstance(widget, gtk.MenuItem):
			widget.activate()



	def popup_menu_cb(self, widget, button, time, data = None):
		if data:
			data.show_all()
			data.popup(None, None, None, 3, time)

	def slide_show_cb(self, widget):
		if self.slide_show_mode == False:
			self.icon.slideshow()
			self.slide_show_mode = True
			self.slide_show()
			gobject.timeout_add( self.config.getint('Learning',
				'SlideInterval')*1000, self.slide_show)
		else:
			self.icon.pause()
			self.slide_show_mode = False

	def setToolTip_from_filter(self, widget = None):
		tooltip_text = ''
		try:
			# getFilterDescription may raise exception in case of it is missing
			# in DB Backend, so handle it gracefully
			flt_list = self.db.getFilterDescription()
			while len(flt_list):
				i = flt_list.pop()
				if tooltip_text == '':
					tooltip_text = i
				else:
					tooltip_text = '%s / %s' % (tooltip_text, i)
		except:
			pass

		if tooltip_text == '':
			tooltip_text = 'Empty Filter'
		self.icon.set_tooltip(tooltip_text)

	def slide_show(self):
		term = self.db.getCard()
		if self.flip == True:
			flashcard.show(term.tdef, term.tterm,
					self.config.getint('Learning',
						'SlideTimeout')*1000)
		else:
			flashcard.show(term.tterm, term.tdef,
					self.config.getint('Learning',
						'SlideTimeout')*1000)
		return self.slide_show_mode

	def flip_cb(self, widget):
		if self.flip == True:
			self.flip = False
		else:
			self.flip = True

	def quit_cb(self, widget, data):
		if data:
			data.hide()
		self.config.write(open('memocard.cfg','wb'))
		gtk.main_quit()

	def run(self):
		gtk.main()

