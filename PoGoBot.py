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
import unidecode
import sys

Client = discord.Client()
client = commands.Bot(command_prefix = "")

cookieCompteur = 0
cRaids = {}
cGyms = {}
server = 0

cAccueil = 0
cRaidAdd = 0
cAdmin = 0

msgGymHuntr = 0

#gesionnaire de la liste de RAid
async def addToListe(cRaid):
    """ajoute un raid à la liste des raids"""
    #variables externes
    global cRaidAdd

    if not isinstance(cRaid, ChannelRaid): return 0

    await client.purge_from(cRaidAdd, check=isNotRaid)
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

#gestionnaires de la liste de GymHuntr
async def updateGymList(msg):
    """update le message des raids alentours"""
    print("coucou c'est moi")
    content = "**Vu sur GymHuntr autour de nous :**\n"
    if len(list(cGyms)) == 0:
        content += "pas de raid en vue, c'est visiblement pas l'heure"
    else:
        for gym in cGyms.values():
            content += gym.outText()
    await client.edit_message(msg, new_content=content)

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
    newName = re.sub(r"-[0-9]*", str("-%i" %(len(cRaid.raid.participants))), cRaid.com.name)
    newName = re.sub(r"t[0-9]", lirePokeId(cRaid.raid.pokeId), newName)
    await client.edit_channel(cRaid.com, name=newName)
    await editListe(cRaid)
    return 1
async def pasCApitaine(channel):
    """message à envoyer au personne pas capitaine qui veulent faire des trucs de capitaines"""
    assert isinstance(channel, discord.Channel)

    await client.send_message(channel, "privilège du chef c.a.d..... pas toi ;-)")

#gestionnaires de la channel d'accueil
async def addLevel(lvl, member):
    """ajoute un nouveau nickname à l'utilisateur"""
    assert isinstance(lvl, int) and lvl > 0 and lvl < 41
    assert isinstance(member, discord.Member)

    regex = re.compile(r"^.* \([0-9]*\)$") #un nick avec un niveau

    nick = member.nick if member.nick else  member.name

    if regex.match(nick):
        newNick = re.sub(r"\([0-9]*\)$", str("(%i)" %(lvl)), nick)
    else:
        newNick = nick + str(" (%i)" %(lvl))

    await client.change_nickname(member, newNick)
async def changeTeam(team, member):
    """enleve tous les rôles d'un utilisateur sauf '@everyone' et '@modo' puis place le member dans la team appropriée
    return 1 si le changement est effectif 0 sinon"""
    team = teamName(team)
    assert team
    assert isinstance(member, discord.Member)

    for role in member.roles:
        if role.name.startswith("almost_"): return 0

    previous = False
    old_team = "rien"
    for role in member.roles:
        if teamdex.get(str("%s" %role.name)):
            previous = True
            old_team = role.name
            await client.remove_roles(member, role)
    if previous:
        await client.send_message(member, str("Tu vas rejoindre la team %s. Comme tu avais déjà une team, tu vas rester sans rôle pendant 1 heure et l'administrateur a été informé de ce changement." %team))
        await client.send_message(server.owner, str("<@%s> va passé de la team %s à la team %s" %(member.id, old_team, team )))
        attente = next(r for r in server.roles if r.name == str("almost_%s" %(team)))
        await client.add_roles(member, attente)
        await asyncio.sleep(3600) #1 heure entière sans rôle
        await client.remove_roles(member, attente)

    await client.add_roles(member, next(r for r in server.roles if r.name == team))
    return 1
async def changeNick(newNick, member):
    """donne un surnom au joueur en tenant compte du niveau eventuellement renseigner"""
    assert isinstance(member, discord.Member)

    regex = re.compile(r"^.* \([0-9]*\)$") #un nick avec un niveau

    nick = member.nick if member.nick else  member.name

    if regex.match(nick):
        newNick = re.sub(r"^.* \(", str("%s (" %newNick), nick)

    await client.change_nickname(member, newNick)
