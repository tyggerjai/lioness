import time
from slackclient import SlackClient
import re


DEBUG_LEVEL = 2

mytoken = ""
sc = SlackClient(mytoken)

_connect = 1

owners = {'tyggerjai':
		 {
		 'id': 'U189HEXD5', 
		}

		}


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
	sc.rtm_disconnect()


def ping_owners(message):
	for owner in owners.keys():
		own = owners[owner]
		resp = sc.api_call("im.open", user = own['id'])
		own['chat'] = resp['channel']['id']

		print(sc.api_call("chat.postMessage", as_user="true:", channel=own['chat'], text=message))





print("Starting ... \n")
print("My owners are: ")
for own in owners.keys():
	print(own)

if (connect_to_server):
	
	debug (1, sc.api_call("api.test"))
	

	print("sending")
	resp = sc.api_call(
    	"chat.postMessage", channel="#bot_testing", text="boop",
    	 username="lioness", icon_url="https://avatars.slack-edge.com/2016-05-12/42349083605_6f1c7e1101ff3fb069d3_48.png"
	)

	for k,v in resp.items():
		debug(3,print("Key: {} Value: {} \n".format(k, v)))

	ts = resp.get('ts')

	
	debug(0,"Timestamp: {}".format(ts))

	chans = sc.api_call("channels.list")
	for chan in chans['channels']:
		print("{} : {}".format(chan['name'], chan['id']))


	while(_connect):

		if (_connect == 2):
			disconnect()
			if (connect_to_server()):
				_connect = 1
			else:
				connect = 0
		

		time.sleep(1)

		resp = sc.api_call("channels.history",
			channel="C1895HN20", oldest = ts 
			)
		
		for msg in resp['messages']:
			if (float(msg['ts']) > float(ts)):
				debug(1, "Setting timestamp".format(ts))
				ts = msg['ts']
			user = msg.get('user')
			if (re.match('!', msg.get('text'))):

				print("Message from {}".format(user))
				print(msg)
				if (user in ops):
					if (msg['text'] == '!die'):
						print("{} says die!".format(user))
						_connect = 0
					elif (msg['text'] == '!hup'):
						_connect = 2
		


			

		


print("Exiting")
