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

has_pynotify = False

try:
	import pynotify
	if  pynotify.init("memocard"):
		pass
	else:
		pass

#	has_pynotify = True
except:
	pass

def show(word, definition, timeout = 10000):
	if has_pynotify == True:
		n = pynotify.Notification(word, definition)
		n.set_timeout(10000)
		n.show()
	else:
		l1 = gtk.Label('<span foreground="blue" size="large"><b>%s</b></span>' % word)
		l1.set_use_markup(True)
		l1.set_alignment(xalign=0, yalign=0.5)

		l2 = gtk.Label('<span foreground="black" size="medium"><b>%s</b></span>' %definition)
		l2.set_use_markup(True)
		l2.set_alignment(xalign=0, yalign=0.5)

		tbl = gtk.Table(2,1)
		tbl.attach(l1, 0, 1, 0, 1, xpadding=5, ypadding=5)
		tbl.attach(l2, 0, 1, 1, 2, xpadding=5, ypadding=5)

		frame = gtk.Frame()
		frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
		frame.show()
		frame.add(tbl)

		win = gtk.Window(type=gtk.WINDOW_POPUP)
		win.set_geometry_hints(None, 160, 50)
		win.add(frame)
		win.connect('configure-event', placement_cb)

		x = win.get_screen().get_width() - 160 - 2
		y = win.get_screen().get_height() - 50 - 38
		win.move(x, y)
		win.show_all()
		gobject.timeout_add(timeout, win.destroy)

def placement_cb(widget, event = None):
	width, height = widget.get_size()
	x = widget.get_screen().get_width() - width - 2
	y = widget.get_screen().get_height() - height - 38
	widget.move(x, y)
