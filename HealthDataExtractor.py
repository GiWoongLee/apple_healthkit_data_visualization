from numpy import *
from xml.etree import ElementTree
from pandas import *
from DataProcessor import DataProcessor

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
        self.stepCount = []
        self.distanceWalking = []
        self.stairsClimbing = []
        self.sleepAnalysis = []

    def _report(self,msg):
        print(msg)
        sys.stdout.flush()

    def _convertDataToDataFrame(self):
        self.dataBundle = dict(map(lambda (key, value): (key, self._dataToDataFrame(key, value)), self.extractedData.iteritems()))

    def _dataToDataFrame(self, key, value):
        labels = self._getDataLabel(key)
        return DataFrame.from_records(value, columns=labels)

    def _getDataLabel(self, data):
        return {
            'stepCount': ['count', 'startDate', 'endDate'],
            'distanceWalking': ['km', 'startDate', 'endDate'],
            'stairsClimbing': ['count', 'startDate', 'endDate'],
            'sleepAnalysis': ['startDate', 'endDate']
        }[data]

    def _modifyMatrixDataType(self):
        self.dataBundle = dict(map(lambda (key, value): (key, self._modifyDataType(key, value)), self.dataBundle.iteritems()))

    # convert count,km,count info to int type + startDate/endDate to datetime format
    def _modifyDataType(self,key,value):
        if(key != 'sleepAnalysis'):
            if(key == 'distanceWalking'):
                value['km'] = value['km'].astype('float64')
            else:
                value['count'] = value['count'].astype(int)
        value['startDate'] = to_datetime(value['startDate'])
        value['endDate'] = to_datetime(value['endDate'])
        return value

    def parseXML(self):
        with open(self.in_path) as f:
            self._report('Reading data from %s...'%self.in_path)
            self.data = ElementTree.parse(f)
            self._report('done')
        f.close()
        self.root = self.data.getroot()

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
        self.extractedData = {'stepCount':self.stepCount, 'distanceWalking':self.distanceWalking, 'stairsClimbing':self.stairsClimbing,'sleepAnalysis':self.sleepAnalysis}

    def makeMatrix(self):
        self._convertDataToDataFrame()
        self._modifyMatrixDataType()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('USAGE: python HealthDataExtractor.py /path/to/datum.xml')
        sys.exit(1)
    dataBundle = HealthDataExtractor(sys.argv[1]).dataBundle
    DataProcessor(dataBundle)


# reference
# http://pbpython.com/pandas-list-dict.html
# https://chrisalbon.com/python/pandas_group_data_by_time.html
# http://www.hydro.washington.edu/~nijssen/computing_workshops/workshop_datetime_pandas_20131112.html