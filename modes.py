from getconfig import get_config_value
import sys
from defer import defer

def hardstop(bot):
    admins = bot.config['misc']['admins'].split('/')
    for user in bot.users:
        if user not in admins:
            bot.voice(user,False)
        bot.users[user]=0
    bot.state=0
    bot.say_main("===========================")
    bot.say_main("Game state completely reset")
    bot.say_main("===========================")

def confirms(bot):
    gamers = [user for user in bot.users if bot.users[user]==1]
    bot.state = 2
    bot.say_main("Game is now in confirmation stage")
    if len(gamers) > 0:
        bot.say_main('Unconfirmed players: {0}'.format(", ".join(gamers)))
        bot.say_main('Unconfirmed players please message me "!confirm"')
    defer(int(bot.config['game']['confirmtimelimit'])-10,confirms_warn,bot)
    defer(int(bot.config['game']['confirmtimelimit']),wrap_start,bot)

def confirms_warn(bot):
    bot.say_main("One minute remains, unconfirmed users:")
    for user in bot.users:
        if bot.users[user] == 1:
            bot.say_main(user)

def wrap_start(bot):
    #Hideous, I know. Deal.
    gamers = [user for user in bot.users if bot.users[user]==2]
    if int(bot.config['gamemodes']['minplayers'])>len(gamers):
        bot.say_main("You have insufficient players.")
        unconf = [user for user in bot.users if bot.users[user]==1]
        if len(unconf) > 0:
            for user in unconf:
                bot.users[user]=0
            bot.say_main(
            "The following players did not confirm, and have been removed:"
                        )
            bot.say_main(", ".join(unconf))
        #If we are only off by 2, go again
        if int(bot.config['gamemodes']['minplayers'])-len(gamers)<=2:
            confirms(bot)
            return
        else:
            bot.say_main("You have far too few players.")
            hardstop(bot)
            return
    elif int(bot.config['gamemodes']['maxplayers'])<len(gamers):
        bot.say_main("You have too many players!")
        #Fix this with new config
        bot.say_main("We can only have {0}".format(
            bot.config['gamemodes']['maxplayers']))
        bot.say_main("Returning to confirmation stage, some people must !leave")
        confirms(bot)
        return
    bot.say_main("starting game with: {0}".format(" ".join(gamers)))
    if str(len(gamers)) not in bot.config['gamemodes']:
        bot.say_main("We don't have a gamemode for that many players. ")
    for user in bot.users:
        if bot.users[user] == 2:
            bot.voice(user,True)

def go_night(bot):
    admins = bot.config['misc']['admins'].split('/')
    for user in bot.users:
        if user not in admins and bot.users[user]>3:
            bot.voice(user,False)           

def go_day(bot):
    admins = bot.config['misc']['admins'].split('/')
    for user in bot.users:
        if user not in admins and bot.users[user]>3:
            bot.voice(user,True)
