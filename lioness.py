import time
import sys
from slackclient import SlackClient
import re
from database import DataBase
from channel import ChannelManager
from users import UserManager
from commander import Commander, CommandArgs
import yaml
import logger

DEBUG_LEVEL = 1
LOGFILE = "lioness_log.txt"
log = Logger(DEBUG_LEVEL, LOGFILE)

def load_configs():
	try:
		with  open("conf.yaml", "r") as conf_file:
			conf = yaml.load(conf_file)
	except :
		e = sys.exc_info()[0]

		print("Could not load: {}".format(e))
		conf = dict()
	return conf


mytoken = ""
with open("API.key") as api:
	mytoken = api.readline().strip()
	api.close()



log.debug(0, "+++++++++++++++++++++++++++++\n++STARTING\n")

sc = SlackClient(mytoken)

_connect = 1
config = load_configs()
log.debug(0,config)
dbconn = DataBase(config['dbname'], config['username'], config['passwd'])

log.debug(0, "DBConn {}".format(dbconn))
tables = dbconn.show_tables()
log.debug(0, tables)

chanman = ChannelManager()
channels = chanman.get_channels()

people = UserManager()
owners = people.get_owners()

commander = Commander(dbconn, log)
commandargs = CommandArgs()

log.debug(1,"Channels to join:")
log.debug(1,channels['join'])

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
		log.debug(1, "Pinging owner {}".format(own))
		log.debug(1,sc.api_call("chat.postMessage", as_user="true:", channel=own['chat'], text=message))


def add_chans(chans):
	for chan in chans['channels']:
		chanman.set_lookup(chan['id'], chan['name'])		
	
		log.debug(3,"{} : {}".format(chan['name'], chan['id']))
		channels['known'].append(chan['name'])

		if (chan['name'] in channels['join']):

			log.debug(2, "Found watching channel {}".format(chan['name']))
			channels['watching'].append(chan['id'])

	for chan in channels['watching']:
		log.debug(3,"Watching {}".format(chan))			


def get_timestamp(msg):
	if (float(msg['ts']) > float(ts)):
		log.debug(0, "Setting timestamp".format(ts))
		return msg['ts']

def reload_plugins():
	plugin.init_plugins()
	return 	plugin.get_plugins()


# Start and connect
log.debug(1,"Starting ... \n")
log.debug(1,"My owners are: ")

for own in owners.keys():
	log.debug(1, own)

if (connect_to_server()):


	log.debug(1, "Checking API")
	log.debug (1, sc.api_call("api.test"))
	#DEBUG_LEVEL = 0


	


	chans = sc.api_call("channels.list")
	add_chans(chans)
		
	resp = sc.api_call(
    	"chat.postMessage", channel="#bot_testing", text="boop",
    	 username="lioness", icon_url="https://avatars.slack-edge.com/2016-05-12/42349083605_6f1c7e1101ff3fb069d3_48.png"
	)

	for k,v in resp.items():
		log.debug(3,"Key: {} Value: {} \n".format(k, v))

	ts = resp.get('ts')

	
	log.debug(0,"Timestamp: {}".format(ts))

	

	while(_connect):
		# HUP received, reload the plugins, disconnect from the server and reconnect
		if (_connect == 2):
			log.debug(0, "++++++++++++ REBOOT OUT OF CHEESE +++++")
			disconnect()
			if (connect_to_server()):
				plugins = reload_plugins()

				_connect = 1
			else:
				_connect = 0
		

		time.sleep(0.5)

		for chan in channels['watching']:
			cname = "#"+chanman.get_name(chan)
			resp = sc.api_call("channels.history",
				channel=chan, oldest = ts 
				)
			
			for msg in resp['messages']:
				ts = get_timestamp(msg)
				user = msg.get('user')
				txt = msg.get('text', '')
				if (re.match('!', txt):
					
					commandargs.user = user
					commandargs.text = [1:]
					commandargs.command = txt[0][1:]
					reply = commander.handle(commandargs)

					chanpost(reply.cname, reply.text)
					
					

			

		


print("Exiting")
