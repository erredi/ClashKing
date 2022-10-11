
def emojiDictionary(emojiName):
    switcher = {
        "Barbarian King": "<:BarbarianKing:701626158181122210>",
        "Archer Queen": "<:ArcherQueen:701626158487175270>",
        "Grand Warden": "<:GrandWarden:701933765450268672>",
        "Royal Champion": "<:RoyalChampion:701933810648088606>",
        "Archer": "<:Archer:701626909498409040>",
        "Baby Dragon": "<:BabyDragon:701626909586358364>",
        "Barbarian": "<:Barbarian:701626910207115274>",
        "Bowler": "<:Bowler:701626910614093844>",
        "Electro Dragon": "<:ElectroDragon:701626910735728672>",
        "Dragon": "<:Dragon:701626910752374804>",
        "Dragon Rider": "<:dragon_rider:855686522653114399>",
        "Balloon": "<:Balloon:701626912241352745>",
        "Ice Golem": "<:IceGolem:701626913701101668>",
        "Miner": "<:Miner:701626913793245255>",
        "Hog Rider": "<:HogRider:701626914506276895>",
        "Yeti": "<:Yeti:701626914816655431>",
        "Wizard": "<:Wizard:701626914841821186>",
        "Healer": "<:Healer:701626914930163783>",
        "Giant": "<:Giant:701626915026370671>",
        "Goblin": "<:Goblin:701626915165044828>",
        "Witch": "<:Witch:701626915173433385>",
        "Minion": "<:Minion:701626915311583294>",
        "P.E.K.K.A": "<:PEKKA:701626915328491610>",
        "Wall Breaker": "<:WallBreaker:701626915357982742>",
        "Golem": "<:Golem:701626915395600394>",
        "Lava Hound": "<:LavaHound:701626915479355483>",
        "Valkyrie": "<:Valkyrie:701626915680681994>",
        "Headhunter": "<:Headhunter:742121658386481262>",
        "Super Wall Breaker" : "<:SuperWallBreaker:701626916133666896>",
        "Super Barbarian": "<:SuperBarbarian:701626916087529673>",
        "Super Archer": "<:SuperArcher:750010593045643355>",
        "Super Giant": "<:SuperGiant:701626915902980197>",
        "Sneaky Goblin": "<:SneakyGoblin:701626916129734787>",
        "Rocket Balloon": "<:RocketBalloon:854368171682431006>",
        "Super Wizard": "<:SuperWizard:785536616864153610>",
        "Inferno Dragon": "<:InfernoDragon:742121658386743366>",
        "Super Minion": "<:SuperMinion:771375748916576286>",
        "Super Valkyrie": "<:SuperValkyrie:771375748815519825>",
        "Super Witch": "<:SuperWitch:742121660324511818>",
        "Ice Hound": "<:IceHound:785539963068481546>",
        "Super Dragon" : "<:SuperDragon:918876075809964072>",
        "Super Bowler" : "<:SuperBowler:892035736168185876>",
        "Unicorn": "<:Unicorn:830510531483795516>",
        "Mighty Yak": "<:MightyYak:830510531222962278>",
        "Electro Owl": "<:ElectroOwl:830511434269982790>",
        "L.A.S.S.I":"<:LASSI:830510531168829521>",
        "trophy": "<:trophyy:849144172698402817>",
        "Wall Wrecker": "<:WallWrecker:701628825142034482>",
        "Battle Blimp": "<:BattleBlimp:701628824395317328>",
        "Stone Slammer":  "<:StoneSlammer:701628824688918588>",
        "Siege Barracks":"<:SiegeBarracks:701628824651169913>",
        "Log Launcher":"<:LogLauncher:785540240358113312>",
        "Flame Flinger" : "<:FlameFlinger:918875579904847873>",
        "Skeleton Spell": "<:skel:652161148241707029>",
        "Rage Spell": "<:rs:665562307606347822>",
        "Poison Spell": "<:ps:652161145582387210>",
        "Healing Spell": "<:hs:652161148057026580>",
        "Invisibility Spell": "<:invi:785474117414551582>",
        "Jump Spell": "<:js:652161148032122897>",
        "Lightning Spell": "<:ls:726648294461407441>",
        "Haste Spell": "<:haste:652161145125470208>",
        "Freeze Spell": "<:fs:652161149193682974>",
        "Earthquake Spell": "<:es:652161143975968798>",
        "Bat Spell": "<:bat:652161147679670301>",
        "Clone Spell": "<:cs:652161148958801920>",
        "clan castle" : "<:clan_castle:855688168816377857>",
        "shield" : "<:clash:855491735488036904>",
        "Electro Titan" : "<:ElectroTitan:1029213693021519963>",
        "Battle Drill" : "<:BattleDrill:1029199490038628442>",
        "Recall Spell" : "<:recall:1029199491385012304>",
        "Frosty" : "<:Frosty:1029199487849201785>",
        "Poison Lizard" : "<:PoisonLizard:1029199485450068029>",
        "Phoenix" : "<:Phoenix:1029199486347661343>",
        "Diggy" : "<:Diggy:1029199488906170428>",
        2: "<:02:701579364483203133>",
        3: "<:03:701579364600643634>",
        4: "<:04:701579365850284092>",
        5 : "<:05:701579365581848616>",
        6 : "<:06:701579365573459988>",
        7 : "<:07:701579365598756874>",
        8 : "<:08:701579365321801809>",
        9 : "<:09:701579365389041767>",
        10 : "<:10:701579365661671464>",
        11 : "<:11:701579365699551293>",
        12 : "<:12:701579365162418188>",
        13 : "<:132:704082689816395787>",
        14 : "<:14:828991721181806623>",
        15: "<:th15:1028905841589506099>",
        "Capital Gold" : "<:capitalgold:987861320286216223>"

    }

    emoji = switcher.get(emojiName, None)
    return emoji

def legend_emojis(emojiName):
    switcher = {
        "legends_shield" : "<:legends:881450752109850635>",
        "sword" : "<:sword:825589136026501160>",
        "shield" : "<:clash:877681427129458739>",
        "Previous Days" : "<:cal:989351376146530304>",
        "Legends Overview" : "<:list:989351376796680213>",
        "Graph & Stats" : "<:graph:989351375349624832>",
        "Legends History" : "<:history:989351374087151617>",
        "quick_check" : "<:plusminus:989351373608980490>",
        "gear" : "<:gear:989351372711399504>",
        "pin" : "<:magnify:944914253171810384>",
        "back" : "<:back_arrow:989399022156525650>",
        "forward" : "<:forward_arrow:989399021602877470>",
        "print" : "<:print:989400875766251581>",
        "refresh" : "<:refresh:989399023087652864>",
        "trashcan" : "<:trashcan:989534332425232464>",
        "alphabet" : "<:alphabet:989649421564280872>",
        "start" : "<:start:989649420742176818>",
        "blueshield" : "<:blueshield:989649418665996321>",
        "bluesword" : "<:bluesword:989649419878166558>",
        "bluetrophy" : "<:bluetrophy:989649417760018483>",
        6: "<:06:701579365573459988>",
        7: "<:07:701579365598756874>",
        8: "<:08:701579365321801809>",
        9: "<:09:701579365389041767>",
        10: "<:10:701579365661671464>",
        11: "<:11:701579365699551293>",
        12: "<:12:701579365162418188>",
        13: "<:132:704082689816395787>",
        14: "<:14:828991721181806623>",
        15: "<:th15:1028905841589506099>"
    }

    emoji = switcher.get(emojiName, None)
    return emoji