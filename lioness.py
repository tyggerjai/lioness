#!/usr/bin/env python3 

import argparse
import time
import os
import sys
from slackclient import SlackClient
import re
import yaml
import logging
from logging.handlers import TimedRotatingFileHandler




def load_configs(cfile):
    """Load the config from the given absolute path file name"""
    try:
        with open(cfile, "r") as conf_file:
            conf = yaml.load(conf_file)
    except :
        e = sys.exc_info()[0]

        print("Could not load: {}".format(e))
        conf = dict()
    return conf



class Lioness():
    """ Lioness is the main class for loading the configs and handling connections

        __init__(self, config, log) takes a dictionary of configs and a logger object

        """
    def __init__(self, config, log):
        """Takes config dict and logger object to initialise """
        self.verbose = 1
        self.log = log
        self.status = "ok"

        try:
            token = config['APIKEY'].strip()
            self.sc = SlackClient(token)
        except:
            self.status = "BAD TOKEN"

        self.dbconn = DataBase(config['dbname'], config['username'], config['passwd'])
        self.log.critical("DBConn {}".format(self.dbconn))

        tables = self.dbconn.show_tables()
        self.log.info( tables)

        self.chanman = ChannelManager()
        self.channels = self.chanman.get_channels()

        self.people = UserManager(self.dbconn, self.sc)
        self.people.set_ops(config['owners'])
        self.people.update_users()
        
        self.commander = Commander(self, config['prefix'], config['enable_plugins'])
        self.botname = config['botname']
        self.icon = config['icon']
        
        self.log.info("Channels to join:")
        self.log.info(self.channels['join'])

        

    def connect_to_server(self):
      self.log.critical("Connecting")  
      if (self.sc.rtm_connect()):
        self.log.critical("Connected")  
        self.ping_owners("Here I am!")
        return 1
      return 0

    def disconnect(self):
        #sc.rtm_disconnect()
        return 1

    def chanpost(self,mychannel, message):
        self.log.debug("Chanpost: {} {}".format(mychannel, message))
        resp = self.sc.api_call(
        "chat.postMessage", channel=mychannel, text=message,
         username=self.botname, icon_url=self.icon)
        self.log.debug( resp)
        return resp


    def ping_owners(self,message):
        for op in self.people.get_owners():
            resp = self.sc.api_call("im.open", user = own['id'])
            own['chat'] = resp['channel']['id']
            self.log.debug( "Pinging owner {}".format(own))
            self.log.debug(sc.api_call("chat.postMessage", as_user="true:", channel=own['chat'], text=message))


    def add_chans(self,chans):
        for chan in chans['channels']:
            self.chanman.set_lookup(chan['id'], chan['name'])        
        
            self.log.debug("{} : {}".format(chan['name'], chan['id']))
            self.channels['known'].append(chan['name'])

            if (chan['name'] in self.channels['join']):

                self.log.debug( "Found watching channel {}".format(chan['name']))
                self.channels['watching'].append(chan['id'])

        for chan in self.channels['watching']:
            self.log.debug("Watching {}".format(chan))           


    def get_timestamp(self,msg):
        if (msg.get('ts')):
            if (float(msg['ts']) > float(self.ts)):
                self.log.error( "Setting timestamp {} ".format(msg['ts']))
            return msg['ts']
        else:
            return self.ts

    



    def setup(self):
        chans = self.sc.api_call("channels.list")
        self.add_chans(chans)
        resp = self.chanpost("#bot_testing", "boop")
        
        for k,v in resp.items():
            self.log.debug("Key: {} Value: {} \n".format(k, v))
        
        self.ts = resp.get('ts')
        self.log.critical("Timestamp: {}".format(self.ts))

        self.log.critical( "Checking API")
        self.sc.api_call("api.test")
        #DEBUG_LEVEL = 0
    def parse_response(self, response, cname):
        
      for msg in response['messages']:
        self.ts = self.get_timestamp(msg)
        user = self.sc.api_call("users.info", user=msg.get('user'))
        self.log.debug( "User object: {}".format(user))
        txt = msg.get('text', '')
        if not "error" in user:
        # probably a bot
            self.people.check_and_add(user)
                        
        if (re.match("^<https?://", txt)):
            txt = '!store ' + txt 

        if (re.match('!', txt)):
            self.log.debug( "COMMAND MESSAGE {}".format(txt))
            txt = txt.split()

            commandargs = CommandArgs()
                        
            commandargs.chan = cname
            commandargs.user = user
            commandargs.command = txt[0][1:]
            commandargs.text = ' '
        
            if (len(txt) > 1):
                commandargs.text = ' '.join(txt[1:])
                    
            return(self.commander.handle(commandargs))


    def listen(self):
        _connect = 1
        while(_connect):
            # HUP received, reload the plugins, disconnect from the server and reconnect
            if (_connect == 2):
                self.log.critical( "++++++++++++ REBOOT OUT OF CHEESE +++++")
                self.disconnect()
                if (self.connect_to_server()):
                    #self.plugins = self.reload_plugins()

                    _connect = 1
                else:
                    _connect = 0
            

            time.sleep(0.5)

            for chan in self.channels['watching']:
                cname = "#"+ self.chanman.get_name(chan)
                resp = self.sc.api_call("channels.history",
                    channel=chan, oldest = self.ts 
                    )
                if "messages" in resp:
                  reply = self.parse_response(resp, cname)
                  if reply and self.verbose:
                    self.chanpost("#bot_testing", reply.getText())


                

            



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prefix')
    parser.add_argument('-c', '--config')
    args = parser.parse_args()
    print( args)
    PREFIX = args.prefix if args.prefix else "./"
    
    conf = args.config if args.config else "{0}/conf/conf.yaml".format(PREFIX)


    try:
        conf = load_configs(conf)
    except:
        e = sys.exc_info()[0]
        print("Can't load config - have you broken it? {}".format(e))

    sys.path.append(PREFIX+"/lib/")
    from database import DataBase
    from channel import ChannelManager
    from users import UserManager
    from commander import Commander, CommandArgs
    
    log = logging.getLogger("Rotating Log")
    log.setLevel(conf['debug_lvl'])
    handler = TimedRotatingFileHandler( conf['prefix']+ "/log/lioness_log", when="d", interval=1, backupCount=7)
    log.addHandler(handler) 

    log.debug("CONFIGS: {}".format(conf))  
    
    lioness = Lioness(conf, log)  
    if (lioness.connect_to_server()):    
        lioness.setup() 
        lioness.listen()




    
