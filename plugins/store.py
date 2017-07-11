########
# Base URL storer
######
from plugins.base import PluginResponse, Plugin
import sys
import requests
import html2text

class store(Plugin):
    def __init__(self, dbconn):
        self.keyword = "store"
        self.response = PluginResponse()
        self.error = ""
        self.dbconn = dbconn


    def command(self, args):
        self.response.setText("Nope")
        text = args.text.split()
        user = args.user
        tag = "generic"

        if (len(text) > 1):
            tag = text[-1]
            stored = " ".join(text[:-1])
        else:
            stored = text[0]
        try:
            self.error = self.dbconn.query("""INSERT INTO `store`(`text`, `tag`, `user`) VALUES(%s, %s, %s)""", (stored, tag, user))
            self.response.setText("Added!")
        except:
            self.response.setText("Cannot la: {}".format(self.error))


        return self.response
