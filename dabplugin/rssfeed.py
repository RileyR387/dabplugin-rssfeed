
import os
import requests
import re

import time
from datetime import datetime
import pytz
from tzlocal import get_localzone

from bs4 import BeautifulSoup
from jinja2 import Environment, BaseLoader


class BotPlugin:
    def __init__(self, msgCallback):
        self.name = "rssplugin"
        self.SendMessage = msgCallback
        self._initEnv()
        self._refreshFeeds()

    # Parent is stopping, maintenance op for clean exit
    def Stop(self):
        print("Stopping plugin...")
        None

    # Run custom threads/refreshes here, using `self.SendMessage`
    # on demand for the default or configured channel ID's
    def Run(self):
        print("Running plugin!")
        None

    # The alert bot service can be configured to run this based on primary services config
    def Job(self):
        print("Running plugin job!")
        None

    # Custom message interpriters for the plugin
    async def ProcessMessage(self, message):
        None

    def _initEnv(self):
        self.channels = []
        self.feeds = []
        for channel in os.getenv('RSSFEED_CHANNEL_IDS').split(','):
            self.channels.append(int(channel.strip()))
        for feed in os.getenv('RSSFEED_FEED_URIS').split(' '):
            self.feeds.append(feed)

    def _refreshFeeds(self):
        None

