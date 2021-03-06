import time
import datetime
import re
from data import pokedex
import discord
from utils import *

class Raid:
    """ classe permettant de décrire un raid instancié:
    - id: numero de la salle dans laquelle s'effectue le raid (il ne doit donc pas dépasser 5)
    - pokeId : numero du pokemon (chiffre negatif pour les niveaux d'oeuf)
    - participant[]: tableau des noms des participants
    - lancement: heure de lancement du raid
    - fin: heure de fin du raids
    - eclosion: si c'est un oeuf on met l'heure d'éclosion
    - battlePlace: le lieu du raid"""

    TEMPS_PRESENCE = datetime.timedelta(minutes=45)

    def __init__(self, ex, id, pokeName, capitaine, temps, battlePlace):
        """constructeur parametré permettant de creer un Raid avec tous les paramettres"""

        #pour l'instant je fais confiance à mes utilisateurs
        self.ex = ex
        self.id = id
        self.pokeId = lirePokeName(pokeName)
        self.participants = []
        self.lancement = 0
        self.capitaine = capitaine
        if self.pokeId < 0:
            self.eclosion = temps
            self.fin = self.eclosion + Raid.TEMPS_PRESENCE
        elif self.pokeId > 0:
            self.fin = temps
            self.eclosion = 0
        self.battlePlace = battlePlace

    def embed(self):
        """ Retourne un embed formaté pour être lu par discord"""
        embed = discord.Embed(title=self.getTitre())
        embed.set_thumbnail(url=self.getUrl())

        field = self.getCapitaine("**chef:**")
        field += getTimeStr(self.lancement, "**lancement:**", self.ex)
        if self.pokeId < 0:
            field += getTimeStr(self.eclosion, "**eclosion:**", self.ex)
        else:
            field += getTimeStr(self.fin, "**fin:**", self.ex)
        field += str("**%i participants** \n" %(len(self.participants)))
        embed.add_field(name=self.battlePlace.lower(), value=field)

        embed.set_footer(text=self.getListParticipants())

        return embed

    def ajouterParticipant(self, newParticipant):
        """ajoute des participants au raid
        renvoit 0 si la personne est déjà inscrite
        1 si l'inscripsion est un succès"""
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
        """edite la date de lancement du raid
        renvoit 1 si la date est au bon format 0 sinon"""
        #tester la validité de la date
        self.lancement = battleTime
        return 1

    def faireEclore(self, pokeName):
        """eclosion d'un oeuf
        l'utilisateur rensigne le nom du pokémon apparut à l'interieur de l'oeuf. le bot remplace le time de fin par éclosion + temps d'incubation et change le numero du pokemon (return 1)
        il ne fait rien si ce n'est pas un oeuf (return 0)"""
        if not self.isOeuf(): return 0
        if not isPokemon(pokeName) : return 0

        self.pokeId = lirePokeName(pokeName)
        self.eclosion = 0
        return 1

    def isOeuf (self):
        """test si le raid selectionné était un oeuf
        retour 1 si oui
        0 sinon"""
        return self.pokeId < 0

    def afficherList(self):
        """renvoit une str qui correspond à la ligne du raid dans la liste de raid-list"""
        if self.pokeId < 0:
            message += str("OEUF-%i : " %(self.pokeId))
        else:
            message += str("%s : " %(pokedex[self.pokeId-1]["fr"].upper()))
        message += str("%s " %(self.battlePlace))
        if self.lancement == 0:
            message += "? "
        else:
            message += str("%s " %(self.lancement.strftime("%H:%M")))
        message += str("avec %i personnes \n" %(len(self.participants)))

        return message

    def getUrl(self):
        if self.pokeId > 0:
            url = str("https://pokemon.gameinfo.io/images/pokemon/%i.png" %(self.pokeId))
        elif self.pokeId == -5 or self.pokeId == -6:
            url = "https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2017/06/Pokemon-GO-Legendary-Egg.png"
        elif self.pokeId == -4 or self.pokeId == -3:
            url = "https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2017/06/Pokemon-GO-Rare-Egg-Yellow.png"
        elif self.pokeId == -2 or self.pokeId == -1:
            url = "https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2017/06/Pokemon-GO-Normal-Egg-Pink.png"

        return url

    def getTitre(self):
        if self.pokeId > 0:
            titre = lirePokeId(self.pokeId).upper()
        elif self.pokeId >-6:
            titre = str("T%i" %(-self.pokeId))
        elif self.ex:
            titre = "Tex"
        return titre

    def getCapitaine(self, label):
        if self.capitaine.nick:
            capitaine = str("%s @%s\n" %(label, self.capitaine.nick))
        else:
            capitaine = str("%s @%s\n" %(label, self.capitaine.name))

        return capitaine

    def getListParticipants(self):
        listParticipant = ""
        for participant in self.participants:
            if participant.nick:
                listParticipant += str("@%s" %(participant.nick))
            else:
                listParticipant += str("@%s" %(participant.name))

        return listParticipant

    def setCapitaine(self, member):
        assert isinstance(member, discord.Member)

        self.capitaine = member

    def outText(self):
        """set an standart one line output for the raid"""
        message = str("**%s:** " %self.getTitre().lower())
        message += str("%s " %self.battlePlace)
        if self.pokeId < 0:
            message += getTimeStr(self.eclosion, "**eclosion:**", self.ex)
        elif self.pokeId > 0:
            message += getTimeStr(self.fin, "**fin:**", self.ex)
        message += "\n"
        return message

    def getRaidName(self):
        """return the name to give to the channel used by the raid"""
        name = str("%s_" %self.id)
        name += str("ex_") if self.ex else ""
        name += lirePokeId(self.pokeId)
        name += str("-%i" %len(self.participants))
        return name

if __name__=="__main__":
    #debut des test unitaires
    pass
