#create and manage the PoGOBot server
import re
import discord

class PoGoServer:

    _REGEX_RAID_ = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*")
    _REGEX_RAID_EX_ = re.compile(r"[0-9]*_ex_[a-z0-9]*-[0-9]*")

    def __init__(self, server):
        #initialisation du server
        self.server = server
        
        #initialisation du compteur de cookie
        self.cookie = 0

        #initialisation du msgGymHuntr
        #il sert a stocker les informtions données par le GymHuntrBot
        self.msgGymHuntr = 0

        #initialisation des 3 dicionnaires de raid
        self.Raids = {}
        self.RaidsGymHuntr = {}
        self.RaidsEx = {}

        #initialisation des chaines du server
        for channel in server.channels:
            if channel.name.lower() == "accueil":
                self.accueil = channel
                print ("accueil trouvé")
            elif channel.name.lower() == "raid":
                self.raid = channel
                print ("raid trouvé")
            elif channel.name.lower() == "admin":
                self.admin = channel
                print("admin trouvé")

    def isAble(member):
        """renvoit 1 si le user est able 0 sinon"""
        assert isinstance(member, discord.Member)

        for role in member.roles:
            if role.name == "disable": return 0

        return 1

    def addCookie(self):
        """rajoute un cookie"""
        self.cookie += 1
        return self.cookie
