from database import DataBase
import yaml

from plugins.base import PluginManager

def load_configs():
	try:
		with  open("conf.yaml", "r") as conf_file:
			conf = yaml.load(conf_file)
	except :
		e = sys.exc_info()[0]

		print("Could not load: {}".format(e))
		conf = dict()
	return conf

config = load_configs()

print(config)
dbconn = DataBase(config['dbname'], config['username'], config['passwd'])
print(dbconn.showtables())

p = PluginManager()
	
TEXTRAS = {'lunch': ("list",),
			'known': ("fish", "users")}

COMMANDS = p.getPlugins()

for c,k in COMMANDS.items():
	print ("------TESTING {}".format(c))
	args = list()
	args.append(c)
	
	response = k.command(dbconn, args)
	print(response.getText())
	
	if (len(TEXTRAS.get(c, ())) > 0):
		args = list()
		args.append(c)
		for i in TEXTRAS.get(c):
			args.extend( i.split())

			print("\n-\n")
			print(args)

			response = k.command(dbconn, args )
			print(response.getText())
			
	
	print("\n----\n ")
