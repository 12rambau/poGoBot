channelex = {
    "bravoure":     {"fr":  "rouge",    "en":  "red" },
    "intuition":    {"fr":  "jaune",    "en":   "yellow"},
    "sagesse":      {"fr":  "bleu",     "en":   "blue"}
}

def findChannel(color, local):
    """return the name of the channel or 0 if it doesn't exist"""
    for channel, trad in channelex.items():
        if color == trad[local]: return channel
    return 0
