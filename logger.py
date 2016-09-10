##########
# Various lioness utilities
#####

class Logger():
	def __init(self, level, file):
		self.DEBUGLEVEL = level
		self.file = file

	def log(level, message):
		if (level < self.DEBUGLEVEL):
			with open(self.file, a) as f:
				f.write(message)