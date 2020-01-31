import xml.etree.ElementTree as ET
import os
import time
from datetime import datetime

from minecraft import Minecraft
from minecraftWrapper import getPlayerEntityIds

_PRISON_CONFIG_FILE_NAME = 'prison.xml'
_PRISON_X = 0
_PRISON_Y = 100
_PRISON_Z = 0
_PRISON_WIDTH = 40

_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

# https://docs.python.org/2/library/xml.etree.elementtree.html


class _Prisoner:
    def __init__(self, xmlData):
        self.__id = ''
        self.__start = 0
        self.__end = 0
        self.__reason = ''

        for child in xmlData:
            if child.tag == 'id':
                self.__id = child.text
            elif child.tag == 'start':
                self.__start = int(child.text)
            elif child.tag == 'end':
                self.__end = int(child.text)
            elif child.tag == 'reason':
                self.__reason = child.text

    @property
    def id(self):
        return self.__id

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def reason(self):
        return self.__reason


class Prison:
    def __init__(self):
        self.__mc = Minecraft.create()
        self.__prisoners = []
        self.__left_top_position = ()
        self.__right_bottom_position = ()

        self.__readConfig()

    def __readConfig(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/' + _PRISON_CONFIG_FILE_NAME
        isExist = os.path.isfile(path)

        if not isExist:
            return
        root = ET.parse(path).getroot()

        for child in root:
            if child.tag == 'prisoners':
                self.__readPrisoners(child)
            elif child.tag == 'prisonPlace':
                self.__readPlaceInfo(child)

    def __readPrisoners(self, prisoners):
        for child in prisoners:
            if child.tag == 'prisoner':
                self.__prisoners.append(_Prisoner(child))

    def __readPlaceInfo(self, xmlPlaceData):
        for child in xmlPlaceData:
            if child.tag == 'l_top':
                self.__left_top_position = self.__getPositions(child)
            elif child.tag == 'r_bottom':
                self.__right_bottom_position = self.__getPositions(child)

    def __getPositions(self, xmlPosData):
        pos = []
        for child in xmlPosData:
            if child.tag == 'x':
                pos.append(int(child.text))
            elif child.tag == 'y':
                pos.append(int(child.text))
            elif child.tag == 'z':
                pos.append(int(child.text))
        return tuple(pos)

    def isPrisoner(self, playerName):
        for p in self.__prisoners:
            if p.id == playerName:
                return True
        return False

    def getRemainedTimeStr(self, playerName):
        for p in self.__prisoners:
            if p.id == playerName:
                ts_now = time.time()
                ts_end = p.end

                if ts_now > ts_end:
                    return ''

                dt_1 = datetime.fromtimestamp(ts_now)
                dt_2 = datetime.fromtimestamp(ts_end)
                v1 = datetime.strptime(dt_1.strftime(_TIME_FORMAT), _TIME_FORMAT)
                v2 = datetime.strptime(dt_2.strftime(_TIME_FORMAT), _TIME_FORMAT)
                return str(v2 - v1)
        return ''

    def getPrisonPlace(self):
        return {'left_top': self.__left_top_position,
                'right_bottom': self.__right_bottom_position,
                }

    def build(self):
        self.__mc.setBlocks(
            _PRISON_X - _PRISON_WIDTH / 2, _PRISON_Y, _PRISON_Z - _PRISON_WIDTH / 2,
            _PRISON_X + _PRISON_WIDTH / 2, _PRISON_Y, _PRISON_Z + _PRISON_WIDTH / 2,
            'glass')

    def getCenter(self):
        return (_PRISON_X, _PRISON_Y + 1, _PRISON_Z)

    def checkAndMove(self):
        ids = getPlayerEntityIds()
        for id in ids:
            name, id = id.split(':')
            if self.isPrisoner(name):
                cur_pos = self.__mc.entity.getTilePos(id)
                self.__mc.entity.setTilePos(id, _PRISON_X, _PRISON_Y + 1, _PRISON_Z)



'''
# Compares floats for equality as proposed in https://www.python.org/dev/peps/pep-0485/#id13
# ---------------------------------------------------------------------------------------------------
def isClose(a, b, relTol=1e-09, absTol=0.0):
    return abs(a - b) <= max(relTol * max(abs(a), abs(b)), absTol)


# Compares tuple of position(x, y, z) -> (float, float, float) for equality
# ---------------------------------------------------------------------------------------------------
def isPositionsClose(l, r):
    if len(l) != 3 or len(r) != 3:
        return False

    xIsEq = isClose(l[0], r[0])
    yIsEq = isClose(l[1], r[1])
    zIsEq = isClose(l[2], r[2])
    return xIsEq and yIsEq and zIsEq
'''