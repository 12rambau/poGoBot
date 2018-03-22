#action a effectuer lors d'une commande dans PogoBotPy
import asyncio
import re

async def updateLevel(lvl, member, bot):
    """ajoute un nouveau nickname à l'utilisateur"""

    regex = re.compile(r"^.* \([0-9]*\)$") #un nick avec un niveau

    nick = member.nick if member.nick else  member.name

    if regex.match(nick):
        newNick = re.sub(r"\([0-9]*\)$", str("(%i)" %(lvl)), nick)
    else:
        newNick = nick + str(" (%i)" %(lvl))

    await bot.change_nickname(member, newNick)

async def updateTeam(team, member, bot, server):
    """change la couleur et lui envoi un petit message ou change la couleur directement"""
    for role in member.roles:
        if role.name.startswith("almost_"): return 0

    previous = False
    old_team = "rien"
    for role in member.roles:
        if teamdex.get(str("%s" %role.name)):
            previous = True
            old_team = role.name
            await bot.remove_roles(member, role)
    if previous:
        await bot.send_message(member, str("Tu vas rejoindre la team %s. Comme tu avais déjà une team, tu vas rester sans rôle pendant 1 heure et l'administrateur a été informé de ce changement." %team))
        await bot.send_message(server.owner, str("<@%s> va passé de la team %s à la team %s" %(member.id, old_team, team )))
        attente = next(r for r in server.roles if r.name == str("almost_%s" %(team)))
        await bot.add_roles(member, attente)
        await asyncio.sleep(3600) #1 heure entière sans rôle
        await client.remove_roles(member, attente)

    await client.add_roles(member, next(r for r in server.roles if r.name == team))

async def updateNick(newNick, member, bot):
    """donne un surnom au joueur en tenant compte du niveau eventuellement renseigner"""
    assert isinstance(member, discord.Member)

    regex = re.compile(r"^.* \([0-9]*\)$") #un nick avec un niveau

    nick = member.nick if member.nick else  member.name

    if regex.match(nick):
        newNick = re.sub(r"^.* \(", str("%s (" %newNick), nick)

    await client.change_nickname(member, newNick)

if __name__=="__main__":
    pass
