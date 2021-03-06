
import requests
import re

import time
from datetime import datetime
import pytz
from tzlocal import get_localzone

from hashlib import sha1

from bs4 import BeautifulSoup

defaultHeaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "user-agent": 'curl/7.68.0',
}

class FeedException:
    pass

class RSSFeed:
    def __init__(self, url):
        self.url = url
        self.seenHashes = {}
        self.feedTitle = ""
        self.CacheFeed()
        print("Cached current feed from: {}".format(self.feedTitle))

    def CacheFeed(self):
        try:
            r = requests.get(self.url, headers=defaultHeaders)
            if r.status_code != 200:
                raise FeedException
            soup = BeautifulSoup(r.content, features='xml')
            articles = soup.findAll('item')
            self.feedTitle = soup.find('channel').find("title").text
            for a in articles:
                title = a.find('title').text
                link = a.find('link').text
                published = a.find('pubDate').text
                itemHash = sha1( (title + link + published).encode() ).hexdigest()
                self.seenHashes[itemHash] = True

        except Exception as e:
            print("Failed to process feed ({}) with error: {}".format(self.url, e ))
            print("Headers:\n{}\nContent:\n{}".format(r.headers, r.content ))

    def NewData(self):
        newItems = []
        try:
            r = requests.get(self.url, headers=defaultHeaders)
            if r.status_code != 200:
                raise FeedException
            soup = BeautifulSoup(r.content, features='xml')
            articles = soup.findAll('item')
            for a in articles:
                title = a.find('title').text
                link = a.find('link').text
                published = a.find('pubDate').text

                itemHash = sha1( (title + link + published).encode() ).hexdigest()

                if itemHash not in self.seenHashes.keys():
                    self.seenHashes[itemHash] = True
                    newItems.append({
                        "channel": self.feedTitle,
                        "title": title,
                        "link": link,
                        "published": published,
                    })
        except Exception as e:
            print("Failed to refresh feed ({}) with error: {}".format(self.url, e))
        return newItems

