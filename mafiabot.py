from getconfig import get_config_value
from irc.bot import ServerSpec, SingleServerIRCBot
import messages
import sys

class MafiaBot(SingleServerIRCBot):
    #0 - Disabled 1 - Signup 2 - Confirmation 3 - Ingame
    state = 1
    players = {}

    def __init__(self, server, nick, nickserv, port=6667):
        miscinfo = ServerSpec(server, port, nickserv)
        SingleServerIRCBot.__init__(self, [miscinfo], nick, nick)
    
    def get_version(self):
        return "Mafiabot - github.com/csssuf/mafiabot"

    def on_pubmsg(self, connection, e):
        print(e.source.__dict__)
        print(type(e.source))
        print(dir(self))
        for key in self.channels:
            print(self.channels[key].users())
            print(self.channels[key].voiced())
        messages.public(connection, e, self)

    def on_privmsg(self, connection, e):
        messages.private(connection, e, self)

    def on_welcome(self, connection, e):
        connection.join(get_config_value('network.channel'))
        print(self.channels)
        for key in self.channels:
            print(self.channels[key].users())
            print(self.channels[key].voiced())
if __name__ == '__main__':
    hrc = bool(int(get_config_value('misc.hasreadconfig')))
    if not hrc:
        print('You need to read and modify the config file!')
        sys.exit(0)
    bot = MafiaBot(get_config_value('network.server'), get_config_value('network.nick'), get_config_value('network.nickserv'))
    bot.start()
