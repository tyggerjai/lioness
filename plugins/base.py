from pathlib import Path
import imp

#import plugins.fish




class Plugin(object):
	pass

class PluginManager():
	COMMANDS = dict()

	def __init__(self):
		self.init_plugins()
		self.register_plugins()

	def init_plugins(self):
		
		self.find_plugins()
		self.register_plugins();

		

	def find_plugins(self):
		plugpath = Path("plugins")
		plugins = [list(plugpath.glob('*.py'))]
		#print(plugins)
		for pg in plugins[0]:
			pp = str(pg)
			pp = pp[:-3]
			#print("LOOKING FOR {}".format(pp))
			
			if (pp != "plugins/base"):
				#print("LOADING {}".format(pp))
			
				p = imp.find_module(pp)

				pl = imp.load_module(pp, p[0], p[1], p[2])
				
		
	def register_plugins(self):
		
		for plugin in Plugin.__subclasses__():
			
			obj= plugin()
			print("Registering {}".format(obj.keyword))
			self.COMMANDS[obj.keyword] = obj

	def getPlugins(self):
		return self.COMMANDS
