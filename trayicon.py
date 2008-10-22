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

class TrayIcon(gtk.StatusIcon):

	def __init__(self):
		gtk.StatusIcon.__init__(self)

	def show(self):
		self.set_from_file('mc_main.png')
		self.set_visible(True)

	def hide(self):
		self.set_visible(False)

	def pause(self):
		self.set_from_file('mc_pause.png')

	def slideshow(self):
		self.set_from_file('mc_slideshow.png')
