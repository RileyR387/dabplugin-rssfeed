#!/usr/bin/env python3

'''
    Wrapper script for plugin development/testing.
'''

import sys
import signal
import time
import asyncio

from dabplugin import rssplugin

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

'''
  DevPlugin mimics the asyncio event loop leveraged in `discord.py`
'''
class DevPlugin:
    def __init__(self):
        self.plugin = rssplugin.BotPlugin(self.MsgCallback)

    async def main(self):
        self.loop = asyncio.get_running_loop()

        self.loop.create_task(
            self.plugin.Run()
        )

        self.fut = self.loop.create_future()
        await self.fut

    def stop(self, signum, frame):
        if self.fut is not None:
            self.fut.set_result("Done")
        self.plugin.Stop()
        self.loop.stop()
        raise ServiceExit

    # Mimic functionality of `discord-alert-bot` call back provided to plugins
    def MsgCallback(self, msgOps):
        if isinstance(msgOps, str):
            #self.QueueMessage( self._defaultChannelId(), msgOps )
            print("ChannelId: {}\n{}".format("default channel", msgOps))
        elif isinstance(msgOps, dict):
            msgKeys = msgOps.keys()
            if 'msg' not in msgKeys:
                print("Message dictionary should be of form: {msg:\"message text\", channelid: \"fdafdsfdsa\"}")
                return

            if 'BROADCAST' in msgKeys and msgOps['BROADCAST']:
                #self._pluginBroadcast(msgOps['msg'])
                print("ChannelId: {}\n{}".format("broadcast", msgOps['msg']))

            if 'channelid' in msgKeys:
                #self.QueueMessage( msgOps['channelid'], msgOps['msg'] )
                print("ChannelId: {}\n{}".format(msgOps['channelid'], msgOps['msg']))

            if 'channelids' in msgKeys:
                for chanID in msgOps['channelids']:
                    #self.QueueMessage( chanID, msgOps['msg'] )
                    print("ChannelId: {}\n{}".format(chanID, msgOps['msg']))
        else:
            print("Error, invalide message options provided")


devPlugin = DevPlugin()

signal.signal(signal.SIGTERM, devPlugin.stop)
signal.signal(signal.SIGINT, devPlugin.stop)

try:
    asyncio.run(devPlugin.main())
except ServiceExit:
    exit(0)
except Exception as e:
    print("Event loop terminated with error: {}".format(e))


