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
		word = word.encode('utf-8')
		word = word.replace('\n','<br/>')
		definition = definition.encode('utf-8')
		definition = definition.replace('\n','<br/>')

		win = gtk.Window(type=gtk.WINDOW_POPUP)
		#win.set_gravity(gtk.gdk.GRAVITY_SOUTH_EAST)

		from htmltextview import HtmlTextView
		htmlview = HtmlTextView()
		htmlview.set_left_margin(5)
		htmlview.set_right_margin(5)
		htmlview.set_wrap_mode(gtk.WRAP_NONE)
		text = '<body><div style="color:blue;font-size:large;font-weight:bold;font-family:serif">%s</div>%s</body>' % (word, definition)
		htmlview.display_html(text)
		htmlview.show()

		frame = gtk.Frame()
		frame.set_shadow_type(gtk.SHADOW_IN)
		frame.show()
		frame.add(htmlview)
		win.add(frame)
		win.connect('configure-event', placement_cb)
		win.show()
		win.realize()
		desktop_type = gtk.gdk.atom_intern("_NET_WM_WINDOW_TYPE_DESKTOP", False)
		print desktop_type
		win.window.property_change(gtk.gdk.atom_intern("_NET_WM_WINDOW_TYPE", False),
				gtk.gdk.atom_intern("ATOM", False), 32,
				gtk.gdk.PROP_MODE_REPLACE,['_NET_WM_WINDOW_TYPE_NOTIFICATION'])


		win.show_all()

		#width, height = win.get_size()
		#x = win.get_screen().get_width() - width
		#y = win.get_screen().get_height() - height
		#print 'a: ', width, ':', height
		#win.move(x, y)
		gobject.timeout_add(timeout, win.destroy)

def placement_cb(widget, event):
	width, height = widget.get_size()
	x = widget.get_screen().get_width() - width
	y = widget.get_screen().get_height() - height
	#widget.move(x, y)
