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

class TrayIcon:
	def show(self):
		return
	def hide(self):
		return
	def connect(self, event, handler):
		return
	def connect(self, event, handler, obj):
		return

class TrayIconGTK(TrayIcon):

	def __init__(self, icon_file):
		self.icon = gtk.StatusIcon()
		self.icon.set_from_file(icon_file)

	def show(self):
			self.icon.set_visible(True)

	def hide(self):
		self.icon.set_visible(False)

	def connect(self, event, handler):
		return self.icon.connect(event, handler)

	def connect(self, event, handler, obj):
		return self.icon.connect(event, handler, obj)

def getIcon():
	return TrayIconGTK("gnome-dev-wavelan.png")

