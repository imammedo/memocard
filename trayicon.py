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
		#self.img = gtk.Image()
		#self.img.set_from_pixbuf(self.icon.get_pixbuf())
		
	def show(self):
			self.icon.set_visible(True)

	def hide(self):
			self.icon.set_visible(False)
	def connect(self, event, handler):
		return self.icon.connect(event, handler)
	def connect(self, event, handler, obj):
		return self.icon.connect(event, handler, obj)

def getIcon():	
	try:
		import egg.trayicon
	except:
		return TrayIconGTK("gnome-dev-wavelan.png")

