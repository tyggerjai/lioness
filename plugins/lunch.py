from plugins.base import PluginResponse, Plugin
from random import randint
import sys

class jibo(Plugin):
	def __init__(self):
		self.keyword = "jibo"
		
	def command(self, text):
		response = PluginResponse()
		response.setText("Why don't you go fuck yourself")
		return response

class lunch(Plugin):	

	prefixes = (
		"Let's go to ",
		"Why not try ",
		"I feel like "
		)

	lunches = (
'the Korean place',
'and the supermarket',
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

	def __init__(self):
		self.keyword = "lunch"

	def command(self, text):
		
		response = PluginResponse()
		response.setText("The usual place")
		
		try:
			if(self.keyword == text[0]):
				response.setText(self.chooseLunch())   
			else:
				response.setText("I have no idea what that is")
		except: 

			e = sys.exc_info()[0]
			print("NFI {}".format(e))
		return response

	def chooseLunch(self):
		prefix =  self.prefixes[randint(0, len(self.prefixes) -1)]  
		lunch = self.lunches[randint(0,len(self.lunches) -1)]
		return prefix + lunch