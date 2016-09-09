########
# Fetches jargon file entries
######
from plugins.base import PluginResponse, Plugin
import sys
import requests
import html2text

class jargon(Plugin):
	def __init__(self, dbconn):
		self.keyword = "jargon"
		self.response = PluginResponse()

	def command(self, text):
		self.response.setText("Nope")
		if (len(text) >1):
			searchstr = "-".join(text[1:])
			#print(text[1])
			cap = text[1][0].upper()
			url = "http://www.catb.org/jargon/html/{}/{}.html".format(cap, searchstr)
			#print(url)
			resp = requests.get(url)
			if (resp.status_code == 200):
			#print(resp)
				txt = html2text.html2text(resp.text).split("\n")
				txt = txt[6:-6]
				if (len(txt) > 15):
					txt = txt[:15]
			
					txt[-1] += "\n(more ...)\n "
			
				
				txt.append("\n" + url)

				txt = "\n".join(txt)
				self.response.setText(txt)
				
			else:

				self.response.setText("I couldn't find that url!")
		return self.response
