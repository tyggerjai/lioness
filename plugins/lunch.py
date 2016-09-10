from plugins.base import PluginResponse, Plugin
import sys

from random import randint


class lunch(Plugin):	

	prefixes = (
		"Let's go to ",
		"Why not try ",
		"I feel like "
		)

	lunches = (
		'the Korean place',
		'the supermarket',
		'Bay city burrito',
		'Beer deluxe',
		'Haddons',
		'Hawthorn',
		'Kebabji',
		'Le resistance',
		'Lucy\'s Dumplings',
		'Samurai',
		'Santorini',
		'Schnitz',
		'shuji sushi',
		'Spud bar',
		'Subway',
		'The nevermind',
		'The roll place in the plaza', 
		'Zen'
		)
	dbconn = ''

	def __init__(self, dbconn):
		self.keyword = "lunch"
		self.dbconn = dbconn

	def command(self,  text):
		response = PluginResponse()
		response.setText("The usual place")
		

		try:
		
			if (len(text) >1):
				
				resp = self.parse_command(text)
				response.setText(resp)
				
			else:
				response.setText(self.choose_lunch())   
		except: 

			e = sys.exc_info()[0]
			return "NFI {}".format(e)
		return response

	def choose_lunch(self):
		prefix =  self.prefixes[randint(0, len(self.prefixes) -1)]  
		lunches = self.get_lunches()
		lunch = self.lunches[randint(0,len(self.lunches) -1)]
		return prefix + lunch

	def parse_command(self,text):
		resp = ''
			
		if (text[1] == 'list'):
		#	print("listing")
			resp = self.list_lunches()

		elif (text[1] == 'add'):	
			try:
				rname = " ".join(text[2:])
				#rname += ["{} ".format(str(x)) for x in text[2:]]
				
				#print("adding  again {}".format(rname))
				self.dbconn.query("""INSERT INTO `restaurants`(`name`) VALUES (%s)""",
				 (rname,))
			except:
				e = sys.exc_info()[0]
				return "DBI {}".format(e)

		return resp

	def list_lunches(self):
		#print("still listing")
		
		return "\n".join(self.get_lunches())

	def get_lunches(self):
		#print("getting")
		lunches = list()
		for s in self.dbconn.query("SELECT name FROM restaurants", ()):
			#print(s[0])
			lunches.append(s[0])
		return lunches
