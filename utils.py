import datetime
from utils import *
from data import *
import re
import unidecode
import discord
from Channel import *
from Raid import *

#function hors loop
def isNotBot(m):
    """prend en entree un discord.on_message
    renvoit 1 si l'auteur n'est pas un bot 0 sinon"""
    return m.author.bot != True
def isNotRaid(m):
    """ prend en entre un discord.on_message
    renvoit 0 si c'est un message qui doit rester dans la console de raid
    1 sinon"""
    if m.content.lower() == "**liste des raids en cours**" or m.content.startswith("**Vu sur GymHuntr autour de nous :**") or m.content.lower().startswith("raid en cour sur"): return 0
    return 1
def isRappelCommand(m):
    """ renvoit 1 si c'est un rappel de commande 0 sinon"""
    return m.content.startswith("Comme je suis sympa je te redonne la commande que tu as essayé de taper :")
def isFuture(temps, ref=datetime.datetime.now()):
    """ prend en entree un heure au format %H:%M et test si elle appartien au future du now en entrée
    renvoit 1 si oui
    renvoit 0 si la date n'est pas au bon format ou si l'heure est dans le passée"""
    assert isinstance(ref, datetime.datetime)
    assert isinstance(temps, datetime.datetime)

    return temps > ref
def isPast(temps, ref=datetime.datetime.now()):
    """ prend en entree un heure au format %H:%M et test si elle appartien au passé du now en entrée
    renvoit 1 si oui
    renvoit 0 si la date n'est pas au bon format ou si l'heure est dans le passée"""
    assert isinstance(ref, datetime.datetime)
    assert isinstance(temps, datetime.datetime)

    return temps < ref
def isPokemon(pokeName):
    """prend en entré un nom de pokemon ou un oeuf
    renvoit 1 si'il existe dans le pokedex
    0 sinon"""
    RegexOeuf = re.compile(r"T[0-9]")
    if RegexOeuf.match(str(pokeName)): return 1

    for ip, pokemon in enumerate(pokedex):
        for nom in pokemon.values():
            if nom == str(pokeName).lower(): return 1

    return 0
def lirePokeName(pokeName):
    """ Permet de lire le pokéName donné en entrée grace au dictionnaire de poketrad. Il pourra chercher en français et en anglais
    retourne le numero du pokemon ou le niveau de l'oeuf (negatif)
    retourne 0 si il n'existe pas"""
    RegexOeuf = re.compile(r"t[0-9]")
    if RegexOeuf.match(str(pokeName)):
        num = pokeName[1:]
        if int(num):
            num = int(num)
            if num < 6 and num > 0: return -num

    for ip, pokemon in enumerate(pokedex):
        for nom in pokemon.values():
            if nom == str(pokeName).lower():
                    return ip+1
    return 0
def lirePokeId(pokeId):
    """ permet de lire un pokeId et renvoit le nom du pokemon ou de l'oeuf
    retourn le nom de l'oeuf ou du pokemon
    0 sinon"""
    if pokeId < 0:
        return str("T%i" %(-pokeId))
    elif pokeId > 0 and pokeId < len(pokedex):
        return pokedex[pokeId-1]["fr"]
    else: return 0
def teamName(team):
    """verifie si la team appartien au dictionnaire
    renvoit le teamName si oui, 0 sinon"""
    assert isinstance(team, str)

    for teamName, trad in teamdex.items():
        if team == trad["fr"]: return teamName

    return 0
def isUniquePlace(battlePlace, RaidsList):
    """retourne 1 si l'endroit n'est pas utilisé 0 sinon"""
    assert isinstance(battlePlace, str)

    libre = 1
    for raidElement in RaidsList.values():
        if battlePlace == raidElement.raid.battlePlace: libre = 0
    return libre
def isUniquePlaceGym(battlePlace, RaidsList):
    """retourne 1 si l'endroit n'est pas utilisé 0 sinon"""
    assert isinstance(battlePlace, str)

    libre = 1
    for raidElement in RaidsList.values():
        if battlePlace == raidElement.battlePlace: libre = 0
    return libre
def isOeufName(pokeName):
    """retourne 1 si c'est un nom d'oeuf, O sinon"""
    if isinstance(pokeName, str):
        regexOeuf = re.compile(r"t[1-5]")
        regexEx = re.compile(r"tex")
        if regexOeuf.match(pokeName) or regexEx.match(pokeName): return 1
    return 0
def rappelCommand(commandName):
    """envoi à l'utilisateur un message permettant de reexpliquer la commande"""
    return str("Comme je suis sympa je te redonne la commande que tu as essayé de taper :\n %s" %commandex[commandName])
