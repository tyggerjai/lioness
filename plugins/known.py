#######
# What do we know?
from plugins.base import PluginResponse, Plugin
import sys

class known(Plugin):
	response = PluginResponse()
	keyword="known"
	tablemap = {'users': ('name','Users') ,
				'restaurants': ('name', 'Restaurants')
				}

	def __init__(self):
		pass

	def command(self, dbconn, text):
		respstr = "Well, that went horribly wrong"

		tbl = list()
		if (len(text) > 1):
			tbl = self.tablemap.get(text[1], ())

		if len(tbl) == 0:
			respstr = "I have no idea what you're asking about"
		else:
			querytext = "SELECT {} FROM {};".format(tbl[0],tbl[1])
			print("QUERY: {}".format(querytext))
			qres = dbconn.query(querytext)
			if qres is not None:
				respstr = "I know {} {}!\n".format(len(qres), tbl[1])
				for txt in	qres:
					respstr += str(txt[0]) + "\n"

		self.response.setText(respstr)
		return self.response
		
