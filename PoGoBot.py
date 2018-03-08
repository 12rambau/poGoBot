import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime
import re
import os
from Raid import *
from Channel import *
from data import *
from utils import *

Client = discord.Client()
client = commands.Bot(command_prefix = "?")

cookieCompteur = 0
cRaids = {}
server = 0

cAccueil = 0
cDiscussion = 0
cPokemon = 0
cRaidAdd = 0

#gesionnaire de la liste de RAid
async def addToListe(cRaid):
    """ajoute un raid à la liste des raids"""
    #variables externes
    global cRaidAdd

    if not isinstance(cRaid, ChannelRaid):
        print ('bite')
        return 0

    await client.purge_from(cRaidAdd, check=is_bot)
    content = str("raid en cour sur <#%s>" %(cRaid.com.id))
    msg = await client.send_message(cRaidAdd, content=content, embed=cRaid.raid.embed())
    cRaid.listMsg = msg
    return 1
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

#gestionnaire des Raid channels du forum
async def removeCRaid(cRaid):
    """retire la channel de la liste des raid
    renvoit 1 si reussi
    0 sinon"""
    if not isinstance(cRaid, ChannelRaid): return 0
    #await client.send_message(cRaid.com, "Attention dans 1 min je vais détruire ce salon, n'oubliez pas de vous dire au revoir !")
    cId = cRaid.com.id
    await removeFromListe(cRaid)
    await client.delete_channel(client.get_channel(cId))
    return 1
async def editCRaid(cRaid):
    """edite les information du raid
    renvoit 1 si reussi
    0 sinon"""
    if not isinstance(cRaid, ChannelRaid): return 0
    await client.edit_message(cRaid.pinMsg, embed=cRaid.raid.embed())
    await client.edit_channel(cRaid.com, name=re.sub(r"-[0-9]*", str("-%i" %(len(cRaid.raid.participants))), cRaid.com.name))
    await editListe(cRaid)
    return 1

#gestionnaires de la channel d'accueil
async def addLevel(lvl, member):
    """retourn 1 si l'ajout nu niveau a fonctionné
    0 sinon"""
    if not isinstance(lvl, int): return 0
    if not isinstance(member, discord.Member): return 0

    regex = re.compile(r"^.* \([0-9]*\)$") #un nick avec un niveau
    if regex.match(member.nick):
        newNick = re.sub(r"\([0-9]*\)$", str("(%i)" %(lvl)), member.nick)
    else:
        newNick = member.nick + str(" (%i)" %(lvl))

    await client.change_nickname(member, newNick)
async def changeTeam(team, user):
    """enleve tous les rôles d'un utilisateur sauf @everyone et @modo puis place le member dans la team appropriée
    return 1 si le changement est effectif 0 sinon"""
    if not isinstance(member, discord.Member): return 0

    for role in member.roles:
        if not (role.name == "@everyone" or role.name == "@modo"): await client.delete_role(member, role)
    await client.add_roles(member, next(r for r in server.roles if r.name == team))


# timer toutes les 10s
async def waitTimer():
    while True:
        await asyncio.sleep(10)

        regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid

        for cCurrent in client.get_all_channels():
            if regex.match(cCurrent.name):
                numRaid = int(cCurrent.name[0])
                cRaidCurrent = cRaids[numRaid]
                date = datetime.datetime.now()
                if cRaidCurrent.raid.fin < date:
                    if not cRaidCurrent.retirerRaid(): continue
                    if not await removeCRaid(cRaidCurrent): continue

