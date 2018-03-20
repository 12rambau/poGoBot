commandex = {
    "cookie":   "!cookie",
    "add":      "!add [pokeName]/T[RaidLvl] [heure_de_fin]/[heure_eclosion] [lieu]",
    "lvl":      "!lvl [mon_lvl]",
    "team":     "!team [couleur]",
    "edit":     "!edit [pokeName]",
    "launch":   "!launch [heure de lancement]",
    "in":       "!in OR !in @[user]",
    "out":      "!out OR !out @[user]",
    "nick":     "!nick [new_nickname]",
    "help":     "@[le_nom_du_bot]",
    "chef":     "!chef @[user]",
    "purge":    "!purge",
    "free":     "!free @[user]",
    "add":      "!add ex [datetime_eclosion] [lieu]",
    }

def rappelCommand(commandName):
    """envoi à l'utilisateur un message permettant de reexpliquer la commande"""
    return str("Comme je suis sympa je te redonne la commande que tu as essayé de taper :\n %s" %commandex[commandName])
