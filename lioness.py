import time
from slackclient import SlackClient
import re


DEBUG_LEVEL = 3

mytoken = ""
with open("API.key") as api:
	mytoken = api.readline().strip()
	api.close()


sc = SlackClient(mytoken)

_connect = 1

owners = {'tyggerjai':
		 	{
		 	'id': 'U189HEXD5', 
			}

		}
channels = { "join": ("bot_testing"),
			"known": list(),
			"watching": list()
	}
print("Channels to join:")
print(channels['join'])

ops = [owners[own]['id'] for own in owners.keys()]

def debug(level, message):
	if (level < DEBUG_LEVEL):
		print(message)

def connect_to_server():
	
	if (sc.rtm_connect()):
		ping_owners("Here I am!")
		return 1
	return 0

def disconnect():
	return 1
	#sc.rtm_disconnect()

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




print("Starting ... \n")
print("My owners are: ")

for own in owners.keys():
	print(own)

if (connect_to_server()):
	debug(1, "Checking API")
	debug (1, sc.api_call("api.test"))
	

	


	chans = sc.api_call("channels.list")
		
	for chan in chans['channels']:
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
		debug(3,print("Key: {} Value: {} \n".format(k, v)))

	ts = resp.get('ts')

	
	debug(0,"Timestamp: {}".format(ts))

	

	while(_connect):

		if (_connect == 2):
			disconnect()
			if (connect_to_server()):
				_connect = 1
			else:
				connect = 0
		

		time.sleep(1)

		for chan in channels['watching']:
			resp = sc.api_call("channels.history",
				channel=chan, oldest = ts 
				)
			
			for msg in resp['messages']:
				if (float(msg['ts']) > float(ts)):
					debug(0, "Setting timestamp".format(ts))
					ts = msg['ts']
				user = msg.get('user')
				if (re.match('!', msg.get('text'))):

					print("Message from {}".format(user))
					print(msg)
					if (user in ops):
						if (re.match("!", msg['text'])):
							if (msg['text'] == '!die'):
								print("{} says die!".format(user))
								_connect = 0
							elif (msg['text'] == '!hup'):
								_connect = 2
							elif (re.match( "!debug", msg['text']) ):
								try:
									lev = int(msg['text'].split()[1])
									DEBUG_LEVEL = lev
									chanpost("#bot_testing", "Setting debug level to {}".format(lev))
								except:
									chanpost("#bot_testing", "Cannot set level {}".format(lev))



		


			

		


print("Exiting")
