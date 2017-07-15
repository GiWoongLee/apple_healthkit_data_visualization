from numpy import *
from xml.etree import ElementTree
from pandas import *

import re
import sys

PREFIX_RE = re.compile('^HK.*TypeIdentifier(.+)$')

def abbreviate(s):
    m = re.match(PREFIX_RE,s)
    return m.group(1) if m else s


class HealthDataExtractor(object):

    def __init__(self,path):
        self.in_path = path
        self.parseXML()
        self.intializeMatrix()
        self.extractRelevantData()
        self.makeMatrix()

    def __getitem__(self, key):
        return self.dataBundle[key]

    def intializeMatrix(self):
        self.dataTypes = ['stepCount', 'distanceWalking', 'stairsClimbing', 'sleepAnalysis']
        self.stepCount = []
        self.stepCountMetaData = {'info': ['value', 'startDate', 'endDate'], 'unit': 'count'}
        self.distanceWalking = []
        self.distanceWalkingMetaData = {'info': ['value', 'startDate', 'endDate'], 'unit': 'km'}
        self.stairsClimbing = []
        self.stairsClimbingMetaData = {'info': ['value', 'startDate', 'endDate'], 'unit': 'count'}
        self.sleepAnalysis = []
        self.sleepAnalysisMetaData = {'info': ['startDate', 'endDate'], 'unit': 'datetime'}

    def parseXML(self):
        with open(self.in_path) as f:
            self.report('Reading data from %s...'%self.in_path)
            self.data = ElementTree.parse(f)
            self.report('done')
        f.close()
        self.root = self.data.getroot()

    def report(self,msg):
        print(msg)
        sys.stdout.flush()

    def extractRelevantData(self):
        for child in self.root:
            if child.tag == 'Record':
                if 'type' in child.attrib:
                    dataType = abbreviate(child.attrib['type'])
                    if dataType == 'StepCount':
                        self.stepCount.append([child.attrib['value'],child.attrib['startDate'],child.attrib['endDate']])
                    elif dataType == 'DistanceWalkingRunning':
                        self.distanceWalking.append([child.attrib['value'],child.attrib['startDate'],child.attrib['endDate']])
                    elif dataType == 'FlightsClimbed':
                        self.stairsClimbing.append([child.attrib['value'],child.attrib['startDate'],child.attrib['endDate']])
                    elif dataType == 'SleepAnalysis':
                        self.sleepAnalysis.append([child.attrib['startDate'],child.attrib['endDate']])
                    else:
                        pass

    def makeMatrix(self):
        self.stepCountDF = DataFrame(self.stepCount)
        self.distanceWalkingDF = DataFrame(self.distanceWalking)
        self.stairsClimbingDF = DataFrame(self.stairsClimbing)
        self.sleepAnalysisDF = DataFrame(self.sleepAnalysis)
        self.dataBundle = {'stepCountData':self.stepCountDF, 'distanceWalkingData':self.distanceWalkingDF, 'stairsClimbingData':self.stepCountDF,'sleepAnalysisData':self.sleepAnalysisDF}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('USAGE: python HealthDataExtractor.py /path/to/datum.xml')
        sys.exit(1)
    data = HealthDataExtractor(sys.argv[1])



# reference
# http://pbpython.com/pandas-list-dict.html
# https://chrisalbon.com/python/pandas_group_data_by_time.html
# http://www.hydro.washington.edu/~nijssen/computing_workshops/workshop_datetime_pandas_20131112.html