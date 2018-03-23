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
    if m.content.lower() == "**liste des raids en cours**" or m.content.startswith("**Vu sur GymHuntr autour de nous :**") or m.content.lower().startswith("raid en cour sur")or m.content.lower() == "**liste des raids ex**": return 0
    return 1
def isRappelCommand(m):
    """ renvoit 1 si c'est un rappel de commande 0 sinon"""
    return m.content.startswith("Comme je suis sympa je te redonne la commande que tu as essayé de taper :")

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
