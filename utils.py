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
def isFuture(temps):
    """ prend en entree un heure au format %H:%M et test si elle appartien au future
    renvoit 1 si oui
    renvoit 0 si la date n'est pas au bon format ou si l'heure est dans le passée"""
    args = temps.split(":")
    if not (len(args) == 2 and isinstance(int(args[0]), int) and isinstance(int(args[1]), int)): return 0
    now = datetime.datetime.now()
    temps = now.replace(hour=int(args[0]), minute=int(args[1]), second=0)

    return temps > now
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
        num = pokeId[1:]
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

if __name__=="__main__":
    #debut des test unitaires
    temps = "23:00"
    if isFuture(temps): print("%s c'est dans le future" %temps)
