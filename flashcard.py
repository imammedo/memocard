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

	has_pynotify = True
except:
	pass

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


