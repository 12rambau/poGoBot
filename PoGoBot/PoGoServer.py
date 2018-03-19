#create and manage the PoGOBot server
import re

class PoGoServer:

    _REGEX_RAID_ = re.compile(r"[0-9]*_[a-z0-9]*-[0-9]*")
    _REGEX_RAID_EX = re.compile(r"[0-9]*_ex_[a-z0-9]*-[0-9]*")

    def __init__(self, server):

        #initialisation du compteur de cookie
        self.cookieCompteur = 0

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
