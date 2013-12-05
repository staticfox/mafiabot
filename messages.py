from getconfig import get_config_value
cmdchar = get_config_value('misc.cmdchar')

def public(c, e, bot):
    if e.arguments[0][:len(cmdchar)] != cmdchar:
        return
    pass

def private(c, e, bot):
    pass
