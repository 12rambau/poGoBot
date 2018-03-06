import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import datetime
import re
from Raid import *
from Channel import *

Client = discord.Client()
client = commands.Bot(command_prefix = "?")


@client.event
async def on_ready():

    global compteur
    compteur = 0

    #creer les 5 channels qui seront utilisés par les joueurs
    ich = 0
    global channels
    channels = []
    while ich < Channel.nbChannelMax:
        channels.append(Channel(ich+1))
        ich += 1
    print ("fin de la création des %i channels \n" %(Channel.nbChannelMax))

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
    global compteur
    args = message.content.split(" ")

    if message.content == "cookie":
        compteur = compteur + 1
        await client.send_message(message.channel, "%i :cookie:" %(compteur) )

    if (message.channel.name == "raid-add"):
        if message.content.upper().startswith("ADD"):
            if len(args) < 4:
                return
            #verifier que le pokemon existe
            pokeName = args[1]
            #verifier que l'heure a du sens
            battleTime = args[2]
            #verifier que le lieu existe
            battlePlace = ' '.join(args[3:])

            #on cherche une conversation de libre
            global channels
            libre = Channel.channelLibre(channels)
            if libre == 0:
                await client.send_message(message.channel, "tout est pris mon pote va jouer avec les autres")
                return

            activeChannels = client.get_all_channels()
            for channel in activeChannels:
                if channel.name == str("raid-%i" %(libre)):
                    await client.send_message(message.channel, "j'ai trouvé une channel de libre")
                    channelCom = channel

                    raid = Raid(1,pokeName,message.author.nick, battleTime, battlePlace)
                    channels[libre-1].ajouterRaid(raid)

                    await client.send_message(channelCom, embed=raid.embed())
                    break
    #'edit'
        # nom de l'arene
        # nom du pokemon (l'arène doit être un oeuf et exister)

    #écoute des channels de raid
    regex = re.compile(r"raid-[0-9]")
    if regex.match(message.channel.name):
        numRaid = int(message.channel.name[5:])
        channel = channels[numRaid-1]
        channelCom = message.channel
        if channel.isRaid():
            if message.content.lower() == "in":
                if not channel.raid.isParticipant(message.author.nick):
                    channel.raid.ajouterParticipant(message.author.nick)
                    await client.send_message(channelCom, embed=channel.raid.embed())
            elif message.content.lower() == "out":
                if channel.raid.isParticipant(message.author.nick):
                    channel.raid.retirerParticipant(message.author.nick)
                    await client.send_message(channelCom, embed=channel.raid.embed())
            elif message.content.lower() == 'abort':
                if message.author.nick == channel.raid.capitaine:
                    if channel.retirerRaid():
                        await client.send_message(channelCom, "le raid a été abandonné")
            elif args[0] == "launch" and len(args) == 2:
                channel.raid.choisirLaunch(args[1])
                await client.send_message(channelCom, embed=channel.raid.embed())
            elif args[0].lower() == "edit" and len(args) == 2:
                pokeName = args[1]
                ierr = channel.raid.faireEclore(pokeName)
                if not ierr:
                    return
                await client.send_message(channelCom, embed=channel.raid.embed())




client.run(os.environ['DISCORD_TOKEN'])
