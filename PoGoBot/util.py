#action de lecture principalement
def getNumChannel(name):
    """retourne le numero au début du nom d'une channel de raid"""
    assert isinstance(name, str)

    index = name.find("_")
    return int(name[:index])
