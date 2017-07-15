class DataProcessor(object):

    def __init__(self,dataBundle):
        self.rawData = dataBundle
        self.showHourlyData()

    def __getitem__(self, item):
        return self.dataBundle[item]

    def _processforHourlyData(self):
        self.dataBundle = dict(
            map(lambda (key, value): (key, self._modifyRawData(key, value)), self.rawData.iteritems()))

    def _modifyRawData(self,key,value):
        if(key!='sleepAnalysis'):
            value.index = value['startDate']
            value = value.drop('startDate',1)
            value = value.drop('endDate',1)
            return value.resample('H').sum().fillna(0)

    def showHourlyData(self):
        self._processforHourlyData()
        # print(self.rawData['stepCount'])
        # print(self.rawData['distanceWalking'])
        # print(self.rawData['stairsClimbing'])
        # print(self.rawData['sleepAnalysis'])