import datetime
from utils import *
from data import *
import re

#function hors loop
def is_bot(m):
    """prend en entree un discord.on_message
    renvoit 1 si l'auteur n'est pas un bot 0 sinon"""
    global msgRaid
    return m.author.bot != True
def isFuture(temps, now=datetime.datetime.now()):
    """ prend en entree un heure au format %H:%M et test si elle appartien au future du now en entrée
    renvoit 1 si oui
    renvoit 0 si la date n'est pas au bon format ou si l'heure est dans le passée"""
    if not isinstance(now, datetime.datetime): return 0
    args = temps.split(":")
    if not (len(args) == 2 and isinstance(int(args[0]), int) and isinstance(int(args[1]), int)): return 0
    temps = now.replace(hour=int(args[0]), minute=int(args[1]), second=0)

    return temps > now
def isPast(temps, now=datetime.datetime.now()):
    """ prend en entree un heure au format %H:%M et test si elle appartien au passé du now en entrée
    renvoit 1 si oui
    renvoit 0 si la date n'est pas au bon format ou si l'heure est dans le passée"""
    if not isinstance(now, datetime.datetime): return 0
    args = temps.split(":")
    if not (len(args) == 2 and isinstance(int(args[0]), int) and isinstance(int(args[1]), int)): return 0
    temps = now.replace(hour=int(args[0]), minute=int(args[1]), second=0)

    return temps < now
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
    RegexOeuf = re.compile(r"T[0-9]")
    if RegexOeuf.match(str(pokeName)):
        num = pokeName[1:]
        if not int(num): return 0
        num = int(num)
        if not (num < 6 and num > 0): return 0
        return -num

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
def isTeam(team):
    """verifie si la team appartien au dictionnaire
    renvoit le teamName si oui, 0 sinon"""
    if not isinstance(team, str): return 0

    for teamName, trad in teamdex.items():
        if team == trad["fr"]: return teamName

    return 0
def isUniquePlace(battlePlace, cRaids):
    """retourne 1 si l'endroit n'a jamais été utilisé 0 sinon"""
    if not isinstance(battlePlace, str): return 0
    if cRaids.values():
        for cCurrent in cRaids.values():
            if battlePlace == cCurrent.raid.battlePlace: return 0

    return 1
def isOeufName(pokeName):
    """retourne 1 si c'est un nom d'oeuf, O sinon"""
    if isinstance(pokename, str):
        regexOeuf = re.compile(r"T[0-9]")
        regexEx = re.compile(r"Tex")
        if regexOeuf.match(pokeName) or regexEx.match(pokeName): return 1
    return 0
def rappelCommand(commandName):
    """envoi à l'utilisateur un message permettant de reexpliquer la commande"""
    return str("comme je suis sympa je te redonne la commande que tu as essayé de taper :\n %s" %commandex[commandName])

if __name__=="__main__":
    #debut des test unitaires
    temps = "00:10"
    now = datetime.datetime.now()
    if isFuture(temps): print(str("%s c'est dans le future" %temps))
    if isFuture(temps, now): print(str("%s c'est dans le future" %temps))
    if isPast(temps, now): print(str("%s c'est dans le passé" %temps))
