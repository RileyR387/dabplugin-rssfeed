
import os
import time
import asyncio

from jinja2 import Environment, BaseLoader

from .rssfeed import RSSFeed

messageTemplateStr = '''{{ channel }} - {{ title }}
{{ link }}'''

messageTemplate = Environment(loader=BaseLoader).from_string(messageTemplateStr)

class BotPlugin:
    def __init__(self, msgCallback):
        self.name = "rssplugin"
        self.SendMessage = msgCallback
        self._initEnv()
        self.lastRefresh = time.time()
        self.isRunning = True

    # Custom message interpriters for the plugin
    async def ProcessMessage(self, message):
        None

    # Parent is stopping, maintenance op for clean exit
    def Stop(self):
        self.isRunning = False
        print("Stopping plugin...")

    # Run asyncio tasks here within the discord event loop,
    # using `self.SendMessage` on demand for the default
    # or configured channel ID's
    async def Run(self):
        while self.isRunning:
            if self._shouldRefresh():
                self._refreshFeeds()
            await asyncio.sleep(1)

    # The alert bot service can be configured to run this based on primary services config
    def Job(self):
        #self.SendMessage("Test message from external plugin job")
        None

    def _initEnv(self):
        self.channels = []
        self.feeds = []

        self.refresh_interval = int(os.getenv('RSSFEED_REFRESH_INTERVAL_SECONDS', default='60'))

        for channel in os.getenv('RSSFEED_CHANNEL_IDS').split(','):
            self.channels.append(int(channel.strip()))
        for feedUrl in os.getenv('RSSFEED_FEED_URIS').split(' '):
            self.feeds.append( RSSFeed(feedUrl) )

    def _shouldRefresh(self):
        if time.time() - self.lastRefresh >= self.refresh_interval:
            return True

    def _refreshFeeds(self):
        print("{} Refreshing Feeds".format(time.time()))
        self.lastRefresh = time.time()
        for feed in self.feeds:
            newData = feed.NewData()
            if newData is not None:
                for item in newData:
                    self._PublishItem( item )

    def _PublishItem(self, item):
        #self.SendMessage( messageTemplate.render( **item ) )
        self.SendMessage({
            'type': 'rich',
            'title': item['title'],
            'url': item['link'],
            'author': item['channel'],
            'description': item['channel']
        })

