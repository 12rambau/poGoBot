#transforme et vérifie que les entrées sont conformes
import asyncio
import discord
from data.channeldex import *
from data.pokedex import *
from data.commandex import *
from datetime import datetime, timedelta
import unidecode
#from PoGoServer import PoGoServer

class Entry:

    def __init__(self, entry, bot):
        self.entry = entry
        self.bot = bot

    async def isLevel(self):
        """change la valeure de l'entry pour correspondre au attente de la commande "lvl". retourne 1 si tout est ok 0 sinon"""
        try:
            assert isinstance(self.entry, discord.Message)
            args = self.entry.content.split(" ")
            lvl = args[1]
            assert isinstance(int(lvl), int) and int(lvl) <= 40 and int(lvl) > 0
            self.entry = int(lvl)
            return 1
        except AssertionError:
            await bot.send_message(self.entry.channel, rappelCommand("lvl"))
            return 0

    async def isTeam(self):
        """change la valeur de l'entry pour correspndre au attentes de la commande team return 1 si ça passe 0 sinon"""
        try:
            assert isinstance(self.entry, discord.Message)
            args = self.entry.content.split(" ")
            assert len(args) == 2
            self.entity = findChannel(args[1], "fr")
            assert channel
            return 1
        except AssertionError:
            await bot.send_message(self.entry.channel, rappelCommand("team"))
            return 0

    async def isNick(self):
        """change la commande pour correspondre aux attentes de la commande nick
        return 1 si ça passe 0 sinon"""
        try:
            assert isinstance(self.entry, discord.message)
            args = self.entry.content.split(" ")
            assert len(args) == 2
            self.entity = args[1]
            return 1
        except AssertionError:
            await bot.send_message(self.entry.channel, rappelCommand("nick"))
            return 0

    async def isAddRaid(self, bot, poGoServer):
        """transforme les données de la commande en tuple pour être utilisé par la command add, O sinon"""
        try:
            assert isinstance(self.entry, discord.Message)
            args = self.entry.content.split(" ")
            assert len(args) > 3

            #test the date
            battleTime = Entry.readHour(args[2])
            assert battleTime > datetime.now()

            #test the pokemon name
            assert isPokemon(args[1])
            pokeName = args[1]

            #manipulation lieu
            battlePlace = unidecode.unidecode(u"%s" %(' '.join(args[3:]))).lower()
            assert Entry.IsUniquePlace(battlePlace, poGoServer.raids)

            #on place tout ça dans un tuple
            self.entry = (pokeName, battleTime, battlePlace)
            return 1
        except AssertionError:
            await bot.send_message(self.entry.channel, rappelCommand("add"))
            return 0

    async def isAddRaidEx(self, bot, poGoServer):
        """transforme les données de la commande en tuple pour être utilisé par la command add, O sinon"""

        try:
            assert isinstance(self.entry, discord.Message)
            args = self.entry.content.split(" ")
            assert len(args) > 4

            #test the date
            battleTime = datetime.strptime(str("%s %s" %(args[2], args[3])), "%d/%m/%Y %H:%M")
            assert battleTime > datetime.now()

            #manipulation lieu
            battlePlace = unidecode.unidecode(u"%s" %(' '.join(args[4:]))).lower()
            assert Entry.IsUniquePlace(battlePlace, poGoServer.raidsEx)

            #on place tout ça dans un tuple
            self.entry = ("tex", battleTime, battlePlace)
            return 1
        except (AssertionError, ValueError):
            await bot.send_message(self.entry.channel, rappelCommand("add ex"))
            return 0

    def readExRaids(self, bot, server):
        """retirer les informations du raid depuis l'embed"""
        assert isinstance(self.entry, discord.Message)
        embed = next (e for e in self.entry.embeds)

        pokeName = embed["title"]

        battlePlace = embed["fields"][0]["name"]

        args = embed["fields"][0]["value"].split("\n")
        chef = args[0].replace("**chef:** @", "")
        chef = next(m for m in server.members if (m.name == chef or m.nick == chef) )

        temps = args[2][-16:]
        temps = datetime.strptime(temps, "%d/%m/%Y %H:%M")

        nbParticipant = int(args[3].split(" ")[0].replace("**", ""))
        participants = []
        if nbParticipant > 0:
            footer = embed["footer"]["text"].split("@")
            footer.pop(0)
            for name in footer:
                participants.append(next(m for m in server.members if (m.name == name or m.nick == name)))
        if temps > datetime.now():
            self.entry = (pokeName, chef, temps, battlePlace, participants, self.entry.channel, self.entry)
            return 1
        else:
            return 0

    def readHour(time):
        """return a datetime corresponding to the given time, 0 if not acceptable"""
        try:
            #assert isinstance(time, str)
            now = datetime.now()
            time = datetime.strptime(time, "%H:%M")
            return datetime(year = now.year, month= now.month, day=now.day, hour= time.hour, minute=time.minute)
        except ValueError:
            return 0

    def IsUniquePlace(place, dic):
        """renvoit 1 si le raid n'existe pas dans le dictionnaire, 0 sinon"""
        try:
            raid = next(r for r in dic.values() if r.battlePlace == place)
            return 0
        except StopIteration:
            return 1
if __name__=="__main__":
    pass
