from getconfig import get_config_value
from irc.bot import ServerSpec, SingleServerIRCBot
import messages
import sys
from time import sleep

class MafiaBot(SingleServerIRCBot):
    #0 - Disabled 1 - Signup 2 - Confirmation 3 - Ingame
    state = 1
    users = {}
    mchan = "" #Main channel for game
    mserv = "" #Main server  for game

    def __init__(self, server, nick, nickserv, port=6667):
        self.nick = nick
        miscinfo = ServerSpec(server, port, nickserv)
        SingleServerIRCBot.__init__(self, [miscinfo], nick, nick)
    
    def say_main(self, msg, target="chan"):
        print(msg)
        print(target)
        if target == "chan":
            target=self.mchan
        self.mserv.privmsg(target,msg)

    def get_version(self):
        return "Mafiabot - github.com/csssuf/mafiabot"

    def on_pubmsg(self, connection, e):
        print(self.users)
        messages.handler(connection, e, self)
    
    def on_namreply(self, connection,e):
        print(self.channels)
        print(self.channels[self.mchan].users())    
        print(type(self.channels[self.mchan].users()))
        for x in self.channels[self.mchan].users():
            if x != self.nick and x!= "ChanServ":
                self.users[x]=0
    def on_join(self, connection, e):
        if e.source.nick == connection.get_nickname():
            pass
        else:
            print("Welcome, {0}".format(e.source.nick))
            self.users[e.source.nick]=0

    def on_quit(self, connection, e):
        print("Why'd you quit?, {0}".format(e.source.nick))
        self.users.pop(e.source.nick)

    def on_part(self, connection, e):
        print("Gparted, {0}".format(e.source.nick))
        self.users.pop(e.source.nick)

    def on_privmsg(self, connection, e):
        messages.handler(connection, e, self)
        print(self.users)

    def on_welcome(self, connection, e):
        self.mchan=get_config_value('network.channel')
        self.mserv=connection
        connection.join(self.mchan)

    def on_connect(self, connection, e):
        pass
    def on_kick(self, c, e):
        sleep(1)
        c.join(e.target)

if __name__ == '__main__':
    hrc = bool(int(get_config_value('misc.hasreadconfig')))
    if not hrc:
        print('You need to read and modify the config file!')
        sys.exit(0)
    bot = MafiaBot(get_config_value('network.server'), get_config_value('network.nick'), get_config_value('network.nickserv'))
    bot.start()
