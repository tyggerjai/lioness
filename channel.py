#############
# Channel module for tracking which channels to listen in, and 
# channel ops etc.


class ChannelManager():
	channels = { "join": ("bot_testing"),
			"known": list(),
			"watching": list()
	}
	def __init__(self):
		pass

	def getChannels(self):
		return self.channels;
	