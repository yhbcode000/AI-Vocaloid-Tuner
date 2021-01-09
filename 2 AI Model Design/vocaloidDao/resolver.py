# import ElementTree class
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import os

import pandas as pd
import numpy as np

from vocaloidDaoClass import vocaloidDaoClass


class vocaloidVSQXResolver(vocaloidDaoClass):
    "Resolve vocaloid vsqx file by xml way."
    # define local variable root
    __root = None
    # define local variable vs part, the node under vsTrack
    __vsPartElement = None
    # define local variable tree
    __tree = None
    # define global variable noteNum
    noteNum = None
    # define global variable noteNum
    resolverIdentifier = None
    # define global variable File Path
    folderPath = None

    def __init__(self, xmlFilePath):
        super().__init__
        # import data from our dataset
        self.__tree = ET.parse(xmlFilePath)
        # pick the root of xml tree
        self.__root = self.__tree.getroot()
        # getting target subtree
        self.__vsPartElement = self.__root.find(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}vsTrack/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}vsPart')
        self.noteNum = len(self.__vsPartElement.findall('{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}note'))
        self.resolverIdentifier = os.path.basename(xmlFilePath)
        self.folderPath = os.path.dirname(xmlFilePath)

    def __getVel(self):
        # ("Log: pass vel list")
        return [int(i.text) for i in self.__vsPartElement.iterfind(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}note/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}v')]

    def __getNoteTime(self):
        # ("Log: pass dur list")
        return [int(i.text) for i in self.__vsPartElement.iterfind(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}note/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}t')]

    def __getDur(self):
        # ("Log: pass dur list")
        return [int(i.text) for i in self.__vsPartElement.iterfind(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}note/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}dur')]
    
    def __getOpe(self):
        # ("Log: pass Ope list")
        return [i.text for i in self.__vsPartElement.iterfind(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}note/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}nStyle/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}v') if i.attrib['id'] == "opening"]
    
    def __formatLists(self,targetList):
        "we has already know that each note has one vel one ope and one dur. from this idea we develop this func"
        resultLists = []
        resultSubList = []
        
        # build the matrix
        for target in targetList:
            for currentTime in range(super().numOfBeats * super().timeSliceRatio):
                resultSubList.append(target)
            resultLists.append(resultSubList)
            resultSubList = []

        return resultLists

    def getVelLists(self):
        "return the formated list of list of velocity"
        return self.__formatLists(self.__getVel())
    
    def getDurLists(self):
        "return the formated list of list of duration"
        return self.__formatLists(self.__getDur())

    def getOpeLists(self):
        "return the formated list of list of opening"
        return self.__formatLists(self.__getOpe())

    def __getTimeStamp(self):
        timeStampsTemp = self.__vsPartElement.iterfind(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}cc/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}t')
        return [int(i.text) for i in timeStampsTemp]

    def __getTimeStampId(self):
        timeStampsIdTemp = self.__vsPartElement.iterfind(
            '{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}cc/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}v')
        return [i.attrib['id'] for i in timeStampsIdTemp]

    def __getTimeStampText(self):
        timeStampTextTemp = self.__vsPartElement.iterfind('{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}cc/{http://www.yamaha.co.jp/vocaloid/schema/vsq4/}v')
        return [int(i.text) for i in timeStampTextTemp]

    def getTimeStampLists(self):
        "Get the time stamp of vs track."
        timeStampsList = []
        timeStamps = []

        for noteIndex in range(self.noteNum):
            for currentTime in range(super().numOfBeats * super().timeSliceRatio):
                timeStamps.append(currentTime)
            timeStampsList.append(timeStamps)
            timeStamps = []
        # ("Log: return the time stamp")
        return timeStampsList

        # ("Log: time stamps list returnned.")
        return timeStamps

    def getTimeStampIdList(self):
        "get the id or the tag of vs track according to time stamps. we don't need this be the input matrix, the original data is good enough"

        # ("Log: time stamps id returnned.")
        return self.__getTimeStampId()

    def getTimeStampTextLists(self):
        "get all these numNote x 960 listss of each id"
        TimeStampTextListsDic = {}
        TimeStampTextList = []
        TimeStampTextSubList = []

        for id in super().idSet:
            print("Log: " + id)
            for noteIndex in range(self.noteNum):
                # prepare data
                index = 0
                timeStampsTemp = self.__getTimeStamp()
                keyTime = timeStampsTemp[index]
                timeStampsIdTemp = self.__getTimeStampId()
                keyId = timeStampsIdTemp[index]
                timeStampsTextTemp = self.__getTimeStampText()
                newValue = timeStampsTextTemp[index]

                noteTimeStampTemp = self.__getNoteTime()
                currentStartingTime = noteTimeStampTemp[noteIndex]

                durList = self.__getDur()
                lastMaxValue = 0

                while (keyTime != currentStartingTime):
                    # update to next index
                    index+=1
                    if index == len(timeStampsTemp):
                        break
                    keyTime = timeStampsTemp[index]
                    keyId = timeStampsIdTemp[index]
                    newValue = timeStampsTextTemp[index]

                for currentTime in range(durList[noteIndex]):
                    flag = 0
                    while (keyTime - currentStartingTime == currentTime):
                        if (keyId == id):
                            lastMaxValue = newValue
                            TimeStampTextSubList.append(lastMaxValue)
                            flag = 1
                            break
                        # update to next index
                        index += 1
                        if index == len(timeStampsTemp):
                            break
                        keyTime = timeStampsTemp[index]
                        keyId = timeStampsIdTemp[index]
                        newValue = timeStampsTextTemp[index]
                        continue
                    if flag == 0:
                        TimeStampTextSubList.append(lastMaxValue)
                # padding with 0s means data not possible
                for currentTime in range(super().numOfBeats * super().timeSliceRatio - durList[noteIndex]):
                    TimeStampTextSubList.append(0)
                TimeStampTextList.append(TimeStampTextSubList)
                TimeStampTextSubList = []
            TimeStampTextListsDic[id] = TimeStampTextList
            TimeStampTextList = []

        # ("Log: time stamps text returnned.")
        return TimeStampTextListsDic

    def getFormatedVocaloidDataInDict(self):
        resultDict = self.getTimeStampTextLists()
        print("Log: finish time stamp")
        resultDict["VEL"] = self.getVelLists()
        print("Log: finish vel")
        resultDict["T"] = self.getTimeStampLists()
        print("Log: finish time")
        resultDict["OPE"] = self.getOpeLists()
        print("Log: finish opening")
        resultDict["DUR"] = self.getDurLists()
        print("Log: finish duration")
        return resultDict

    def saveFormatedVocaloidData(self):
        VocaloidDataDictDf = pd.DataFrame(self.getFormatedVocaloidDataInDict())
        try:
            VocaloidDataDictDf.to_csv(os.path.join(self.folderPath, self.resolverIdentifier[:-5]+"DataDict.csv"))
            print("Log: save to " + self.folderPath + "")
            return 1
        except:
            return -1
    
    def __intconverter(self, x):
        try:
            return int(x)
        except:
            return int(x[1:-1])

    def loadFormatedVocaloidData(self):
        "Load local data as data frame. data are in vector form"
        result = pd.DataFrame(pd.read_csv(os.path.join(self.folderPath, self.resolverIdentifier[:-5]+"DataDict.csv"))).drop(axis=1, labels="Unnamed: 0")
        result = result.applymap(lambda x : [self.__intconverter(i) for i in x[1:-1].split(", ")])
        print("Log: loaded ")
        return result

    def __getDiscreteArg(self, dataDict):
        pass

    def __getContinuousArg(self, dataDict):
        pass
    
    def saveVocaloidDataDfToVsqx(self):
        "Save modified data to vsqx"
        pass
