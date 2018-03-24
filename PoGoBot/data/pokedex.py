import re

pokedex = [
    {"fr":  "bulbizarre",   "en":   "bulbazaur"},
    {"fr":  "herbizarre",   "en":   "ivysaur"},
    {"fr":  "florizarre",   "en":   "venusaur"},
    {"fr":  "salameche",    "en":   "charmander"},
    {"fr":  "reptincel",    "en":   "chameleon"},
    {"fr":  "dracaufeu",    "en":   "charizard"},
    {"fr":  "carapuce",     "en":   "squirtle"},
    {"fr":  "carabaffe",    "en":   "wartortle"},
    {"fr":  "tortank",      "en":   "blastoise"},
    {"fr":  "chenipan",     "en":   "caterpie"},
    {"fr":  "chrysacier",   "en":   "metapod"},
    {"fr":  "papilusion",   "en":   "butterfree"},
    {"fr":  "aspicot",      "en":   "weedle"},
    {"fr":  "coconfort",    "en":   "kakuna"},
    {"fr":  "dardagnan",    "en":   "beedrill"},
    {"fr":  "roucool",      "en":   "pidgey"},
    {"fr":  "roucoups",     "en":   "pidgeotto"},
    {"fr":  "roucarnage",   "en":   "pidgeot"},
    {"fr":  "rattata",      "en":   "rattata"},
    {"fr":  "rattatac",     "en":   "raticate"},
    {"fr":  "piafabec",     "en":   "spearow"},
    {"fr":  "rapasdepic",   "en":   "fearow"},
    {"fr":  "abo",          "en":   "ekans"},
    {"fr":  "arbok",        "en":   "arbok"},
    {"fr":  "pikachu",      "en":   "pikachu"},
    {"fr":  "raichu",       "en":   "raichu"},
    {"fr":  "sabelette",    "en":   "sandshrew"},
    {"fr":  "sablaireau",   "en":   "sandslash"},
    {"fr":  "nidoran",      "en":   "nidoran"},
    {"fr":  "nidorina",     "en":   "nidorina"},
    {"fr":  "nidoqueen",    "en":   "nidoqueen"},
    {"fr":  "nidoran",      "en":   "nidoran"},
    {"fr":  "nidorino",     "en":   "nidorino"},
    {"fr":  "nidoking",     "en":   "nidoking"},
    {"fr":  "melofee",      "en":   "clefairy"},
    {"fr":  "melodelfe",    "en":   "clefable"},
    {"fr":  "goupix",       "en":   "vulpix"},
    {"fr":  "feunard",      "en":   "ninetales"},
    {"fr":  "rondoudou",    "en":   "jigglypuff"},
    {"fr":  "grodoudou",    "en":   "wigglytuff"},
    {"fr":  "nosferapti",   "en":   "zubat"},
    {"fr":  "nosferalto",   "en":   "golbat"},
    {"fr":  "mystherbe",    "en":   "oddish"},
    {"fr":  "ortide",       "en":   "gloom"},
    {"fr":  "rafflesia",    "en":   "vileplume"},
    {"fr":  "paras",        "en":   "paras"},
    {"fr":  "parasect",     "en":   "parasect"},
    {"fr":  "mimitoss",     "en":   "venonat"},
    {"fr":  "aeromite",     "en":   "venomoth"},
    {"fr":  "taupiqueur",   "en":   "diglett"},
    {"fr":  "triopiqueur",  "en":   "dugtrio"},
    {"fr":  "miaouss",      "en":   "meowth"},
    {"fr":  "persian",      "en":   "persian"},
    {"fr":  "psykokwak",    "en":   "psyduck"},
    {"fr":  "akwakwak",     "en":   "golduck"},
    {"fr":  "ferosinge",    "en":   "mankey"},
    {"fr":  "colossinge",   "en":   "primeape"},
    {"fr":  "caninos",      "en":   "growlithe"},
    {"fr":  "arcanin",      "en":   "arcanine"},
    {"fr":  "ptitard",      "en":   "poliwag"},
    {"fr":  "tetarte",      "en":   "poliwhirl"},
    {"fr":  "tartard",      "en":   "poliwrath"},
    {"fr":  "abra",         "en":   "abra"},
    {"fr":  "kadabra",      "en":   "kadabra"},
    {"fr":  "alakasam",     "en":   "alakasam"},
    {"fr":  "machoc",       "en":   "machop"},
    {"fr":  "machopeur",    "en":   "machoke"},
    {"fr":  "mackogneur",   "en":   "machamp"},
    {"fr":  "chetiflor",    "en":   "belsprout"},
    {"fr":  "boustiflor",   "en":   "weepinebell"},
    {"fr":  "empiflor",     "en":   "victreebel"},
    {"fr":  "tentacool",    "en":   "tentacool"},
    {"fr":  "tentacruel",   "en":   "tentacruel"},
    {"fr":  "racaillou",    "en":   "geodude"},
    {"fr":  "gravalanch",   "en":   "graveler"},
    {"fr":  "grolem",       "en":   "golem"},
    {"fr":  "ponyta",       "en":   "ponyta"},
    {"fr":  "galopa",       "en":   "rapidash"},
    {"fr":  "ramoloss",     "en":   "slowpoke"},
    {"fr":  "flagadoss",    "en":   "slowbro"},
    {"fr":  "magneti",      "en":   "magnemite"},
    {"fr":  "magneton",     "en":   "magneton"},
    {"fr":  "canartichaud", "en":   "farfetch'd"},
    {"fr":  "doduo",        "en":   "doduo"},
    {"fr":  "dodrio",       "en":   "dodrio"},
    {"fr":  "otaria",       "en":   "seel"},
    {"fr":  "lamantine",    "en":   "dewgong"},
    {"fr":  "tadmorv",      "en":   "grimer"},
    {"fr":  "grotadmorv",   "en":   "muk"},
    {"fr":  "kokiyas",      "en":   "shellder"},
    {"fr":  "crustabri",    "en":   "cloyster"},
    {"fr":  "fantominus",   "en":   "gastly"},
    {"fr":  "spectrum",     "en":   "haunter"},
    {"fr":  "ectoplasma",   "en":   "gengar"},
    {"fr":  "onix",         "en":   "onix"},
    {"fr":  "soporifik",    "en":   "drowzee"},
    {"fr":  "hypnomade",    "en":   "hypno"},
    {"fr":  "krabby",       "en":   "krabby"},
    {"fr":  "krabboss",     "en":   "kingler"},
    {"fr":  "voltorbe",     "en":   "voltorb"},
    {"fr":  "electrode",    "en":   "electrode"},
    {"fr":  "noeunoeuf",    "en":   "exeggcute"},
    {"fr":  "noadkoko",     "en":   "exeggutor"},
    {"fr":  "osselait",     "en":   "cubone"},
    {"fr":  "ossatueur",    "en":   "marowak"},
    {"fr":  "kicklee",      "en":   "hitmonlee"},
    {"fr":  "tygnon",       "en":   "hitmonchan"},
    {"fr":  "excelangue",   "en":   "lickitung"},
    {"fr":  "smogo",        "en":   "koffing"},
    {"fr":  "smogogo",      "en":   "weezing"},
    {"fr":  "rhinocorne",   "en":   "rhyhorn"},
    {"fr":  "rhinoferos",   "en":   "rhydon"},
    {"fr":  "leveinard",    "en":   "chansey"},
    {"fr":  "saquedeneu",   "en":   "tangela"},
    {"fr":  "kangourex",    "en":   "kangaskhan"},
    {"fr":  "hypotrempe",   "en":   "horsea"},
    {"fr":  "hypocean",     "en":   "seadra"},
    {"fr":  "poissirene",   "en":   "goldeen"},
    {"fr":  "poissoroy",    "en":   "seaking"},
    {"fr":  "stari",        "en":   "staryu"},
    {"fr":  "staross",      "en":   "starmie"},
    {"fr":  "M. Mime",      "en":   "Mr. Mime"},
    {"fr":  "insecateur",   "en":   "scyther"},
    {"fr":  "lippoutou",    "en":   "jynx"},
    {"fr":  "elektek",      "en":   "electabuzz"},
    {"fr":  "magmar",       "en":   "magmar"},
    {"fr":  "scarabrute",   "en":   "pinsir"},
    {"fr":  "tauros",       "en":   "tauros"},
    {"fr":  "magicarpe",    "en":   "magikarp"},
    {"fr":  "leviator",     "en":   "gyarados"},
    {"fr":  "lokhlass",     "en":   "laprass"},
    {"fr":  "metamorph",    "en":   "ditto"},
    {"fr":  "evoli",        "en":   "eevee"},
    {"fr":  "aquali",       "en":   "vaporeon"},
    {"fr":  "voltali",      "en":   "jolteon"},
    {"fr":  "pyroli",       "en":   "flareon"},
    {"fr":  "porygon",      "en":   "porygon"},
    {"fr":  "amonita",      "en":   "omanyte"},
    {"fr":  "amonistar",    "en":   "omastar"},
    {"fr":  "kabuto",       "en":   "kabuto"},
    {"fr":  "kabutops",     "en":   "kabutops"},
    {"fr":  "ptera",        "en":   "ptera"},
    {"fr":  "ronflex",      "en":   "snorlax"},
    {"fr":  "artikodin",    "en":   "articuno"},
    {"fr":  "electhor",     "en":   "zapdos"},
    {"fr":  "sulfura",      "en":   "moltres"},
    {"fr":  "minidraco",    "en":   "dratini"},
    {"fr":  "draco",        "en":   "dragonair"},
    {"fr":  "dracolosse",   "en":   "dragonite"},
    {"fr":  "mewtwo",       "en":   "mewtwo"},
    {"fr":  "mew",          "en":   "mews"},
    {"fr":  "germignon",    "en":   "chikorita"},
    {"fr":  "macronium",    "en":   "bayleef"},
    {"fr":  "meganium",     "en":   "meganium"},
    {"fr":  "hericendre",   "en":   "cyndaquil"},
    {"fr":  "feurisson",    "en":   "quilava"},
    {"fr":  "typhlosion",   "en":   "typhlosion"},
    {"fr":  "kaiminus",     "en":   "totodile"},
    {"fr":  "crocodil",     "en":   "croconaw"},
    {"fr":  "aligatueur",   "en":   "feraligatr"},
    {"fr":  "fouinette",    "en":   "sentrel"},
    {"fr":  "fouinar",      "en":   "furret"},
    {"fr":  "hoothoot",     "en":   "hoothoot"},
    {"fr":  "noarfang",     "en":   "noctowl"},
    {"fr":  "coxy",         "en":   "ledyba"},
    {"fr":  "coxyclaque",   "en":   "ledian"},
    {"fr":  "mimigal",      "en":   "spinarak"},
    {"fr":  "migalos",      "en":   "ariados"},
    {"fr":  "nostenfer",    "en":   "crobat"},
    {"fr":  "loupio",       "en":   "chinchou"},
    {"fr":  "lanturn",      "en":   "lanturn"},
    {"fr":  "pichu",        "en":   "pichu"},
    {"fr":  "melo",         "en":   "cleffa"},
    {"fr":  "toudoudou",    "en":   "igglybuff"},
    {"fr":  "togepi",       "en":   "togepi"},
    {"fr":  "togetic",      "en":   "togetic"},
    {"fr":  "natu",         "en":   "natu"},
    {"fr":  "xatu",         "en":   "xatu"},
    {"fr":  "wattouat",     "en":   "mareep"},
    {"fr":  "lainergie",    "en":   "flaaffy"},
    {"fr":  "pharamp",      "en":   "ampharos"},
    {"fr":  "joliflor",     "en":   "bellossom"},
    {"fr":  "marill",       "en":   "marill"},
    {"fr":  "azumarill",    "en":   "azumarill"},
    {"fr":  "simularbre",   "en":   "sudowoodo"},
    {"fr":  "tarpaud",      "en":   "politoed"},
    {"fr":  "granivol",     "en":   "hoppip"},
    {"fr":  "floravol",     "en":   "skiploom"},
    {"fr":  "cotovol",      "en":   "jumpluff"},
    {"fr":  "capumain",     "en":   "aipom"},
    {"fr":  "tournegrin",   "en":   "sunkern"},
    {"fr":  "heliatronc",   "en":   "sunflora"},
    {"fr":  "yanma",        "en":   "yanma"},
    {"fr":  "axoloto",      "en":   "wooper"},
    {"fr":  "maraiste",     "en":   "quagsire"},
    {"fr":  "mentali",      "en":   "espeon"},
    {"fr":  "noctali",      "en":   "umbreon"},
    {"fr":  "cornebre",     "en":   "murkrow"},
    {"fr":  "roigada",      "en":   "slowking"},
    {"fr":  "feuforeve",    "en":   "misdreavus"},
    {"fr":  "zarbi",        "en":   "unown"},
    {"fr":  "qulbutoke",    "en":   "wobbuffet"},
    {"fr":  "girafarig",    "en":   "girafarig"},
    {"fr":  "pomdepik",     "en":   "pineco"},
    {"fr":  "foretress",    "en":   "forretress"},
    {"fr":  "insolourdo",   "en":   "dunesparce"},
    {"fr":  "scorplane",    "en":   "gligar"},
    {"fr":  "steelix",      "en":   "steelix"},
    {"fr":  "snubbull",     "en":   "snubbull"},
    {"fr":  "granbull",     "en":   "granbull"},
    {"fr":  "qwilfish",     "en":   "qwilfish"},
    {"fr":  "cizayox",      "en":   "scizor"},
    {"fr":  "caratroc",     "en":   "shuckle"},
    {"fr":  "scarhino",     "en":   "heracross"},
    {"fr":  "farfuret",     "en":   "sneasel"},
    {"fr":  "teddiursa",    "en":   "teddiursa"},
    {"fr":  "ursaring",     "en":   "ursaring"},
    {"fr":  "limagma",      "en":   "slugma"},
    {"fr":  "volcaropod",   "en":   "magcargo"},
    {"fr":  "marcacrin",    "en":   "swinub"},
    {"fr":  "cochignon",   "en":   "piloswine"},
    {"fr":  "corayon",      "en":   "corsola"},
    {"fr":  "remoraid",     "en":   "remoraid"},
    {"fr":  "octillery",    "en":   "octillery"},
    {"fr":  "cadoizo",      "en":   "delibird"},
    {"fr":  "demanta",      "en":   "mantine"},
    {"fr":  "airmure",      "en":   "skarmory"},
    {"fr":  "malosse",      "en":   "houndour"},
    {"fr":  "demolosse",    "en":   "houndoom"},
    {"fr":  "hyporoi",      "en":   "kingdra"},
    {"fr":  "phanpy",       "en":   "phanpy"},
    {"fr":  "donphan",      "en":   "donphan"},
    {"fr":  "porygon2",     "en":   "porygon2"},
    {"fr":  "cerfrousse",   "en":   "stantler"},
    {"fr":  "queuloriol",   "en":   "smeargle"},
    {"fr":  "debugant",     "en":   "tyrogue"},
    {"fr":  "kapoera",      "en":   "hitmontop"},
    {"fr":  "lippouti",     "en":   "smoochum"},
    {"fr":  "elekid",       "en":   "elekid"},
    {"fr":  "magby",        "en":   "magby"},
    {"fr":  "ecremeuh",     "en":   "miltank"},
    {"fr":  "leuphorie",    "en":   "blissey"},
    {"fr":  "raikou",       "en":   "raikou"},
    {"fr":  "entei",        "en":   "entei"},
    {"fr":  "suicune",      "en":   "suicune"},
    {"fr":  "embrilex",     "en":   "larvitar"},
    {"fr":  "ymphect",      "en":   "pupitar"},
    {"fr":  "tyranocif",    "en":   "tyranitar"},
    {"fr":  "lugia",        "en":   "lugia"},
    {"fr":  "ho-oh",        "en":   "ho-oh"},
    {"fr":  "celebi",       "en":   "celebi"},
    {"fr":  "arcko",        "en":   "treecko"},
    {"fr":  "massko",       "en":   "grovyle"},
    {"fr":  "jungko",       "en":   "sceptile"},
    {"fr":  "poussifeu",    "en":   "torchic"},
    {"fr":  "galifeu",      "en":   "combusken"},
    {"fr":  "braségali",    "en":   "blaziken"},
    {"fr":  "gobou",        "en":   "mudkip"},
    {"fr":  "flobio",       "en":   "marshtomp"},
    {"fr":  "laggron",      "en":   "swampert"},
    {"fr":  "medhyena",     "en":   "poochyena"},
    {"fr":  "grahyena",     "en":   "mightyena"},
    {"fr":  "zigzaton",     "en":   "zigzagoon"},
    {"fr":  "lineon",       "en":   "linoone"},
    {"fr":  "chenipotte",   "en":   "wurmple"},
    {"fr":  "armulys",      "en":   "silcoon"},
    {"fr":  "charmillon",   "en":   "beautifly"},
    {"fr":  "blindalys",    "en":   "cascoon"},
    {"fr":  "papinox",      "en":   "dustox"},
    {"fr":  "nenupiot",     "en":   "lotad"},
    {"fr":  "lombre",       "en":   "lombre"},
    {"fr":  "ludicolo",     "en":   "ludicolo"},
    {"fr":  "grainipiot",   "en":   "seedot"},
    {"fr":  "pifeuil",      "en":   "nuzleaf"},
    {"fr":  "tengalice",    "en":   "shiftry"},
    {"fr":  "nirondelle",   "en":   "taillow"},
    {"fr":  "heledelle",    "en":   "swellow"},
    {"fr":  "goelise",      "en":   "wingull"},
    {"fr":  "bekipan",      "en":   "pelipper"},
    {"fr":  "tarsal",       "en":   "ralts"},
    {"fr":  "kirlia",       "en":   "kirlia"},
    {"fr":  "gardevoir",    "en":   "gardevoir"},
    {"fr":  "arakdo",       "en":   "surskit"},
    {"fr":  "maskadra",     "en":   "masquerain"},
    {"fr":  "balignon",     "en":   "shroomish"},
    {"fr":  "chapignon",    "en":   "breloom"},
    {"fr":  "parecool",     "en":   "slakoth"},
    {"fr":  "vigoroth",     "en":   "vigoroth"},
    {"fr":  "monaflemit",   "en":   "slaking"},
    {"fr":  "ningale",      "en":   "nincada"},
    {"fr":  "ninjask",      "en":   "ninjask"},
    {"fr":  "munja",        "en":   "shedinja"},
    {"fr":  "chuchmur",     "en":   "whismur"},
    {"fr":  "ramboum",      "en":   "loudred"},
    {"fr":  "brouhabam",    "en":   "exploud"},
    {"fr":  "makuhita",     "en":   "makuhita"},
    {"fr":  "hariyama",     "en":   "hariyama"},
    {"fr":  "azurill",      "en":   "azurill"},
    {"fr":  "tarinor",      "en":   "nosepass"},
    {"fr":  "skitty",       "en":   "skitty"},
    {"fr":  "delcatty",     "en":   "delcatty"},
    {"fr":  "ténéfix",      "en":   "sableye"},
    {"fr":  "mysdibule",    "en":   "mawile"},
    {"fr":  "galekid",      "en":   "aron"},
    {"fr":  "galegon",      "en":   "lairon"},
    {"fr":  "galeking",     "en":   "aggron"},
    {"fr":  "meditikka",    "en":   "meditite"},
    {"fr":  "charmina",     "en":   "medicham"},
    {"fr":  "dynavolt",     "en":   "electrike"},
    {"fr":  "elecsprint",   "en":   "manectric"},
    {"fr":  "posipi",       "en":   "plusle"},
    {"fr":  "negapi",       "en":   "minun"},
    {"fr":  "muciole",      "en":   "volbeat"},
    {"fr":  "lumivole",     "en":   "illumise"},
    {"fr":  "roselia",      "en":   "roselia"},
    {"fr":  "gloupti",      "en":   "gulpin"},
    {"fr":  "avaltout",     "en":   "swalot"},
    {"fr":  "carvanha",     "en":   "carvanha"},
    {"fr":  "sharpedo",     "en":   "sharpedo"},
    {"fr":  "wailmer",      "en":   "wailmer"},
    {"fr":  "wailord",      "en":   "wailord"},
    {"fr":  "chamallot",    "en":   "numel"},
    {"fr":  "camerupt",     "en":   "camerupt"},
    {"fr":  "chartor",      "en":   "torkoal"},
    {"fr":  "spoink",       "en":   "spoink"},
    {"fr":  "groret",       "en":   "grumpig"},
    {"fr":  "spinda",       "en":   "spinda"},
    {"fr":  "kraknoix",     "en":   "trapinch"},
    {"fr":  "vibraninf",    "en":   "vibrava"},
    {"fr":  "libégon",      "en":   "flygon"},
    {"fr":  "cacnea",       "en":   "cacnea"},
    {"fr":  "cacturne",     "en":   "cacturne"},
    {"fr":  "tylton",       "en":   "swablu"},
    {"fr":  "altaria",      "en":   "altaria"},
    {"fr":  "mangriff",     "en":   "zangoose"},
    {"fr":  "seviper",      "en":   "seviper"},
    {"fr":  "seleroc",      "en":   "lunatone"},
    {"fr":  "solaroc",      "en":   "solrock"},
    {"fr":  "barloche",     "en":   "barboach"},
    {"fr":  "barbicha",     "en":   "whiscash"},
    {"fr":  "ecrapince",    "en":   "corphish"},
    {"fr":  "colhomard",    "en":   "crawdaunt"},
    {"fr":  "balbuto",      "en":   "baltoy"},
    {"fr":  "kaorine",      "en":   "claydol"},
    {"fr":  "lilia",        "en":   "lileep"},
    {"fr":  "vacilys",      "en":   "cradily"},
    {"fr":  "anorith",      "en":   "anorith"},
    {"fr":  "armaldo",      "en":   "armaldo"},
    {"fr":  "barpau",       "en":   "feebas"},
    {"fr":  "milobellus",   "en":   "milotic"},
    {"fr":  "morpheo",      "en":   "castform"},
    {"fr":  "kecleon",      "en":   "kecleon"},
    {"fr":  "polichombr",   "en":   "shuppet"},
    {"fr":  "branette",     "en":   "banette"},
    {"fr":  "skelenox",     "en":   "duskull"},
    {"fr":  "teraclope",    "en":   "dusclops"},
    {"fr":  "tropius",      "en":   "tropius"},
    {"fr":  "eoko",         "en":   "chimecho"},
    {"fr":  "absol",        "en":   "absol"},
    {"fr":  "okeoke",       "en":   "wynaut"},
    {"fr":  "stalgamin",    "en":   "snorunt"},
    {"fr":  "oniglali",     "en":   "glalie"},
    {"fr":  "obalie",       "en":   "spheal"},
    {"fr":  "phogleur",     "en":   "sealeo"},
    {"fr":  "kaimorse",     "en":   "walrein"},
    {"fr":  "coquiperl",    "en":   "clamperl"},
    {"fr":  "serpang",      "en":   "huntail"},
    {"fr":  "rosabyss",     "en":   "gorebyss"},
    {"fr":  "relicanth",    "en":   "relicanth"},
    {"fr":  "lovdisc",      "en":   "luvdisc"},
    {"fr":  "draby",        "en":   "bagon"},
    {"fr":  "drackhaus",    "en":   "shelgon"},
    {"fr":  "drattak",      "en":   "salamence"},
    {"fr":  "terhal",       "en":   "beldum"},
    {"fr":  "metang",       "en":   "metang"},
    {"fr":  "metalosse",    "en":   "metagross"},
    {"fr":  "regirock",     "en":   "regirock"},
    {"fr":  "regice",       "en":   "regice"},
    {"fr":  "registeel",    "en":   "registeel"},
    {"fr":  "latias",       "en":   "latias"},
    {"fr":  "latios",       "en":   "latios"},
    {"fr":  "kyogre",       "en":   "kyogre"},
    {"fr":  "groudon",      "en":   "groudon"},
    {"fr":  "rayquaza",     "en":   "rayquaza"},
    {"fr":  "jirachi",      "en":   "jirachi"},
    {"fr":  "deoxys",       "en":   "deoxys"},
]

