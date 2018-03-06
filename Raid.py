import time
import datetime
import re
from pokedex import *
import discord

class Raid:
    """ classe permettant de décrire un raid instancié:
    - id: numero de la salle dans laquelle s'effectue le raid (il ne doit donc pas dépasser 5)
    - pokeId : numero du pokemon (chiffre negatif pour les niveaux d'oeuf)
    - participant[]: tableau des noms des participants
    - lancement: heure de lancement du raid
    - fin: heure de fin du raids
    - eclosion: si c'est un oeuf on met l'heure d'éclosion
    - battlePlace: le lieu du raid"""

    nb_salon = 5
    temps_presence = datetime.timedelta(minutes=45)

    def __init__(self, id, pokeId, capitaine, temps, battlePlace):
        """constructeur parametré permettant de creer un Raid avec tous les paramettres"""

        #pour l'instant je fais confiance à mes utilisateurs
        self.id = id
        self.pokeId = Raid.lirePokeId(pokeId)
        self.participants = []
        self.lancement = 0
        self.capitaine = capitaine
        if self.pokeId < 0:
            self.eclosion = datetime.datetime.strptime(temps, "%H:%M")
            self.fin = 0
        elif self.pokeId > 0:
            self.fin = datetime.datetime.strptime(temps, "%H:%M")
            self.eclosion = 0
        self.battlePlace = battlePlace

    def afficherConsole(self):
        """permet d'afficher en console le raid selectionné"""
        print("id: %i" %(self.id))
        print("pokeId: %i" %(self.pokeId))
        print("nb Participants: %i" %(len(self.participants)))
        if isinstance(self.lancement, datetime.datetime):
            print ("lancement à: %s" %(self.lancement.strftime("%H:%M")))
        else:
            print ("lancement : ?")
        if isinstance(self.fin, datetime.datetime):
            print("fin à: %s" %(self.fin.strftime("%H:%M")))
        else:
            print("fin à: ?")
        if isinstance(self.eclosion, datetime.datetime):
            print("eclosion: %s" %(self.eclosion.strftime("%H:%M")))
        else:
            print("eclosion: ?")

    def lirePokeId(pokeId):
        """ Permet de lire le pokéId donné en entré grace au dictionnaire de poketrad
        Il pourra chercher en français et en anglais
        retourne le numero du pokemon ou le niveau de l'oeuf (negatif)
        retourne 0 si il n'existe pas"""
        RegexOeuf = re.compile(r"T[0-9]")
        if RegexOeuf.match(str(pokeId)):
            num = pokeId[1:]
            try:
                if isinstance(int(num), int):
                    num = int(num)
                    if num < 6 and num > 0:
                        return -num
            except:
                pass

        for ip, pokemon in enumerate(pokedex):
            for nom in pokemon.values():
                if nom == str(pokeId).lower():
                    return ip+1
        return 0

    def embed(self):
        """ Retourne un embed formaté pour être lu par discord"""
        if self.pokeId > 0:
            embed = discord.Embed(title = pokedex[self.pokeId-1]["fr"].upper())
        else:
            embed = discord.Embed(title=str("Raid LvL%i" %(-self.pokeId)))

        if self.pokeId > 0:
            url = str("https://pokemon.gameinfo.io/images/pokemon/%i.png" %(self.pokeId))
        elif self.pokeId == -5:
            url = "https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2017/06/Pokemon-GO-Legendary-Egg.png"
        elif self.pokeId == -4 or self.pokeId == -3:
            url = "https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2017/06/Pokemon-GO-Rare-Egg-Yellow.png"
        elif self.pokeId == -2 or self.pokeId == -1:
            url = "https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2017/06/Pokemon-GO-Normal-Egg-Pink.png"
        embed.set_thumbnail(url=url)
        field = str("capitaine: @%s \n" %(self.capitaine))
        if self.lancement == 0:
            field += str("lancement: ? \n")
        else:
            field += str("lancement: %s \n" %(self.lancement.strftime("%H:%M")))
        if self.pokeId < 0:
            field += str('ecclosion: %s \n' %(self.eclosion.strftime("%H:%M")))
        else:
            field += str('fin: %s \n' %(self.fin.strftime("%H:%M")))
        field += str("%i participants \n" %(len(self.participants)))
        embed.add_field(name=self.battlePlace.lower(), value=field)

        listParticipant = "@"+str(' @'.join(self.participants))
        embed.set_footer(text=listParticipant)

        return embed

    def ajouterParticipant(self, newParticipant):
        """ajoute des participants au raid
        renvoit 0 si la personne est déjà inscrite
        1 si l'inscripsion est un succès"""
        if self.isParticipant(newParticipant):
            return 0
        else:
            self.participants.append(newParticipant)
            return 1

    def retirerParticipant(self, oldParticipant):
        """retire un participant de la liste
        renvoit 0 si le participant n'est pas dans la liste
        1 si le remove est un succès"""
        if self.isParticipant(oldParticipant):
            self.participants.remove(oldParticipant)
            return 1
        else:
            return 0

    def isParticipant(self, searchParticipant):
        """ renvoit 0 si le participant n'existe pas 1 sinon"""
        for participant in self.participants:
            if participant == searchParticipant:
                return 1
        return 0

    def choisirLaunch(self, battleTime):
        """edite la date de lancement du raid"""
        self.lancement = datetime.datetime.strptime(battleTime, "%H:%M")

    def faireEclore(self, pokeName):
        """eclosion d'un oeuf
        l'utilisateur rensigne le nom du pokémon apparut à l'interieur de l'oeuf. le bot remplace le time de fin par éclosion + temps d'incubation et change le numero du pokemon (return 1)
        il ne fait rien si ce n'est pas un oeuf (return 0)"""
        if not self.isOeuf():
            return 0

        newPokeId = Raid.lirePokeId(pokeName)
        if newPokeId == 0:
            return 0

        self.pokeId = newPokeId
        self.fin = self.eclosion + Raid.temps_presence
        self.eclosion = 0

        return 1



    def isOeuf (self):
        """test si le raid selectionné était un oeuf
        retour 1 si oui
        0 sinon"""
        if self.pokeId < 0:
            return 1
        else:
            return 0

if __name__=="__main__":
    #debut des test unitaires
    print("on effectue les testes unitaires \n")

    if Raid.lirePokeId(-50) != 0:
        print ("FALSE conaissance des bornes des pokémons")
    if Raid.lirePokeId("T2") != -2:
        print ("FALSE lecture des oeufs")
    if Raid.lirePokeId("T20") != 0:
        print ("FALSE connaissance des bornes des oeufs")
    if Raid.lirePokeId("T2T") != 0:
        print ("FALSE lecture d'un mauvais oeuf")
    if Raid.lirePokeId("florizarre") != 3:
        print ("FALSE ne sait pas lire un pokemon")
    if Raid.lirePokeId("blastoise") != 9:
        print("FALSE ne sait pas lire l'anglais")
    if Raid.lirePokeId('RATTAta') != 19:
        print("FALSE tient compte de la casse")
