#transforme et vérifie que les entrées sont conformes
import asyncio
import discord
import data.commandex

class Entry:

    def __init__(entry, bot):
        self.entry = entry
        self.bot = bot

    async def isLevel(self):
        """change la valeure de l'entry pour correspondre au attente de la commande "lvl". retourne 1 si tout est ok 0 sinon"""
        try:
            assert isinstance(self.entry, discord.message)
            args = self.entry.content.split(" ")
            lvl = args[1]
            assert isinstance(int(lvl), int) and int(lvl) <= 40 and int(lvl) > 0
            self.entry = int(lvl)
            return 1
        except AssertionError:
            await bot.send_message(self.entity.channel, rappelCommand("lvl"))
            return 0

    async def isTeam(self):
        """change la valeur de l'entry pour correspndre au attentes de la commande team return 1 si ça passe 0 sinon"""
        try:
            assert isinstance(self.entry, discord.message)
            args = self.entry.content.split(" ")
            assert len(args) == 2
            self.entity = findChannel(args[1], "fr")
            assert channel
            return 1
        except AssertionError:
            await bot.send_message(self.entity.channel, rappelCommand("team"))
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
            await bot.send_message(self.entity.channel, rappelCommand("nick"))
            return 0


if __name__=="__main__":
    pass
