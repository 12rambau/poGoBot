import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import datetime
import re
import os
from Raid import *
from Channel import *

Client = discord.Client()
client = commands.Bot(command_prefix = "?")

cookieCompteur = 0
cRaids = {}
activeChannels = client.get_all_channels()

cAccueil = 0
cRaidList = 0
cDiscussion = 0
cPokemon = 0
cRaidAdd = 0


@client.event
async def on_ready():

    #variable externes
    global activesChannels
    global cAccueil
    global cRaidList
    global cDiscussion
    global cPokemon
    global cRaidAdd

    #on identifie tous les salon sur lesquel peut agir le bot
    regex = re.compile(r"raid-[0-9]")
    for cCurrent in activeChannels:
        if cCurrent.name == "accueil":
            cAccueil = cCurrent
        elif cCurrent.name == "raid-list":
            cRaidList = cCurrent
        elif cCurrent.name == "discussion":
            cDiscussion = cCurrent
        elif cCurrent.name == "pokemon":
            cPokemon = cCurrent
        elif cCurrent.name == "raid-add":
            cRaidAdd = cCurrent
        elif regex.match(cCurrent.name):
            num = int(cCurrent.name[5:])
            cRaids[num]=ChannelRaid(num, cCurrent)

    print("Bot is ready and back online !")

    #lancement des tests unitaires
    #activeChannels = client.get_all_channels()
    #for channel in activeChannels:
    #    if channel.name == "raid-add":
    #        channelCom = channel
    #        break
    #await client.send_message(channelCom, "add T5 14:30 la chatte à la voisine" )

    #for channel in activeChannels:
    #    if channel.name == "raid-1": #normalement le raid est dans raid-1
    #        channelCom = channel
    #        break

    #await client.send_message(channelCom, "bip bip")
    #await client.send_message(channelCom, "in")
    #await client.send_message(channelCom, "in")
    #await client.send_message(channelCom, "out")
    #await client.send_message(channelCom, "out")
    #await client.send_message(channelCom, "launch 15:00")
    #await client.send_message(channelCom, "edit tortank")
    #await client.send_message(channelCom, "launch 15:10")
    #await client.send_message(channelCom, "abort")



# écoute les évènements de GymHuntrBot pour réactualiser en permanence la liste
# des pokémons disponibles pour les raid

    # creer/réécrire le message épingler avec :
    # le pokémon/oeuf
    # les cp, moves
    # le moment de l'éclosion
    # l'heure du Raid
    # l'heure de fin
    # liste des participants

# timer toutes les minutes parcourir les raids
    # si heure de fin dépassée alors on libere le salon

#ajout manuel d'evenement
@client.event
async def on_message(message):

    #variables externes
    global cookieCompteur
    global cRaidAdd
    global cRaids

    args = message.content.split(" ")
    if message.content == "cookie":
        cookieCompteur +=  1
        await client.send_message(message.channel, "%i :cookie:" %(cookieCompteur) )

    if (message.channel == cRaidAdd):
        if message.content.lower().startswith("add") and not len(args) < 4:
            pokeName = args[1]
            battleTime = args[2]
            battlePlace = ' '.join(args[3:])

            #on cherche une conversation de libre
            libre = ChannelRaid.channelLibre(cRaids)
            if not libre:
                await client.send_message(message.channel, "tout est pris mon pote va jouer avec les autres")
                return
            await client.send_message(message.channel, "j'ai trouvé une channel de libre")
            raid = Raid(1,pokeName,message.author.nick, battleTime, battlePlace)
            libre.ajouterRaid(raid)
            await client.send_message(libre.com, embed=raid.embed())

    #écoute des channels de raid
    regex = re.compile(r"raid-[0-9]")
    if regex.match(message.channel.name):
        numRaid = int(message.channel.name[5:])
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if message.content.lower() == "in":
                    if cCurrent.raid.ajouterParticipant(message.author.nick):
                        await client.send_message(cCurrent.com, embed=cCurrent.raid.embed())
            elif message.content.lower() == "out":
                if cCurrent.raid.retirerParticipant(message.author.nick):
                     await client.send_message(cCurrent.com, embed=cCurrent.raid.embed())
            elif message.content.lower() == 'abort':
                if message.author.nick == cCurrent.raid.capitaine:
                    if cCurrent.retirerRaid():
                        await client.send_message(cCurrent.com, "le raid a été abandonné")
            elif args[0] == "launch" and len(args) == 2:
                battleTime = args[1]
                if cCurrent.raid.choisirLaunch(battleTime):
                    await client.send_message(cCurrent.com, embed=cCurrent.raid.embed())
            elif args[0].lower() == "edit" and len(args) == 2:
                pokeName = args[1]
                if cCurrent.raid.faireEclore(pokeName):
                    await client.send_message(cCurrent.com, embed=cCurrent.raid.embed())

client.run(os.environ['DISCORD_TOKEN'])
