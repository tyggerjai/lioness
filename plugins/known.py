########
# Base URL storer
######
from plugins import PluginResponse, Plugin
import sys

class store(Plugin):
    def __init__(self, dbconn):
        self.keyword = "known"
        self.response = PluginResponse()
        self.error = ""
        self.dbconn = dbconn


    def command(self, args):
        self.response.setText("Nope")
        
        text = args.text.split(" ")
        #userID = args.user["user"]["id"]

        #if (text[0] == "update"):
            
        
        try:
            self.error = self.dbconn.query("SELECT * FROM `users`", [])
            self.response.setText(self.error)
        except:
            self.response.setText("Cannot la: {}".format(self.error))


        return self.response