async def freeFreshmen(member):
    """remove the disable role of the member if he has it"""
    assert isinstance(member, discord.Member)

    try:
        disable = next(r for r in member.roles if r.name == "disable")
    except StopIteration:
        return

    await client.remove_roles(member, disable)

# timer toutes les 10s
async def waitTimer():

    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid

    while True:
        await asyncio.sleep(60)

        now = datetime.datetime.now()

        #test pour comprendre le bug de suppression des raids
        try:
            toDelete = []
            for cCurrent in client.get_all_channels():
                if regex.match(cCurrent.name):
                    print("il y a match")
                    numRaid = getNumChannel(cCurrent.name)
                    cRaidCurrent = cRaids[numRaid]
                    if cRaidCurrent.raid.fin < now:
                        print ("il faut le detruire c'est le mal")
                        toDelete.append(cRaidCurrent)

            for cRaidCurrent in toDelete:
                cId = cRaidCurrent.id
                cRaidCurrent.retirerRaid()
                await removeCRaid(cRaidCurrent)
                del cRaids[cId]
        except: #catch all errors
            await client.send_message(cAdmin, "j'ai bugé")
            e = sys.exc_info()[0]
            await client.send_message(cAdmin, str("erreur : \n%s" %e))
            continue

#routine demarage
@client.event
async def on_ready():
    #variable externes
    global cAccueil
    global cRaidAdd
    global server
    global cAdmin

    #recuperer le server
    server = client.get_server(os.environ["DISCORD_SERVER_ID"])

    #on identifie tous les salon sur lesquel peut agir le bot
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    cToDelete = []
    for cCurrent in server.channels:
        if cCurrent.name.lower() == "accueil":
            cAccueil = cCurrent
        elif cCurrent.name.lower() == "raid":
            cRaidAdd = cCurrent
            await client.purge_from(cRaidAdd)
        elif cCurrent.name.lower() == "admin":
            cAdmin = cCurrent
            await client.send_message(cAdmin, "Bot is ready and back online !")
        elif regex.match(cCurrent.name):
            cToDelete.append(cCurrent.id)

    for cId in cToDelete:
        await client.delete_channel(client.get_channel(cId))

    #ecrire le message de GymHuntr
    await client.send_message(cRaidAdd, "je vais pas rester")

    #ecrire le message initiale des raid
    await client.send_message(cRaidAdd, "Liste des raids en cours")

    print("Bot is ready and back online !")

    #changer les couleurs des utilisateurs en attente
    for member in server.members:
        for role in member.roles:
            if role.name.startswith("almost_"):
                oldRole = role
                team = role.name.replace ("almost_", "")
                newRole = next(r for r in server.roles if r.name == team)
                await client.remove_roles(member, oldRole)
                await client.add_roles(member, newRole)

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
    global cAdmin

    #se debarasser des messages privés et des disabled
    if message.channel.is_private or not isAble(message.author): return

    #variables internes
    args = message.content.lower().split(" ")
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid

    #n'import où si on lui parle
    if message.content.lower() == str("<@%s>" %client.user.id):
        await client.send_message(message.channel, sendHelp())
        await client.delete_message(message)
    elif message.content.lower() == "!cookie" :
        cookieCompteur +=  1
        await client.send_message(message.channel, "%i :cookie:" %(cookieCompteur) )
        await client.delete_message(message)
    elif message.content.lower().startswith("!lvl") and len(args) == 2:
        #variable check
        try:
            lvl = int(args[1])
            assert isLevel(lvl)
        except (ValueError, AssertionError):
            await client.send_message(message.channel, rappelCommand("lvl"))
            return

        await addLevel(lvl, message.author)
        await client.delete_message(message)
    elif message.content.lower().startswith("!team") and len(args) == 2:
        #variable check
        team = args[1]
        try:
            assert teamName(team)
        except AssertionError:
            await client.send_message(message.channel, rappelCommand("team"))
            return

        await changeTeam(team, message.author)
        await client.delete_message(message)
    elif message.content.lower().startswith("!nick"):
        #variable check
        try:
            assert len(args) == 2
            newNick = args[1]
        except AssertionError:
            await client.send_message(message.channel, rappelCommand("nick"))
            return

        await changeNick(newNick, message.author)
        await client.delete_message(message)

    #écoute des channels de raid
    elif regex.match(message.channel.name):
        numRaid = getNumChannel(message.channel.name)
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if args[0].lower() == "!in" and len(args) == 2:
                    userId = args[1].replace('<@', '').replace('>', '').replace('!','')
                    try:
                        user = next( m for m in client.get_all_members() if m.id == userId)
                    except StopIteration:
                        await client.send_message(message.channel, rappelCommand("in"))
                        return

                    cCurrent.raid.ajouterParticipant(user)
                    await editCRaid(cCurrent)
            elif args[0].lower() == "!out" and len(args) == 2:
                    userId = args[1].replace('<@', '').replace('>', '').replace('!','')
                    try:
                        user = next( m for m in client.get_all_members() if m.id == userId)
                    except StopIteration:
                        await client.send_message(message.channel, rappelCommand("out"))
                        return

                    cCurrent.raid.retirerParticipant(user)
                    await editCRaid(cCurrent)
            elif message.content.lower() == "!in":
                    cCurrent.raid.ajouterParticipant(message.author)
                    await editCRaid(cCurrent)
                    await client.delete_message(message)
            elif message.content.lower() == "!out":
                    cCurrent.raid.retirerParticipant(message.author)
                    await editCRaid(cCurrent)
                    await client.delete_message(message)
            elif message.content.lower() == '!abort':
                    if message.author == cCurrent.raid.capitaine:
                        cCurrent.retirerRaid()
                        await removeCRaid(cCurrent)
                        del cRaids[cCurrent.id]
                    else:
                        await pasCApitaine(messageChannel)
            elif message.content.lower().startswith("!chef"):
                #variable check
                try:
                    assert len(args) == 2
                    memberId = args[1].replace('<@', '').replace('>', '').replace('!','')
                    member = next( m for m in server.members if m.id == memberId)
                except (AssertionError, StopIteration):
                    await client.send_message(message.channel, rappelCommand("chef"))
                    return

                if message.author == cCurrent.raid.capitaine:
                    cCurrent.raid.setCapitaine(member)
                    await editCRaid(cCurrent)
                else:
                    await pasCApitaine(message.channel)
            elif args[0] == "!launch" and len(args) == 2:
                    battleTime = args[1]
                    try:
                        assert isHour(battleTime)
                        battleTime = convertTime(battleTime)
                        assert isFuture(battleTime)
                        assert isPast(battleTime, cCurrent.raid.fin)
                    except AssertionError:
                        await client.send_message(message.channel, rappelCommand("launch"))
                        return

                    cCurrent.raid.choisirLaunch(battleTime)
                    await editCRaid(cCurrent)
                    await client.delete_message(message)
            elif args[0].lower() == "!edit" and len(args) == 2:
                    pokeName = unidecode.unidecode(u"%s" %(args[1]))
                    try:
                        assert isPokemon(pokeName)
                    except AssertionError:
                        await client.send_message(message.channel, rappelCommand("edit"))
                        return

                    cCurrent.raid.faireEclore(pokeName)
                    await editCRaid(cCurrent)
                    await client.delete_message(message)

    #on écoute la channel d'add
    elif message.channel == cRaidAdd:
        if message.content.lower() == "je vais pas rester":
            msgGymHuntr = message
            await updateGymList(msgGymHuntr)
        if message.content.lower().startswith("!add") and not len(args) < 4:
            pokeName = unidecode.unidecode(u"%s" %(args[1]))
            battleTime = args[2]
            battlePlace = unidecode.unidecode(u"%s" %(' '.join(args[3:])))

            #variable check
            try:
                assert isHour(battleTime)
                battleTime = convertTime(battleTime)
                assert isFuture(battleTime)
                assert (isPokemon(pokeName) or isOeufName(pokeName))
                assert isUniquePlace(battlePlace, cRaids)
            except AssertionError:
                await client.send_message(message.channel, rappelCommand("add"))
                return

            cCom = await client.create_channel(server, str("%i_%s-0" %(ChannelRaid.nb_channel+1,pokeName)))
            cRaids[ChannelRaid.nb_channel] = ChannelRaid(cCom)
            raid = Raid(0,pokeName,message.author, battleTime, battlePlace)
            cRaid = cRaids[ChannelRaid.nb_channel].ajouterRaid(raid)

            await addToListe(cRaid)
            cRaid.pinMsg = await client.send_message(cCom, embed=raid.embed())
            await client.pin_message(cRaid.pinMsg)
        elif message.content.lower() == "!purge":
            await client.purge_from(cRaidAdd, check=isNotRaid)
        elif isNotBot(message) : await client.delete_message(message)

    elif message.channel == cAccueil:
        if message.content.lower().startswith("!free") and len(args) == 2:
            #variable check
            userId = args[1].replace('<@', '').replace('>', '').replace('!','')
            try:
                user = next( m for m in client.get_all_members() if m.id == userId)
            except StopIteration:
                await client.send_message(message.channel, rappelCommand('free'))
                return

            await freeFreshmen(user)
            await client.delete_message(message)

    elif message.channel.name == "gymhuntr":
        args = message.embeds[0]["descripsion"].lower().split("\n")
        pokeName = args[1].lower()
        battleTime = lireHeure(args[3])
        battlePlace = lireLieu(args[0])

        #variable check
        try:
            assert isUniquePlace(battlePlace, cRaids)
        except AssertionError:
            return

        raid = Raid(0,pokeName,message.author, battleTime, battlePlace)
        if isUniquePlace(raid.battlePlace, cGyms):
            cGyms.append(raid)
        else:
            updateGym(raid, cGym)

        await updateGymList()

