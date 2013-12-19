from getconfig import get_config_value
import sys
from defer import defer

def confirms(bot):
    bot.state = 2
    defer(int(get_config_value('game.confirmtimelimit'))-10,confirms_warn,bot)
    defer(int(get_config_value('game.confirmtimelimit')),wrap_start,bot)

def confirms_warn(bot):
    bot.say_main("One minute remains, unconfirmed users:")
    for user in bot.users:
        if bot.users[user] == 1:
            bot.say_main(user)

def wrap_start(bot):
    bot.say_main("starting game with:")
    for user in bot.users:
        if bot.users[user] == 2:
            bot.say_main(user)
