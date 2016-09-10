####################
# Command handler for Lioness bot. This is where the heavy lifting happens.
###
from plugins.base import PluginManager
import re

class CommandArgs():
	def __init__(self):
		self.user = ''
		self.command = ''
		self.string = ''

class CommandResponse():
	
	def __init__(self, chan):
		self.channel = chan

class Commander():

	def __init__(self, dbconn, log):
		self.dbconn = dbconn;
		self.log = log
		
		plugin = PluginManager(dbconn)
		self.commands = plugin.get_plugins()

	def handle(self, args):
		response = CommandResponse()
		
		self.log.debug(2,"Message from {}: {}".format(user, msg))
		self.log.debug(2, "Parsed: {}".format( comstring))


		opts, content = parse_opts(args.text)

		if (self.plugins.get(args.command)):
			try:
				self.log.debug(0, " ({})trying {}".format(cname, cmd))
				response = plugins[cmd].command(comstring) 
				self.log.debug(0, response)

				chanpost(cname, "{}".format(response.getText()))
			except:
				e = sys.exc_info()[0]

				
				self.log.debug(0, "Could not perform plugin! ")


		elif (user in ops):
			if (cmd == 'die'):
				self.log.debug(0, "{} says die!".format(user))
				_connect = 0
			elif (cmd == 'hup'):
				_connect = 2
			elif (cmd == 'self.log.debug' ):
				try:
					lev = int(comstring[1])
					DEBUG_LEVEL = lev
					chanpost("#bot_testing", "Setting self.log.debug level to {}".format(lev))
				except:
					chanpost("#bot_testing", "Cannot set level {}".format(lev))
			else:
				chanpost("#bot_testing","What you talkin about, Willis?")
		else:
			chanpost(cname, "I have no idea what you are asking me to do.")

	def parse_opts(self, text):
		opts = dict()
		content = ''
		key = ''
		for token in text.split():
			if re.match("-", token):
				key = token
				while (key[0] == "-"):
					key = key[1:]

			else:
				if key != ''
					opts[key] = token
					key = ''
				else:
					content += str(token) + " "


