# fichier de lancement du poGoBot
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import os
from PoGoServer import PoGoServer

Client = discord.Client()
bot = commands.Bot(command_prefix = "")

#routine demarage
@bot.event
async def on_ready():

    #recuperer le server
    poGoServer = PoGoServer(bot.get_server(os.environ["DISCORD_SERVER_ID"]))

bot.run(os.environ['DISCORD_TOKEN'])
