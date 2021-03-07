#!/usr/bin/env python3

from dabplugin import rssfeed

def MsgCallback(msgOps):
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


plugin = rssfeed.BotPlugin(MsgCallback)

plugin.Run()

plugin.Stop()

