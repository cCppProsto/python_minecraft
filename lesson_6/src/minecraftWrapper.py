from minecraft import Minecraft


def getPlayerEntityIds():
    try:
        mc = Minecraft.create()
        players = mc.getPlayerEntityIds()
        return players
    except:
        pass
    return []
