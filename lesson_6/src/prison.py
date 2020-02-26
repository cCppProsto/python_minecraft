# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import time
from datetime import datetime

from src.minecraftWrapper import MinecraftSingleton as mc

_PRISON_CONFIG_FILE_NAME = 'prison.xml'
_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

# https://docs.python.org/2/library/xml.etree.elementtree.html


class _Prisoner:
    def __init__(self, xmlData, idx):
        self.__name = ''
        self.__start = 0
        self.__end = 0
        self.__reason = ''
        self.__idx = idx

        for child in xmlData:
            if child.tag == 'name':
                self.__name = child.text
            elif child.tag == 'start':
                self.__start = int(child.text)
            elif child.tag == 'end':
                self.__end = int(child.text)
            elif child.tag == 'reason':
                self.__reason = child.text

    @property
    def name(self):
        return self.__name

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def reason(self):
        return self.__reason

    @property
    def index(self):
        return self.__idx


class Prison:
    __instance = None

    @classmethod
    def getInstance(cls):
        try:
            if not cls.__instance:
                cls.__instance = Prison()
                return cls.__instance
            else:
                return cls.__instance
        except:
            return None

    def __init__(self):
        self.__prisoners = []
        self.__pos = ()
        self.__width = 0

        self.__root = None
        self.__tree = None
        self.__prisonersElement = None

        self.__readConfig()

    def addToPrison(self, name, reason, days=0, hours=0, minutes=0):
        self._reloadConfig()

        if self.isPrisoner(name):
            return
        period = minutes*60 + hours * 3600 + days*86400
        _str = ("<prisoner>\n"
                "    <name>{}</name>\n"
                "    <start>{}</start>\n"
                "    <end>{}</end>\n"
                "    <reason>{}</reason>\n"
                "</prisoner>\n"
                "\n")

        ts_start = int(time.time())
        ts_end = int(ts_start + period)
        result_data = _str.format(name, ts_start, ts_end, reason)

        newElement = ET.fromstring(result_data)
        #self.__prisonersElement.append(newElement)
        for prisoners in self.__root.findall('prisoners'):
            prisoners.append(newElement)
            self.__tree.write(os.path.dirname(os.path.abspath(__file__)) + '/' + _PRISON_CONFIG_FILE_NAME)
            self._reloadConfig()

    def isPrisoner(self, playerName):
        for p in self.__prisoners:
            if p.name == playerName:
                return True
        return False

    def getPrisoners(self):
        list_res = []
        for p in self.__prisoners:
            list_res.append(p.name)
        return list_res

    def getPrisoner(self, name):
        for p in self.__prisoners:
            if p.name == name:
                return p
        return None

    def getRemainedTimeStr(self, playerName):
        for p in self.__prisoners:
            if p.name == playerName:
                ts_now = int(time.time())
                ts_end = int(p.end)

                if ts_now > ts_end:
                    return ''

                dt_1 = datetime.fromtimestamp(ts_now)
                dt_2 = datetime.fromtimestamp(ts_end)
                v1 = datetime.strptime(dt_1.strftime(_TIME_FORMAT), _TIME_FORMAT)
                v2 = datetime.strptime(dt_2.strftime(_TIME_FORMAT), _TIME_FORMAT)
                return str(v2 - v1)
        return ''

    def getPos(self):
        return self.__pos

    def getWidth(self):
        return self.__width

    def _reloadConfig(self):
        self.__prisoners = []
        self.__pos = ()
        self.__width = 0

        self.__root = None
        self.__tree = None
        self.__prisonersElement = None
        self.__readConfig()

    def __readConfig(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/' + _PRISON_CONFIG_FILE_NAME
        isExist = os.path.isfile(path)

        if not isExist:
            return
        self.__tree = ET.parse(path)
        self.__root = self.__tree.getroot()

        for child in self.__root:
            if child.tag == 'prisoners':
                self.__readPrisoners(child)
            elif child.tag == 'prisonPlace':
                self.__readPlaceInfo(child)

        self.__prisonersElement = self.__root.find('prisoners')

    def __readPrisoners(self, prisoners):
        for idx, child in enumerate(prisoners):
            if child.tag == 'prisoner':
                self.__prisoners.append(_Prisoner(child, idx))

    def __readPlaceInfo(self, xmlPlaceData):
        for child in xmlPlaceData:
            if child.tag == 'pos':
                self.__pos = self.__getPositions(child)
            elif child.tag == 'width':
                self.__width = int(child.text)

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

    def _buildRoom(self, lp, rp):
        if mc.getInstance():
            # floor
            mc.getInstance().setBlocks(lp, rp, 'glass')

            # roof
            p1 = (lp[0], lp[1] + 4, lp[2])
            p2 = (rp[0], rp[1] + 4, rp[2])
            mc.getInstance().setBlocks(p1, p2, 'cocoa')

            # wall - 1
            p1 = (lp[0], lp[1], lp[2] - 1)
            p2 = (p1[0] + self.__width, p1[1] + 3, p1[2])
            mc.getInstance().setBlocks(p1, p2, 'acacia_log')

            # wall - 2
            p1 = (lp[0] - 1, lp[1], lp[2])
            p2 = (p1[0], p1[1] + 3, p1[2] + self.__width)
            mc.getInstance().setBlocks(p1, p2, 'blue_ice')

            # wall - 3
            p2 = (rp[0], rp[1], rp[2] + 1)
            p1 = (p2[0] - self.__width, p2[1] + 3, p2[2])
            mc.getInstance().setBlocks(p1, p2, 'frosted_ice')

            # wall - 4
            p2 = (rp[0] + 1, rp[1], rp[2])
            p1 = (p2[0], p2[1] + 3, p2[2] - self.__width)
            mc.getInstance().setBlocks(p1, p2, 'ice')

    def removeFromPrisoners(self, name):
        for prisoners in self.__root.findall('prisoners'):
            for prisoner in prisoners.findall('prisoner'):
                if name == prisoner.find('name').text:
                    prisoners.remove(prisoner)
                    self.__tree.write(os.path.dirname(os.path.abspath(__file__)) + '/' + _PRISON_CONFIG_FILE_NAME)
                    self._reloadConfig()
                    return

    def checkAndMove(self):
        if not mc.getInstance():
            return

        _mc = mc.getInstance()

        ids = _mc.getPlayerEntityIds()
        for v in ids:
            name, id = v.split(':')
            remainedTime = self.getRemainedTimeStr(name)
            if remainedTime:
                p = self.getPrisoner(name)
                if p:
                    x, y, z = _mc.getEntityTilePos(id)
                    xOffset = (p.index * (self.__width + 2))
                    plp = (self.__pos[0] + xOffset, self.__pos[1], self.__pos[2])
                    prp = (self.__pos[0] + self.__width + xOffset, self.__pos[1], self.__pos[2] + self.__width)
                    pp = (plp[0] + self.__width/2, plp[1] + 1, plp[2] + self.__width/2)

                    if x < plp[0] or x > prp[0] or z < plp[2] or z > prp[2] or y < plp[1]:
                        self._buildRoom(plp, prp)
                        _mc.setEntityTilePos(id, pp)

                    _mc.setSign((plp[0], plp[1]+1, [2]), name, p.reason, 'be happy', remainedTime)
            else:
                self.removeFromPrisoners(name)


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



<root>
    <prisoners>
        <prisoner>
            <name>cppProsto</name>
            <start>1581321936</start>
            <end>1582358736</end>
            <reason>prosto</reason>
        </prisoner>
    </prisoners>
    <prisonPlace>
        <pos>
            <x>-100</x>
            <y>40</y>
            <z>0</z>
        </pos>
        <width>4</width>
    </prisonPlace>
</root>


'''