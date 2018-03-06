class Channel:
    """Classe definissant le contenu en cours des channels de raid:
    - NB_CHANNEL: nombre de channel construites par le bot
    - id: numero du cannal
    - raid: descripsion du raid en cours, si raid = 0 alors c'est vide"""

    nbChannelMax = 5
    NB_CHANNEL = 0

    def __init__(self, id):
        """initialisation d'une channel avec pour seul information son ID, le raid est initialisé à 0"""
        self.raid = 0
        self.id = id
        Channel.NB_CHANNEL += 1

    def ajouterRaid(self, raid):
        """ajoute un raid dans une channel libre
        retourne 1 si l'ajout a marché
        retourn 0 sinon"""
        if self.raid == 0:
            self.raid = raid
            return 1

        return 0

    def retirerRaid(self):
        """retirer le raid en cour dans la channel"""
        if self.raid != 0:
            self.raid = 0
        return 1

    def channelLibre(channels):
        """renvoit le plus petit numero de channel libre pour ajouter un nouveau canal
        renvoit 0 sinon"""
        for channel in channels:
            if channel.raid == 0:
                return channel.id
        return 0

    def isRaid(self):
        """renvoit 1 si un raid est présent 0 sinon"""
        if self.raid == 0:
            return 0
        else:
            return 1
