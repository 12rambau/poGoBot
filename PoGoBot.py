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

# timer toutes les minutes parcourir les raids
    # si heure de fin dépassée alors on libere le salon
async def waitTimer():
    while True:
        await asyncio.sleep(10)

        regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid

        for cCurrent in client.get_all_channels():
            if regex.match(cCurrent.name):
                numRaid = int(cCurrent.name[0])
                cRaidCurrent = cRaids[numRaid]
                date = datetime.datetime.now()
                print ("raid: %s" %(cRaidCurrent.raid.fin.timestamp()))
                print ("date: %s" %(date.timestamp()))
                await asyncio.sleep(30)
                if cRaidCurrent.raid.fin < date:
                    if cRaidCurrent.retirerRaid():
                        cId = cRaidCurrent.com.id
                        await removeFromListe(cRaidCurrent)
                        await client.delete_channel(client.get_channel(cId))
                        cCurrent = 0


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

    #on lance le garbage collector
    await waitTimer()

    print("Bot is ready and back online !")

#ajout manuel d'evenement
@client.event
async def on_message(message):

    #variables externes
    global cookieCompteur
    global cRaidAdd
    global cRaids
    global cRaidList
    global cAccueil
    global server
    args = message.content.split(" ")
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if message.content == "cookie":
        cookieCompteur +=  1
        await client.send_message(message.channel, "%i :cookie:" %(cookieCompteur) )
        await client.delete_message(message)

    elif message.channel == cRaidAdd:
        if message.content.lower().startswith("add") and not len(args) < 4:
            pokeName = args[1]
            battleTime = args[2]
            battlePlace = ' '.join(args[3:])

            cCom = await client.create_channel(server, str("%i_%s-0" %(ChannelRaid.nb_channel+1,pokeName)))
            cRaids[ChannelRaid.nb_channel] = ChannelRaid(cCom)

            raid = Raid(0,pokeName,message.author, battleTime, battlePlace)
            cRaid = cRaids[ChannelRaid.nb_channel].ajouterRaid(raid)

            await addToListe(cRaid)
            msg = await client.send_message(cCom, embed=raid.embed())
            await client.pin_message(msg)
            cRaid.pinMsg = msg

    #on écoute la channel d'accueil
    elif message.channel == cAccueil:
        if message.content.startswith("lvl") and len(args) == 2:
            lvl = args[1]
            regex = re.compile(r"^.* \([0-9]*\)$")
            print(message.author.nick)
            if regex.match(message.author.nick):
                newNick = re.sub(r"\([0-9]*\)$", str("(%s)" %(lvl)), message.author.nick)
            else:
                newNick = message.author.nick
                newNick += str(" (%s)" %(lvl))
            print(newNick)
            await client.change_nickname(message.author, newNick)

        if message.content.startswith("team") and len(args) == 2:
            team = args[1]
            for role in message.author.roles:
                if not role.name == "@everyone" : await client.delete_role(message.author, role)
            await client.add_roles(message.author, next(r for r in server.roles if r.name == team))


    #écoute des channels de raid
    elif regex.match(message.channel.name):
        numRaid = int(message.channel.name[0])
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if message.content.lower() == "in":
                    if cCurrent.raid.ajouterParticipant(message.author):
                        await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                        await client.edit_channel(cCurrent.com, name=re.sub(r"-[0-9]*", str("-%i" %(len(cCurrent.raid.participants))), cCurrent.com.name))
                        await editListe(cCurrent)
                        await client.delete_message(message)
            elif message.content.lower() == "out":
                if cCurrent.raid.retirerParticipant(message.author):
                     await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                     await client.edit_channel(cCurrent.com, name=re.sub(r"-[0-9]*", str("-%i" %(len(cCurrent.raid.participants))), cCurrent.com.name))
                     await editListe(cCurrent)
                     await client.delete_message(message)
            elif message.content.lower() == 'abort':
                if message.author == cCurrent.raid.capitaine:
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
            elif args[0].lower() == "dispo" and len(args) == 2:
                userId = args[1].replace('<@', '').replace('>', '')
                if cCurrent.raid.ajouterParticipant(next( m for m in client.get_all_members() if m.id == userId)):
                    await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                    await client.edit_channel(cCurrent.com, name=re.sub(r"-[0-9]*", str("-%i" %(len(cCurrent.raid.participants))), cCurrent.com.name))
                    await editListe(cCurrent)

@client.event
async def on_reaction_add(reaction, user):

    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if regex.match(reaction.message.channel.name):
        numRaid = int(reaction.message.channel.name[0])
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if reaction.emoji == '👌':
                if cCurrent.raid.ajouterParticipant(user):
                    await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                    await client.edit_channel(cCurrent.com, name=re.sub(r"-[0-9]*", str("-%i" %(len(cCurrent.raid.participants))), cCurrent.com.name))
                    await editListe(cCurrent)

@client.event
async def on_reaction_remove(reaction, user):
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if regex.match(reaction.message.channel.name):
        numRaid = int(reaction.message.channel.name[0])
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if reaction.emoji == '👌':
                if cCurrent.raid.retirerParticipant(user):
                    await client.edit_message(cCurrent.pinMsg, embed=cCurrent.raid.embed())
                    await client.edit_channel(cCurrent.com, name=re.sub(r"-[0-9]*", str("-%i" %(len(cCurrent.raid.participants))), cCurrent.com.name))
                    await editListe(cCurrent)

client.run(os.environ['DISCORD_TOKEN'])
