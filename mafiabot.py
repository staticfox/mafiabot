from irc.bot import ServerSpec, SingleServerIRCBot
import messages
import sys
import configparser
from time import sleep

class MafiaBot(SingleServerIRCBot):
    #0 - Disabled 1 - Signup 2 - Confirmation 3 - Ingame
    state = 1
    users = {}
    mchan = "" #Main channel for game
    mserv = "" #Main server  for game

    #def __init__(self, server, nick, nickserv, port=6667):
    def __init__(self, config, port=6667):
        self.config = config
        self.nick = config['network']['nick']
        self.userpass=config['network']['nickserv']
        miscinfo = ServerSpec(config['network']['server'], 
                              port, 
                              config['network']['nickserv'])
        SingleServerIRCBot.__init__(self, [miscinfo], self.nick, self.nick)
    
    def say_main(self, msg, target="chan"):
        print(msg)
        print(target)
        if target == "chan":
            target=self.mchan
        self.mserv.privmsg(target,msg)

    def voice(self,user,on):
        if on:
            toggle="+"
        else:
            toggle="-"
        self.mserv.mode(self.mchan,"{0}v {1}".format(toggle,user))

    def get_version(self):
        return "Mafiabot - github.com/csssuf/mafiabot"

    def on_pubmsg(self, connection, e):
        print(self.users)
        messages.handler(connection, e, self)
    
    def on_namreply(self, connection,e):
        print(self.channels)
        print(self.channels[self.mchan].users())    
        print(type(self.channels[self.mchan].users()))
        print(self.channels[self.mchan].modes)
        print(self.channels[self.mchan].voiceddict)
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
        self.mchan="#" + config['network']['channel']
        self.mserv=connection
        connection.join(self.mchan)

    def on_connect(self, connection, e):
        self.say_main("IDENTIFY {0} {1}".format(self.nick,self.userpass),
                    "NickServ")
    def on_kick(self, c, e):
        sleep(1)
        c.join(e.target)

if __name__ == '__main__':
    config = configparser.RawConfigParser()
    config.read('config.cfg')
    hrc = config.getboolean('misc','hasreadconfig')
    if not hrc:
        print('You need to read and modify the config file!')
        sys.exit(0)
    #My crystal ball says this might come up, good to watch
    #users' backs, especially if users are us
    minplay=config['gamemodes']['minplayers']
    maxplay=config['gamemodes']['maxplayers']
    if minplay>maxplay:
        print('Your gamemodes are screwed up')
        sys.exit(0)
    print(config['gamemodes']['minplayers'])
    print(config['time']['jointimelimit'])
    print(config['gamemodes']['maxplayers'])
    bot = MafiaBot(config)
    bot.start()