#routine demarage
@client.event
async def on_ready():
    #variable externes
    global cAccueil
    global cDiscussion
    global cPokemon
    global cRaidAdd
    global server

    #recuperer le server
    server = client.get_server(os.environ["DISCORD_SERVER_ID"])

    #on identifie tous les salon sur lesquel peut agir le bot
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    cToDelete = []
    for cCurrent in client.get_all_channels():
        if cCurrent.name == "accueil":
            cAccueil = cCurrent
        elif cCurrent.name == "discussion":
            cDiscussion = cCurrent
        elif cCurrent.name == "pokemon":
            cPokemon = cCurrent
        elif cCurrent.name == "raid":
            cRaidAdd = cCurrent
            await client.purge_from(cRaidAdd)
        elif regex.match(cCurrent.name):
            cToDelete.append(cCurrent)

        for cCurrent in cToDelete:
            await client.delete_channel(cCurrent)

    #ecrire le message initiale des raid
    await client.send_message(cRaidAdd, "liste des raides en cours")

    print("Bot is ready and back online !")

    #on lance le garbage collector
    await waitTimer()

    #si on atteint cet endroit c'est que le garbage collector a craché
    print ('bug')

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

    #variables internes
    args = message.content.split(" ")
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if message.content == "cookie":
        cookieCompteur +=  1
        await client.send_message(message.channel, "%i :cookie:" %(cookieCompteur) )
        await client.delete_message(message)

    #on écoute la channel d'add
    elif message.channel == cRaidAdd:
        if message.content.lower().startswith("add") and not len(args) < 4:
            pokeName = args[1]
            battleTime = args[2]
            battlePlace = ' '.join(args[3:])

            cCom = await client.create_channel(server, str("%i_%s-0" %(ChannelRaid.nb_channel+1,pokeName)))
            cRaids[ChannelRaid.nb_channel] = ChannelRaid(cCom)
            raid = Raid(0,pokeName,message.author, battleTime, battlePlace)
            cRaid = cRaids[ChannelRaid.nb_channel].ajouterRaid(raid)

            if not await addToListe(cRaid): return
            cRaid.pinMsg = await client.send_message(cCom, embed=raid.embed())
            await client.pin_message(cRaid.pinMsg)

    #on écoute la channel d'accueil
    elif message.channel == cAccueil:
        if message.content.lower().startswith("lvl") and len(args) == 2:
            lvl = int(args[1])
            if not await addLevel(lvl, message.author): return
            await client.delete_message(message)
        if message.content.lower().startswith("team") and len(args) == 2:
            team = args[1]
            if not await changeTeam(team, user): return
            await client.delete_message(message)


    #écoute des channels de raid
    elif regex.match(message.channel.name):
        numRaid = int(message.channel.name[0])
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if message.content.lower() == "in":
                if not cCurrent.raid.ajouterParticipant(message.author): return
                if not await editCRaid(cCurrent): return
                await client.delete_message(message)
            elif message.content.lower() == "out":
                if not cCurrent.raid.retirerParticipant(message.author): return
                if not await editCRaid(cCurrent): return
                await client.delete_message(message)
            elif message.content.lower() == 'abort':
                if not message.author == cCurrent.raid.capitaine: return
                if not cCurrent.retirerRaid(): return
                if not await removeCRaid(cCurrent): return
            elif args[0] == "launch" and len(args) == 2:
                battleTime = args[1]
                if not cCurrent.raid.choisirLaunch(battleTime): return
                if not await editCRaid(cCurrent): return
                await client.delete_message(message)
            elif args[0].lower() == "edit" and len(args) == 2:
                pokeName = args[1]
                if not cCurrent.raid.faireEclore(pokeName): return
                if not await editCRaid(cCurrent): return
                await client.delete_message(message)
            elif args[0].lower() == "dispo" and len(args) == 2:
                userId = args[1].replace('<@', '').replace('>', '').replace('!','')
                if not cCurrent.raid.ajouterParticipant(next( m for m in client.get_all_members() if m.id == userId)): return
                if not await editCRaid(cCurrent): return

#ajout d'emoji
@client.event
async def on_reaction_add(reaction, user):
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if regex.match(reaction.message.channel.name):
        numRaid = int(reaction.message.channel.name[0])
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if reaction.emoji == '👌':
                if not cCurrent.raid.ajouterParticipant(user): return
                if not await editCRaid(cCurrent): return

#retrait d'emoji
@client.event
async def on_reaction_remove(reaction, user):
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if regex.match(reaction.message.channel.name):
        numRaid = int(reaction.message.channel.name[0])
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if reaction.emoji == '👌':
                if not cCurrent.raid.retirerParticipant(user): return
                if not await editCRaid(cCurrent): return

client.run(os.environ['DISCORD_TOKEN'])
