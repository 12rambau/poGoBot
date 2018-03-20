# fichier de lancement du poGoBot
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import os
from PoGoServer import PoGoServer

Client = discord.Client()
bot = commands.Bot(command_prefix = "")

global poGoServer

#routine demarage
@bot.event
async def on_ready():

    global poGoServer

    #recuperer le server
    poGoServer = PoGoServer(bot.get_server(os.environ["DISCORD_SERVER_ID"]))


#ajout manuel d'evenement
@bot.event
async def on_message(message):

    global poGoServer

    # se debarasser des messages privés et des disabled et du bot
    if message.channel.is_private or not PoGoServer.isAble(message.author): return

    #variables internes
    entry = Entry(message, bot)

    #n'import où si on lui parle
    if message.content.lower() == str("<@%s>" %bot.user.id):
        pass
    elif message.content.lower() == "!cookie" :
        await bot.send_message(message.channel, "%i :cookie:" poGoServer.addCookie())
        await bot.delete_message(message)
    elif message.content.lower().startswith("!lvl") and len(args) == 2:
        if await entry.isLevel():
            await addLevel(entry.entry, message.author, bot)
            await bot.delete_message(message)
    elif message.content.lower().startswith("!team") and len(args) == 2:
        pass
    elif message.content.lower().startswith("!nick"):
        pass

    #ecouter les channels de raid Ex
    elif PoGoServer._REGEX_RAID_EX_.match(message.channel.name):
            #numRaid = getNumChannel(message.channel.name)
            #cCurrent = cRaidEx[numRaid]
            if True:#cCurrent.isRaid():
                if args[0].lower() == "!in" and len(args) == 2:
                    pass
                elif args[0].lower() == "!out" and len(args) == 2:
                    pass
                elif message.content.lower() == "!in":
                    pass
                elif message.content.lower() == "!out":
                    pass
                elif message.content.lower() == '!abort':
                    pass
                elif message.content.lower().startswith("!chef"):
                    pass
                elif args[0].lower() == "!edit" and len(args) == 2:
                    pass

    #écoute des channels de raid
    elif PoGoServer._REGEX_RAID_.match(message.channel.name):
        #numRaid = getNumChannel(message.channel.name)
        #cCurrent = cRaids[numRaid]
        if True: #Current.isRaid():
            if args[0].lower() == "!in" and len(args) == 2:
                pass
            elif args[0].lower() == "!out" and len(args) == 2:
                pass
            elif message.content.lower() == "!in":
                pass
            elif message.content.lower() == "!out":
                pass
            elif message.content.lower() == '!abort':
                pass
            elif message.content.lower().startswith("!chef"):
                pass
            elif args[0] == "!launch" and len(args) == 2:
                pass
            elif args[0].lower() == "!edit" and len(args) == 2:
                pass

    #on écoute la channel d'add
    elif message.channel == poGoServer.raid:
        if message.content.lower() == "je vais pas rester":
            pass
        elif message.content.lower().startswith("!add ex") and not len(args) < 5:
            pass
        elif message.content.lower().startswith("!add") and not len(args) < 4:
            pass
        elif message.content.lower() == "!purge":
            pass
        elif isNotBot(message) : await client.delete_message(message)

    elif message.channel == poGoServer.accueil:
        if message.content.lower().startswith("!free") and len(args) == 2:
            pass

    elif message.channel.name == "gymhuntr": #and #not message.content:
        pass

#ajout d'emoji
@bot.event
async def on_reaction_add(reaction, user):
    if True:#regex.match(reaction.message.channel.name):
        pass

#retrait d'emoji
@bot.event
async def on_reaction_remove(reaction, user):
    if True:#regex.match(reaction.message.channel.name):
        pass

@bot.event
async def on_member_update(before, after):
    pass

@bot.event
async def on_member_join(member):
    pass


bot.run(os.environ['DISCORD_TOKEN'])
