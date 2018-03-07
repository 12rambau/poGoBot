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
from data import *

Client = discord.Client()
client = commands.Bot(command_prefix = "?")

cookieCompteur = 0
cRaids = {}
activeChannels = 0
server = 0

cAccueil = 0
cRaidList = 0
cDiscussion = 0
cPokemon = 0
cRaidAdd = 0

def is_bot(m):
    global msgRaid
    return m.author.name != "PoGoBot"

async def addToListe(cRaid):
    """ajoute un raid à la liste des raids"""

    #variables externes
    global cRaidAdd

    await client.purge_from(cRaidAdd, check=is_bot)
    content = str("raid en cour sur <#%s>" %(cRaid.com.id))
    msg = await client.send_message(cRaidAdd, content=content, embed=cRaid.raid.embed())
    cRaid.listMsg = msg

async def editListe(cRaid):
    """editer le message corresponant au raid selectionné"""
    msg = str("raid en cour sur <#%s>" %(cRaid.com.id))
    await client.edit_message(cRaid.listMsg, new_content=msg, embed=cRaid.raid.embed())

async def removeFromListe(cRaid):
    """retirer un raid périmé ou abandonné"""

    #variable globales
    global cRaidAdd

    await client.delete_message(cRaid.listMsg)




    return 0

@client.event
async def on_ready():
    #variable externes
    global activesChannels
    global cAccueil
    global cRaidList
    global cDiscussion
    global cPokemon
    global cRaidAdd
    global server
    global msgRaid

    #recuperer le server
    server = client.get_server(os.environ["DISCORD_SERVER_ID"])

    #on identifie tous les salon sur lesquel peut agir le bot
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    cIds = []
    for cCurrent in client.get_all_channels():
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
            await client.purge_from(cRaidAdd)
        elif regex.match(cCurrent.name):
            cIds.append(cCurrent.id)

        for cId in cIds:
            await client.delete_channel(client.get_channel(cId))
    activeChannels = client.get_all_channels()

    #ecrire le message initiale des raid
    msgRaid = await client.send_message(cRaidAdd, "liste des raides en cours")

    print("Bot is ready and back online !")

# timer toutes les minutes parcourir les raids
    # si heure de fin dépassée alors on libere le salon

#ajout manuel d'evenement
@client.event
async def on_message(message):

    #variables externes
    global cookieCompteur
    global cRaidAdd
    global cRaids
    global cRaidList

    args = message.content.split(" ")
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if message.content == "cookie":
        cookieCompteur +=  1
        await client.send_message(message.channel, "%i :cookie:" %(cookieCompteur) )
        await client.delete_message(message)

    elif (message.channel == cRaidAdd):
        if message.content.lower().startswith("add") and not len(args) < 4:
            pokeName = args[1]
            battleTime = args[2]
            battlePlace = ' '.join(args[3:])

            cCom = await client.create_channel(server, str("%i_%s-0" %(ChannelRaid.nb_channel+1,pokeName)))
            cRaids[ChannelRaid.nb_channel] = ChannelRaid(cCom)

            raid = Raid(0,pokeName,message.author.nick, battleTime, battlePlace)
            cRaid = cRaids[ChannelRaid.nb_channel].ajouterRaid(raid)

            await addToListe(cRaid)
            msg = await client.send_message(cCom, embed=raid.embed())
            await client.pin_message(msg)
            cRaid.pinMsg = msg

    #écoute des channels de raid
    elif regex.match(message.channel.name):
        numRaid = int(message.channel.name[0])
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if message.content.lower() == "in":
                    if cCurrent.raid.ajouterParticipant(message.author.nick):
                        await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                        await client.edit_channel(cCurrent.com, name=re.sub(r"-[0-9]*", str("-%i" %(len(cCurrent.raid.participants))), cCurrent.com.name))
                        await editListe(cCurrent)
                        await client.delete_message(message)
            elif message.content.lower() == "out":
                if cCurrent.raid.retirerParticipant(message.author.nick):
                     await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                     await client.edit_channel(cCurrent.com, name=re.sub(r"-[0-9]*", str("-%i" %(len(cCurrent.raid.participants))), cCurrent.com.name))
                     await editListe(cCurrent)
                     await client.delete_message(message)
            elif message.content.lower() == 'abort':
                if message.author.nick == cCurrent.raid.capitaine:
                    if cCurrent.retirerRaid():
                        cId = cCurrent.com.id
                        await removeFromListe(cCurrent)
                        await client.delete_channel(client.get_channel(cId))
                        cCurrent = 0
            elif args[0] == "launch" and len(args) == 2:
                battleTime = args[1]
                if cCurrent.raid.choisirLaunch(battleTime):
                    await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                    await editListe(cCurrent)
                    await client.delete_message(message)
            elif args[0].lower() == "edit" and len(args) == 2:
                pokeName = args[1]
                if cCurrent.raid.faireEclore(pokeName):
                    await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                    await client.edit_channel(cCurrent.com, name=re.sub(r"_[a-z0-9]*-", str("_%s-" %(pokedex[cCurrent.raid.pokeId-1]["fr"])), cCurrent.com.name))
                    await editListe(cCurrent)
                    await client.delete_message(message)

client.run(os.environ['DISCORD_TOKEN'])
