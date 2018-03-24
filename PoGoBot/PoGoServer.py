#create and manage the PoGOBot server
import re
import discord
from Entry import Entry
from Raid import Raid
import asyncio

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

        #initialisation des 3 listes de raid
        self.raids = {}
        self.raidsGymHuntr = {}
        self.raidsEx = {}

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
    async def purgeServer(self, bot):
        """nettoie la channel de raid et tous les raids"""
        await bot.purge_from(self.raid)
        await self.purgeRaid(bot)
        await self.purgeRaidEx(bot)
        await self.updateRAidsChannel(bot)

    async def purgeRaid(self, bot):
        """ nettoie le serveur de tous ses raids
        operation réalisée en 2 temps car on ne peut supprimer d'élément d'un dico en cours de parcour"""
        raidChannels=[]
        for channel in self.server.channels:
            if PoGoServer._REGEX_RAID_.match(channel.name): raidChannels.append(channel.id)

        for id in raidChannels:
            await bot.delete_channel(bot.get_channel(id))

    async def purgeRaidEx(self, bot):
        """ajoute les raids encore en cours à la liste des raids ex"""
        raidExChannels=[]
        for channel in self.server.channels:
            if PoGoServer._REGEX_RAID_EX_.match(channel.name): raidExChannels.append(channel.id)

        for id in raidExChannels:
            channel = bot.get_channel(id)
            entry = Entry(next(m for m in await bot.pins_from(channel)), bot)
            if entry.readExRaids(bot, self.server):
                raid = Raid.RaidFromExEmbed(entry.entry)
                self.raidsEx[raid.id] = raid
            else:
                await bot.delete_channel(channel)

    async def updateRAidsChannel(self, bot):
        """read all the actual informations in the Raid channel"""
        #liste des raids Ex
        await bot.send_message(self.raid, "**liste des Raids Ex**")
        for raid in self.raidsEx.values():
            await raid.updateCommunication(bot, self)
        #list des raids GymHuntrBot
        content = "**Vu sur GymHuntr autour de nous :**\n"
        embed = discord.Embed()
        field = ""
        if len(list(self.raidsGymHuntr)) == 0:
            content += "pas de raid en vue, c'est visiblement pas l'heure"
        else:
            for raid in self.raidsGymHuntr.values():
                field += raid.outText()
            embed.add_field(name= "Actualisés", value=field)
        self.msgGymHuntr = await bot.send_message(self.raid, content=content, embed=embed)
        #ecrire le message initiale des raid
        await bot.send_message(self.raid, "**Liste des raids en cours**")
        for raid in self.raids.values():
            raid.updateCommunication(bot, self)