def getTimeStr(time, label):
    """return the str corresponding to the time at (%H:%M) format with the appropriate label"""

    if time == 0:
        temps = str("%s: ? \n" %label)
    else:
        assert isinstance(time, datetime.datetime)
        temps = str("%s: %s \n" %(label, time.strftime("%H:%M")))

    return temps
def isHour(time):
    """renvoit 1 si l'heure est au bon format pour etre transformé en heure, 0 sinon"""
    try:
        assert isinstance(time, str)

        regex = re.compile(r"[0-9]*:[0-9]*")
        assert regex.match(time)

        args = time.split(":")
        assert len(args) == 2 and isinstance(int(args[0]), int) and isinstance(int(args[1]), int)

        heure = int(args[0])
        minute = int(args[1])
        assert heure < 24 and heure >= 0
        assert minute < 60 and minute >= 0

    except AssertionError:
        return 0

    return 1
def convertTime(time):
    args = time.split(":")
    time = datetime.datetime.now()
    time = time.replace(hour=int(args[0]), minute=int(args[1]), second=0)

    return time
def getNumChannel(name):
    """retourne l'id du salon"""
    index = name.find("_")
    numRaid = int(name[:index])
    assert(numRaid > 0)

    return numRaid
def isLevel(lvl):
    """renvoit 1 si c'est un level correct 0 sinon"""
    assert isinstance(lvl, int)

    if lvl <= 40 and lvl > 0:
        return 1
    else:
        return 0
def sendHelp():
    """construct the help message to send to the user"""

    message = "**Voilà un petit rappel des commandes que tu peux utiliser avec le PoGoBot**\n\n"

    for name, command in commandex.items():
        message += str("**%s:**\t\t%s\n" %(name, command))

    message += "\nPour des renseignements plus prescis rend toi directement sur la doc en ligne :\n <https://github.com/12rambau/poGoBot/wiki>"
    return message
def setAbled(before, after):
    """ renvoit 1 si on vient de retirer disable au membre"""
    assert isinstance(before, discord.Member)
    assert isinstance(after, discord.Member)

    for bRole in before.roles:
        if bRole.name == "disable":
            for aRole in after.roles:
                if aRole == "disable":
                    return 0
            return 1
    return 0
def isAble(member):
    """renvoit 1 si le user est able 0 sinon"""
    assert isinstance(member, discord.Member)

    for role in member.roles:
        if role.name == "disable": return 0

    return 1
def lireLieu(lieu):
    """renvoit le lieu issu de GymHuntr formaté comme il se doit"""
    assert isinstance(lieu, str)

    return unidecode.unidecode(u"%s" %lieu.lower().replace(".**", "").replace("**", ""))
def lireHeure(temps):
    """retourne le temps donné par GymHuntr au format attendu par Raid"""
    assert isinstance(temps, str)

    temps = temps.replace("*Raid Ending: ", "").replace("*Raid Starting: ", "").replace("*", "")
    temps = temps.split(" ")
    temps = datetime.timedelta(hours= int(temps[0]), minutes=int(temps[2]), seconds=int(temps[4]))
    temps = datetime.datetime.now() + temps

    return temps
def updateGym(raid, gymList):
    """replace the old gym informations with the updated one"""
    #assert isinstance(raid, Raid)

    index = -1
    for key, gym in gymList.items():
        if gym.battlePlace == raid.battlePlace:
            index = key
            break

    if not index == -1 : gymList[index] = raid
def removeGym(raid, gymList):
    """remove the raid that has the same place as the parameter raid"""
    #assert isinstance(raid, Raid)

    index = -1
    for key, gym in gymList.items():
        if gym.battlePlace == raid.battlePlace:
            index = key
            break
    if not index == -1: gymList.pop(key)
def readGymEmbed(embed):
    """return the tuple of crucial information (pokeName, battlePlace, battleTime)"""

    args = embed["description"].split ("\n")
    pokeName = ""
    if not embed["title"].find("Raid is starting soon!") == -1:
        pokeName = str("t%s" %embed["title"].split(" ")[1])
        battleTime = lireHeure(args[1])
    elif not embed["title"].find("Raid has started!") == -1:
        pokeName = args[1].lower()
        battleTime = lireHeure(args[3])
    else:
        raise Exception("pas reussi à lire")

    battlePlace = lireLieu(args[0])
    return (pokeName, battlePlace, battleTime)

if __name__=="__main__":
    pass
