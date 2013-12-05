from getconfig import get_config_value
import sys

cmdchar = get_config_value('misc.cmdchar')
admins = get_config_value('misc.admins').split('/')
nick = get_config_value('network.nick')
def handler(c, e, bot):
    if e.arguments[0][:len(cmdchar)] != cmdchar:
        return
    cmd = e.arguments[0][len(cmdchar):]
    args = cmd.split(' ')[1:]
    cmd = cmd.split(' ')[0]
    if e.source.nick in admins:
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

