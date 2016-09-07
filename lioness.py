import time
import sys
from slackclient import SlackClient
import re
from channel import ChannelManager
from users import UserManager
from plugins.base import PluginManager


DEBUG_LEVEL = 3

def debug(level, message):
	if (level < DEBUG_LEVEL):
		print(message)

mytoken = ""
with open("API.key") as api:
	mytoken = api.readline().strip()
	api.close()


debug(0, "+++++++++++++++++++++++++++++\n++STARTING\n")

sc = SlackClient(mytoken)

_connect = 1
chanman = ChannelManager()
channels = chanman.getChannels()

people = UserManager()
owners = people.getOwners()

plugin = PluginManager()

debug(1,"Channels to join:")
debug(1,channels['join'])

ops = [owners[own]['id'] for own in owners.keys()]


def connect_to_server():
	
	if (sc.rtm_connect()):
		ping_owners("Here I am!")
		return 1
	return 0

def disconnect():
	#sc.rtm_disconnect()
	return 1

def chanpost(mychannel, message):
	resp = sc.api_call(
    	"chat.postMessage", channel=mychannel, text=message,
    	 username="lioness", icon_url="https://avatars.slack-edge.com/2016-05-12/42349083605_6f1c7e1101ff3fb069d3_48.png"
	)


def ping_owners(message):
	for owner in owners.keys():
		own = owners[owner]
		resp = sc.api_call("im.open", user = own['id'])
		own['chat'] = resp['channel']['id']
		debug(1, "Pinging owner {}".format(own))
		debug(1,sc.api_call("chat.postMessage", as_user="true:", channel=own['chat'], text=message))


def reload_plugins():
	plugin.initPlugins()
	return 	plugin.getPlugins()


debug(1,"Starting ... \n")
debug(1,"My owners are: ")

for own in owners.keys():
	debug(1, own)

if (connect_to_server()):

	plugins = reload_plugins()

	debug(1, "Checking API")
	debug (1, sc.api_call("api.test"))
	#DEBUG_LEVEL = 0


	


	chans = sc.api_call("channels.list")
	for chan in chans['channels']:
		chanman.setLookup(chan['id'], chan['name'])		
	
		debug(3,"{} : {}".format(chan['name'], chan['id']))
		channels['known'].append(chan['name'])

		if (chan['name'] in channels['join']):

			debug(2, "Found watching channel {}".format(chan['name']))
			channels['watching'].append(chan['id'])

	for chan in channels['watching']:
		debug(3,"Watching {}".format(chan))		

		
	resp = sc.api_call(
    	"chat.postMessage", channel="#bot_testing", text="boop",
    	 username="lioness", icon_url="https://avatars.slack-edge.com/2016-05-12/42349083605_6f1c7e1101ff3fb069d3_48.png"
	)

	for k,v in resp.items():
		debug(3,"Key: {} Value: {} \n".format(k, v))

	ts = resp.get('ts')

	
	debug(0,"Timestamp: {}".format(ts))

	

	while(_connect):

		if (_connect == 2):
			debug(0, "++++++++++++ REBOOT OUT OF CHEESE +++++")
			disconnect()
			if (connect_to_server()):
				plugins = reload_plugins()

				_connect = 1
			else:
				connect = 0
		

		time.sleep(1)

		for chan in channels['watching']:
			cname = "#"+chanman.getName(chan)
			resp = sc.api_call("channels.history",
				channel=chan, oldest = ts 
				)
			
			for msg in resp['messages']:
				if (float(msg['ts']) > float(ts)):
					debug(0, "Setting timestamp".format(ts))
					ts = msg['ts']
				user = msg.get('user')
				if (re.match('!', msg.get('text'))):
					
					comstring = msg.get('text').split()
					comstring[0] = comstring[0][1:]
					
					debug(2,"Message from {}: {}".format(user, msg))
					debug(2, "Parsed: {}".format( comstring))

					if (plugins.get(comstring[0])):
							try:
								debug(0, " ({})trying {}".format("#"+chan, comstring[0]))
								response = plugins[comstring[0]].command(comstring) 
								debug(0, response)

								chanpost(cname, "{}".format(response.getText()))
							except:
								e = sys.exc_info()[0]
								chanpost(cname, "the {} plugin has a problem! Blame Jai! {}".format(comstring[0], e))

								debug(0, "Could not perform plugin! ")


					elif (user in ops):
						if (comstring[0] == 'die'):
							debug(0, "{} says die!".format(user))
							_connect = 0
						elif (comstring[0] == 'hup'):
							_connect = 2
						elif (comstring[0] == 'debug' ):
							try:
								lev = int(comstring[1])
								DEBUG_LEVEL = lev
								chanpost("#bot_testing", "Setting debug level to {}".format(lev))
							except:
								chanpost("#bot_testing", "Cannot set level {}".format(lev))
					else:
						chanpost(cname, "I have no idea what you are asking me to do.")

			

		


print("Exiting")
