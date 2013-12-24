from getconfig import get_config_value
import sys
import modes

def handler(c, e, bot):
    cmdchar = bot.config['misc']['cmdchar']
    admins = bot.config['misc']['admins'].split('/')
    nick = bot.config['network']['nick']

    if e.arguments[0][:len(cmdchar)] != cmdchar:
        return
    if e.source.nick == nick:
        return
    cmd = e.arguments[0][len(cmdchar):]
    args = cmd.split(' ')[1:]
    cmd = cmd.split(' ')[0]
    if e.source.nick in admins:
        if cmd == 'voicelist':
            print(bot.channels[bot.mchan].voiceddict)

        if cmd == 'voiceall':
            for user in bot.users:
                bot.voice(user,True)

        if cmd == 'reset':
            modes.hardstop(bot)

        if cmd == 'talk':
            bot.say_main(" ".join(args))

        if cmd == 'quit': 
            c.disconnect('Quitted from IRC by %s' % e.source)
            sys.exit(0)

        elif cmd == 'disable':
            if not bot.state == 0:
                c.privmsg(e.target, "Disabling.")
            bot.state = 0

        elif cmd == 'enable' and bot.state == 0:
            bot.state = 1
            c.privmsg(e.target, "Enabling.")

        if bot.state == 1:
            if cmd == 'start':
                gamers = []
                for key in bot.users:
                    if bot.users[key]==1:
                        gamers.append(key)
                print('Starting with {0}'.format(gamers))
                modes.confirms(bot)

    if bot.state == 1:
        if cmd == 'join' and bot.users[e.source.nick] in [0,-1,-3]:
            bot.users[e.source.nick]=1
        if cmd == 'leave' and bot.users[e.source.nick] in [1,2]:
            bot.users[e.source.nick]=0

    elif bot.state == 2:
        if cmd == 'join' and bot.users[e.source.nick] in [0,-1,-3]:
            bot.users[e.source.nick]=2
        if cmd == 'confirm' and bot.users[e.source.nick]==1:
            bot.users[e.source.nick]=2
        if cmd == 'leave' and bot.users[e.source.nick] in [1,2]:
            bot.users[e.source.nick]=0

    elif bot.state == 5:
        if 200<bot.users[e.source.nick]<251:
            for user in bot.users:
                if 200<bot.users[user]<251 and user!=e.source.nick:
                    bot.say_main("{0}: {1}".format(e.source.nick,
                                                cmd+"".join(args)))
