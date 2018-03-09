from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import os

client = commands.Bot(command_prefix = "?")

@client.event
async def on_ready():
    print("je teste la connexion")
    await asyncio.sleep(30)
    print("j'ai finit d'attendre")
    await client.logout()

client.run(os.environ['DISCORD_TOKEN'])
