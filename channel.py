#############
# Channel module for tracking which channels to listen in, and 
# channel ops etc.


class ChannelManager():
	lookup = dict()
	revlookup = dict()
	channels = { "join": ("bot_testing", "general"),
			"known": list(),
			"watching": list()
	}
	def __init__(self):
		pass

	def getChannels(self):
		return self.channels;
	
	def setLookup(self, cid, name):
		self.lookup[cid] = name
		self.revlookup[name] = cid

	def getName(self, cid):
		return self.lookup.get(cid)