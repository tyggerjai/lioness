

from plugins.base import PluginManager

p = PluginManager()
	


COMMANDS = p.getPlugins()

for c,k in COMMANDS.items():
	response = k.command(c.split())
	print(response.getText())


