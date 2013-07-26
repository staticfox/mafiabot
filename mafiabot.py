from getconfig import get_config_value
from irc.bot import ServerSpec, SingleServerIRCBot


class MafiaBot(SingleServerIRCBot):

    def __init__(self, server, nick, nickserv, port=6667):
        miscinfo = ServerSpec(server, port, nickserv)
        SingleServerIRCBot.__init__(self, [miscinfo], nick, nick)
    
    def get_version(self):
        return "Mafiabot - github.com/csssuf/mafiabot"

    def on_pubmsg(self, connection, e):
        pass

    def on_welcome(self, connection, e):
        connection.join(get_config_value('network.channel'))

if __name__ == '__main__':
    bot = MafiaBot(get_config_value('network.server'), get_config_value('network.nick'), get_config_value('network.nickserv'))
    bot.start()
