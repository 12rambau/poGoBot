#action a effectuer lors d'une commande dans PogoBotPy
import asyncio
import re

async def addLevel(lvl, member, bot):
    """ajoute un nouveau nickname à l'utilisateur"""

    regex = re.compile(r"^.* \([0-9]*\)$") #un nick avec un niveau

    nick = member.nick if member.nick else  member.name

    if regex.match(nick):
        newNick = re.sub(r"\([0-9]*\)$", str("(%i)" %(lvl)), nick)
    else:
        newNick = nick + str(" (%i)" %(lvl))

    await bot.change_nickname(member, newNick)
