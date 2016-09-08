from pathlib import Path
import imp
import sys


class PluginResponse(object):
	_text = ''
	def __init__(self):
		pass
	def setText(self, text):
		self._text = text
	def getText(self):
		return str(self._text)

class Plugin(object):
	pass

class PluginManager():
	COMMANDS = dict()
	dbconn = ''

	def __init__(self, dbconn):
		self.dbconn = dbconn
		self.initPlugins()
		#print(dbconn)
		

	def initPlugins(self):
		COMMANDS={}
		self.findPlugins()
		self.registerPlugins();

		

	def findPlugins(self):
		plugpath = Path("plugins")
		plugins = [list(plugpath.glob('*.py'))]
#		print(plugins)
		for pg in plugins[0]:
			pp = str(pg)
			pp = pp[:-3]
			#print("LOOKING FOR {}".format(pp))
			
			if (pp != "plugins/base"):
#				print("--Loading {}".format(pp))
				try:
					p = imp.find_module(pp)

					pl = imp.load_module(pp, p[0], p[1], p[2])
				except:
					e = sys.exc_info()[0]

					print("----  Could not load: {}".format(e))		
		
	def registerPlugins(self):
		
		for plugin in Plugin.__subclasses__():
			print(plugin)
				
			obj= plugin(self.dbconn)
			print("--Registering {}".format(obj.keyword))
		
			self.COMMANDS[obj.keyword] = obj

	def getPlugins(self):
		return self.COMMANDS
