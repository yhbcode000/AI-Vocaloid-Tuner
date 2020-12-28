# import ElementTree class
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import os

from vocaloidDaoClass import vocaloidDaoClass

class vocaloidVSQXResolver(vocaloidDaoClass):
    "Resolve vocaloid vsqx file by xml way."
    # define local variable root
    __root = None
    # define local variable vs part, the node under vsTrack
    __vsPartElement = None

    def __init__(self, xmlFilePath):
        super().__init__
        # import data from our dataset
        tree = ET.parse(xmlFilePath)
        # pick the root of xml tree
        self.__root = tree.getroot()
        # getting target subtree
        self.__vsPartElement = self.__root.find(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}vsTrack/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}vsPart')

    def getTimeStampList(self):
        timeStamps = []
        timeStampsTemp = self.__vsPartElement.iterfind(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}cc/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}t')
        for currentTime in range(super().numOfBeats * super().timeSliceRatio):
            for id in range(super().idNum):
                timeStamps.append(currentTime)
        print("Log: time stamps returnned.\n")
        return timeStamps
    
    def getTimeStampsId(self):
        pass
    
    def getTimeStampsValue(self):
        pass

resolver = vocaloidVSQXResolver(r"C:\Users\hobar\Desktop\AI-Tuner\1 Feasibility Test\originalSoundData\testData1.vsqx")

timeStamps = resolver.
