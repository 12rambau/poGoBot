from PoGoBot import *
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix = "?")

async def timerLogout():
    await asyncio.sleep(30)
    await client.logout()

client.run(os.environ['DISCORD_TOKEN'])
