from getconfig import get_config_value
import sys

cmdchar = get_config_value('misc.cmdchar')
admins = get_config_value('misc.admins').split('/')
def public(c, e, bot):
    if e.arguments[0][:len(cmdchar)] != cmdchar:
        return
    print('proceeding with command %s.' % e.arguments[0][len(cmdchar):])
    cmd = e.arguments[0][len(cmdchar):]
    args = cmd.split(' ')[1:]
    cmd = cmd.split(' ')[0]
    if cmd == 'quit' and e.source.nick in admins:
        c.disconnect('Quitted from IRC by %s' % e.source)
        sys.exit(0)
    pass

def private(c, e, bot):
    pass
