from minecraft import Minecraft

def buld_platform(x, y, z):
    mc = Minecraft.create()
    mc.setBlocks(x - 4, y, z - 4, x + 4, y, z + 4, 'glass')
