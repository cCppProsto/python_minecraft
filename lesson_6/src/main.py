from minecraft import Minecraft
from prison import Prison

mc = Minecraft.create()
pos = mc.player.getTilePos()
# mc.setSign(pos.x + 1, pos.y, pos.z, 'BIRCH_SIGN', 1, 'oak_sign', 1, 'Hello World', '123', 'This is oak_sign')

id = mc.getPlayerEntityId('cppprosto')

#x, y, z = pos
#buld_platform(x, y + 40, z)
#mc.entity.setTilePos(id, x, y+41, z)

p = Prison()
p.build()
x, y, z = p.getCenter()
mc.entity.setTilePos(id, x, y, z)

'''
mc = Minecraft.create()
pos = mc.player.getTilePos()
x, y, z = pos

h = mc.getHeight(1, 2)

mc.spawnEntity(x, y, z,'donkey')
id = mc.getPlayerEntityId('cppprosto')
#ids = mc.getPlayerEntityIds()
#mc.entity.setTilePos(id, x + 5, y, z)
pos = None
'''