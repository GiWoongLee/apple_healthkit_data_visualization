import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np; np.random.seed(22)
from pandas import *

class Visualizer(object):

    def __init__(self,processedData):
        self.data = processedData
        # self.plotDataHourly()
        self.plotTimeSeriesPackage()
        self.plotMultiDataPackage()

    def __getitem__(self, item):
        return 0

    def getPartialData(self,title,col,num):
        return self.data[title][col][:num]

    def _plotDataBarGraph(self,title,col,num):
        self.data[title].columns.name = title
        self.data[title].index.name = 'Time(Hour)'
        plotTitle = 'Hour-Based ' + title
        self.data[title][col][:num].plot(lw=2, colormap='jet', marker='.', markersize=10, title=plotTitle)
        plt.show()

    def _plotDataScatterPlot(self,title,col,num):
        sns.tsplot(data=self.data[title][col][:num], err_style="ci_bars", interpolate=False)
        plt.show()
        # https://chrisalbon.com/python/seaborn_pandas_timeseries_plot.html

    def _plotDensityPlot(self,title,col,num):
        self.data[title][col][:num].plot(kind='kde')
        # sns.distplot(self.data[title][col][:num], hist=False, rug=True);
        plt.show()
        # https://stackoverflow.com/questions/31348737/how-to-plot-kernel-density-plot-of-dates-in-pandas

    def _plotUnivariateDistribution(self,title,col,num):
        sns.distplot(self.data[title][col][:num])
        plt.show()

    def _plotHistorgram(self, title, col, num):
        sns.distplot(self.data[title][col][:num],kde=False,rug=True)
        plt.show()

    def _plotBandWidthDistribution(self,title,col,num):
        sns.kdeplot(self.data[title][col][:num])
        sns.kdeplot(self.data[title][col][:num], bw=.2, label="bw: 0.2")
        sns.kdeplot(self.data[title][col][:num], bw=2, label="bw: 2")
        plt.legend()
        plt.show()

    def _mergeTwoDataFrame(self,title1,title2,col1,col2):
        normalizedData = self.data[title1].divide(10,axis=col1)
        return concat([normalizedData,self.data[title2]], axis=1, join='inner')
        # return self.data[title1][1:].merge(self.data[title2], left_on=col1, right_on=col2, how='inner')

    def _plotBiScatterPlot(self,title1,title2,col1,col2,num):
        mergedData =self._mergeTwoDataFrame(title1,title2,col1,col2)
        sns.jointplot(x=col1, y=col2, data=mergedData[:num])
        plt.show()

    def _plotBiJointPlot(self,title1,title2,col1,col2,num):
        mergedData = self._mergeTwoDataFrame(title1, title2, col1, col2)
        sns.jointplot(x=col1, y=col2, data=mergedData[:num], kind="kde")
        plt.show()

    def _plotBiKdePlot(self,title1,title2,col1,col2,num):
        mergedData = self._mergeTwoDataFrame(title1, title2, col1, col2)
        f, ax = plt.subplots(figsize=(6, 6))
        sns.kdeplot(mergedData[col1][:num], mergedData[col2][:num], ax=ax)
        plt.show()

    def _plotBiKdeColorPlot(self, title1, title2, col1, col2, num):
        mergedData = self._mergeTwoDataFrame(title1, title2, col1, col2)
        f, ax = plt.subplots(figsize=(6, 6))
        cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
        sns.kdeplot(mergedData[col1][:num],mergedData[col2][:num], cmap=cmap, n_levels=60, shade=True);
        plt.show()

    def _plotBiKdeCrossPlot(self, title1, title2, col1, col2, num):
        mergedData = self._mergeTwoDataFrame(title1, title2, col1, col2)
        g = sns.jointplot(x=col1, y=col2, data=mergedData[:num], kind="kde", color="m")
        g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
        g.ax_joint.collections[0].set_alpha(0)
        g.set_axis_labels(col1,col2);
        plt.show()

    def _plotViolinPlot(self,title1,title2,col1,col2,num):
        mergedData = self._mergeTwoDataFrame(title1, title2, col1, col2)
        sns.violinplot([mergedData[col2][:num],mergedData[col1][:num]])
        plt.show()

    def _plotHeatMap(self,title1,title2,col1,col2,num):
        mergedData = self._mergeTwoDataFrame(title1, title2, col1, col2)
        sns.heatmap([mergedData[col2][:num],mergedData[col1][:num]],annot=True,fmt="f")
        plt.show()

    def _plotClusterMap(self,title1,title2,col1,col2,num):
        mergedData = self._mergeTwoDataFrame(title1, title2, col1, col2)
        mergedData = mergedData.drop('timeSeries', 1)
        sns.clustermap(mergedData[:num])
        plt.show()

    def plotTimeSeriesPackage(self):
        self._plotDataBarGraph('stepCount', 'stepCount', 100)
        self._plotDataScatterPlot('stepCount', 'stepCount', 100)
        self._plotDensityPlot('stepCount', 'stepCount', 100)
        self._plotUnivariateDistribution('stepCount', 'stepCount', 100)
        self._plotHistorgram('stepCount', 'stepCount', 100)
        self._plotBandWidthDistribution('stepCount', 'stepCount', 100)

    def plotMultiDataPackage(self):
        self._plotBiScatterPlot('stepCount','stairsClimbing','stepCount','stairsCount',100)
        self._plotBiJointPlot('stepCount','stairsClimbing','stepCount','stairsCount',100)
        self._plotBiKdePlot('stepCount','stairsClimbing','stepCount','stairsCount',100)
        self._plotBiKdeColorPlot('stepCount','stairsClimbing','stepCount','stairsCount',100)
        self._plotBiKdeCrossPlot('stepCount','stairsClimbing','stepCount','stairsCount',100)
        self._plotViolinPlot('stepCount','stairsClimbing','stepCount','stairsCount',100)
        self._plotHeatMap('stepCount','stairsClimbing','stepCount','stairsCount',100)
        self._plotClusterMap('stepCount','stairsClimbing','stepCount','stairsCount',100)

    def plotDataHourly(self):
        dict(map(lambda (key, value): (key, self._plotData(key, value)), self.data.iteritems()))

    def _plotData(self,key,value):
        if(key!='sleepAnalysis'):
            self.data[key].columns.name = key
            self.data[key].index.name = "Time(Hour)"
            plotTitle = 'Hour-Based ' + key
            self.data[key][:400].plot(lw=2, colormap='jet', marker='.', markersize=10, title=plotTitle)
            self.data[key][:1000].plot(lw=2, colormap='jet', marker='.', markersize=10, title=plotTitle)
            plt.show()

#reference : https://seaborn.pydata.org/tutorial/distributions.html
# https: // chrisalbon.com / python / pandas_with_seaborn.html
# https://seaborn.pydata.org/tutorial/distributions.html