from minecraft import Minecraft


class MinecraftSingleton:
    __instance = None

    def __init__(self, mc):
        self.__mc = mc
        self.__tmp = ''

    @classmethod
    def getInstance(cls):
        try:
            if not cls.__instance:
                mc = Minecraft.create()
                cls.__instance = MinecraftSingleton(mc)
                return cls.__instance
            else:
                return cls.__instance
        except:
            return None

    def getPlayerEntityIds(self):
        try:
            players = self.__mc.getPlayerEntityIds()
            return players
        except:
            pass
        return []

    def setPrisonSign(self, pos, line1='', line2='', line3='', line4=''):
        try:
            self.__mc.setSign(pos[0], pos[1], pos[2], 'BIRCH_SIGN', 1, line1, line2, line3, line4)
        except:
            pass

    def setBlocks(self, pos1, pos2, type):
        try:
            self.__mc.setBlocks(pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2], type)
        except:
            pass

    def getEntityTilePos(self, id):
        try:
            return self.__mc.entity.getTilePos(id)
        except:
            return 0, 0, 0

    def setEntityTilePos(self, id, pos):
        try:
            self.__mc.entity.setTilePos(id, pos[0], pos[1], pos[2])
        except:
            pass

