from getconfig import get_config_value
import sys
from defer import defer

def hardstop(bot):
    admins = get_config_value('misc.admins').split('/')
    for user in bot.users:
        if user not in admins:
            bot.voice(user,False)
        bot.users[user]=0
    bot.state=0
    bot.say_main("===========================")
    bot.say_main("Game state completely reset")
    bot.say_main("===========================")

def confirms(bot):
    gamers = []
    for key in bot.users:
        if bot.users[key]==1:
            gamers.append(key)
    bot.state = 2
    bot.say_main("Game is now in confirmation stage")
    bot.say_main('Joined players: {0}'.format(",".join(gamers)))
    bot.say_main('Joined players please message me "!confirm"')
    defer(int(get_config_value('game.confirmtimelimit'))-10,confirms_warn,bot)
    defer(int(get_config_value('game.confirmtimelimit')),wrap_start,bot)

def confirms_warn(bot):
    bot.say_main("One minute remains, unconfirmed users:")
    for user in bot.users:
        if bot.users[user] == 1:
            bot.say_main(user)

def wrap_start(bot):
    bot.say_main("starting game with: {0}".format(" ".join([user for user in
                                    bot.users if bot.users[user]==2])))
    for user in bot.users:
        if bot.users[user] == 2:
            bot.voice(user,True)

def go_night(bot):
    admins = get_config_value('misc.admins').split('/')
    for user in bot.users:
        if user not in admins and bot.users[user]>3:
            bot.voice(user,False)           

def go_day(bot):
    admins = get_config_value('misc.admins').split('/')
    for user in bot.users:
        if user not in admins and bot.users[user]>3:
            bot.voice(user,True)
