import time
import threading
from src.prison import Prison
from src.minecraftWrapper import MinecraftSingleton as mc

_isWorking = True
_prisonIsPause = False


_MENU_STATE_MAIN = 1
_MENU_STATE_PRISON = 2

_CURRENT_MENU_STATE = _MENU_STATE_MAIN


def _getIntInput(title, default=0):
    value = raw_input(title + '(default=' + str(default) + '):  ')
    if not value:
        value = default
    else:
        value = int(value)
    return value

def printMainMenu():
    print('1. Prison')
    print('2. Get players')
    print('3. Exit')


def printPrisonMenu():
    print('1. Add player to prison')
    print('2. Get prisoners')
    print('3. Back to main menu')


def printMenu():
    if _CURRENT_MENU_STATE == _MENU_STATE_MAIN:
        printMainMenu()
    elif _CURRENT_MENU_STATE == _MENU_STATE_PRISON:
        printPrisonMenu()


def setMenuState(state):
    global _CURRENT_MENU_STATE
    _CURRENT_MENU_STATE = state


def handleMainMenu(val):
    global _isWorking

    if val == 1:
        setMenuState(_MENU_STATE_PRISON)

    elif val == 2:
        players = mc.getInstance().getPlayerEntityIds()
        print('')
        for p in players:
            v = p.split(':')
            print(v[0])
        print('')

    elif val == 3:
        _isWorking = False


def handlePrisonMenu(val):
    if val == 1:
        p = Prison().getInstance()

        name = str(raw_input('name: '))
        if p.isPrisoner(name):
            print(name + ' already in prison')
            return

        reason = str(raw_input('reason: '))
        days = _getIntInput('days', 0)
        hours = _getIntInput('hours', 0)
        minutes = _getIntInput('minutes', 0)

        p.addToPrison(name=name, reason=reason, days=days, hours=hours, minutes=minutes)

    elif val == 2:
        p = Prison().getInstance()
        prisoners = p.getPrisoners()
        print('')
        for v in prisoners:
            print('    name: ' + v + ',  remained: ' + p.getRemainedTimeStr(v))
        print('')
    elif val == 3:
        setMenuState(_MENU_STATE_MAIN)


def inputCmdHandler(val):
    if _CURRENT_MENU_STATE == _MENU_STATE_MAIN:
        handleMainMenu(val)
    elif _CURRENT_MENU_STATE == _MENU_STATE_PRISON:
        handlePrisonMenu(val)


def main():
    global _isWorking

    while _isWorking:
        printMenu()
        iv = input()
        inputCmdHandler(iv)


def manager():
    global _isWorking

    p = Prison().getInstance()
    while _isWorking:
        if not _prisonIsPause:
            p.checkAndMove()
        time.sleep(1)

t1 = threading.Thread(target=main)
t2 = threading.Thread(target=manager)

t1.start()
t2.start()

t1.join()
t2.join()

print('All stopped.')



def test():
    import datetime
    import time
    ts_start = time.time()
    ts_end = ts_start + 1000

    tc = datetime.datetime.fromtimestamp(ts_start)
    tn = datetime.datetime.fromtimestamp(ts_end)

    dt1 = datetime.datetime.strptime(tc.strftime('%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S.%f')
    dt2 = datetime.datetime.strptime(tn.strftime('%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S.%f')
    dtdiff = dt2 - dt1
    _str = str(dtdiff)
    dtdiff = None

    #p = Prison()

#main()

#test()



#x, y, z = p.getCenter()
#mc.entity.setTilePos(id, x, y, z)


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
# mc.setSign(pos.x + 1, pos.y, pos.z, 'BIRCH_SIGN', 1, 'oak_sign', 1, 'Hello World', '123', 'This is oak_sign')

#x, y, z = pos
#buld_platform(x, y + 40, z)
#mc.entity.setTilePos(id, x, y+41, z)
#id = mc.getPlayerEntityId('cppprosto')
#ids = mc.getPlayerEntityIds()
#for id in ids:
#    name, id = id.split(':')