#ajout d'emoji
@client.event
async def on_reaction_add(reaction, user):
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if regex.match(reaction.message.channel.name):
        numRaid = getNumChannel(reaction.message.channel.name)
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if reaction.emoji == '👌':
                cCurrent.raid.ajouterParticipant(user)
                await editCRaid(cCurrent)

#retrait d'emoji
@client.event
async def on_reaction_remove(reaction, user):
    regex = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*") #nom des channels de raid
    if regex.match(reaction.message.channel.name):
        numRaid = getNumChannel(reaction.message.channel.name)
        cCurrent = cRaids[numRaid]
        if cCurrent.isRaid():
            if reaction.emoji == '👌':
                cCurrent.raid.retirerParticipant(user)
                await editCRaid(cCurrent)

@client.event
async def on_member_update(before, after):
    try:
        assert setAbled(before, after)
    except AssertionError:
        return

    intro = ""
    try:
        intro = next(m for m in await client.pins_from(cAdmin) if m.content.startswith("!intro"))
    except StopIteration:
        await client.send_message(after, "va reveiller ton admin et dis lui qu'il a oublié le message d'accueil. Au fait BONJOUR !!")
    await client.send_message(after, intro.content.replace("!intro", ""))



@client.event
async def on_member_join(member):
    try:
        role = next(r for r in server.roles if r.name == "disable")
    except StopIteration:
        await client.send_message(server.owner, "votre server ne comporte pas de sécurrité n'importe qui peut y faire n'importe quoi")

    await client.add_roles(member, role)
    await client.send_message(member, "Pour activer ta préscence sur le forum %s, merci de nous envoyer un screenshot de ton profil sur le salon #accueil du forum" %server.name)

client.run(os.environ['DISCORD_TOKEN'])