def isPokemon(pokeName):
    """renvoit le pokename si c'est formaté comme un nom de pokemon 0 sinon"""
    RegexOeuf = re.compile(r"t[0-9]")
    if RegexOeuf.match(str(pokeName)):
        lvl = int(pokeName.replace("t",""))
        if lvl < 6 and lvl > 0: return pokeName
    else:
        for ip, pokemon in enumerate(pokedex):
            for nom in pokemon.values():
                if nom == pokeName: return pokeName
    return 0

def lirePokeName(pokeName):
    """retourn le numero du pokemon ou de l'oeuf (-1 à -6) retourn 0 sinon"""
    RegexOeuf = re.compile(r"t[0-9]")
    if RegexOeuf.match(str(pokeName)):
        num = pokeName[1:]
        if int(num):
            num = int(num)
            if num < 6 and num > 0: return -num
    elif pokeName.lower() == "tex":
        return -6
    else:
        for ip, pokemon in enumerate(pokedex):
            for nom in pokemon.values():
                if nom == str(pokeName).lower(): return ip+1

    return 0

def lirePokeId(pokeId):
    """retourn le nom de l'oeuf ou du pokemon, 0 sinon"""
    if pokeId < 0:
        return str("T%i" %(-pokeId))
    elif pokeId > 0 and pokeId < len(pokedex):
        return pokedex[pokeId-1]["fr"]
    return 0

if __name__=="__main__":
    #debut des test unitaires
    pass