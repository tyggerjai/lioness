import sys
import time
from pytz import timezone
import parsedatetime.parsedatetime as pdt
from datetime import datetime, timedelta
from plugins import PluginResponse, Plugin
from builtins import remind


class countdown(Plugin):
    def __init__(self, **kwargs):
        self.keyword = ("countdown",)
        self.response = PluginResponse()
        self.error = ""
        self.level= -1

        self.reminder = remind.remind(**kwargs)

    def command(self, args):
        self.response = self.reminder(args)
        return self.response