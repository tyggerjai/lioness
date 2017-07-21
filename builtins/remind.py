########
# Base URL storer
######
import sys
import time
from pytz import timezone
import parsedatetime.parsedatetime as pdt
from datetime import datetime, timedelta
from plugins import PluginResponse, Plugin

#XXX TODO 
# This works ok, but the message is a bit mangled. What we should do
# is start with the full message, and remove bits until we fail the
# dateparse. Then add bits back one at a time until it passes.
# Whatever we took off is the message.
# We can't start at the start, because we want greedy matching for,
# say, "at 3 pm tomorrow". 

class remind(Plugin):
    def __init__(self, **kwargs):
        self.keyword = ("remind",)
        self.response = PluginResponse()
        self.error = ""
        self.bot = ""
        self.builtin = 1
        self.level = -1
        self.cal = pdt.Calendar()
        self.usage = """ remind [user] [time] <message>. Defaults to
        "me",  "tomorrow"  """


    def command(self, args):
        self.response.setText("Nope")
        text = args.text.split(" ")
        self.bot.log.critical(text[0])
        remindtime = ""
        user = ""
        reminder = ""
        if len(text) < 1: #username, message
            self.response.setText(usage)
            return self.response

        try:
            maybetime = self.cal.parse(args.text, datetime.now(timezone('UTC')))
        except:
            maybetime = self.cal.parse("tomorrow", datetime.now(timezone('UTC')))
            
        remindtime = time.strftime('%Y-%m-%d %H:%M:%S', maybetime[0]) 
       
        user = args.user["user"]["name"]
        if (text[0] == "me"):
            text = text[1:]
        else:
            tryuser = self.bot.people.user_by_name(text[0])

            if (tryuser):
                user = tryuser[0][0]
                self.bot.log.critical(user)
                text = text[1:]
            
        if text[0] == "to":
            text = text[1:]

        self.response.setText("Reminding {} at {} : {}".format(user, remindtime, " ".join(text)))
        
        return self.response
