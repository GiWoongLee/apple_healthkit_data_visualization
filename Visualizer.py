import matplotlib.pyplot as plt

class Visualizer(object):

    def __init__(self,processedData):
        self.data = processedData
        self.plotDataHourly()

    def __getitem__(self, item):
        return 0

    def plotDataHourly(self):
        dict(map(lambda (key, value): (key, self._plotData(key, value)), self.data.iteritems()))

    def _plotData(self,key,value):
        if(key!='sleepAnalysis'):
            self.data[key].columns.name = key
            self.data[key].index.name = "Time(Hour)"
            plotTitle = 'Hour-Based ' + key
            self.data[key][:50].plot(lw=2, colormap='jet', marker='.', markersize=10, title=plotTitle)
            plt.show()