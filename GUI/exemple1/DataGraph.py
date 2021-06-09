import sys
import wx
import wxmplot
import numpy

class DataGraph(wx.Frame) :
    def __init__(self, parent):
        self.app = wx.App()
        super(DataGraph, self).__init__(parent, size=(450, 300))
        # m_x = x
        # m_y = y

    def makeGraph(self) :
        x1 = [0, 1, 2, 3]
        y1 = [0, 3, 4, 1]
        x2 = [0, 1, 2, 3]
        y2 = [5, 2, 3, 3]

        varGraph = wxmplot.PlotPanel(self, (1750, 1600))

        varGraph.scatterplot(x1, y1, title = 'x vs y graph', xLabel = 'x', yLabel = 'y')
        varGraph.scatterplot(x2, y2, color = "red", edgecolor = "red")

        self.Show()

if __name__ == '__main__':
    graph = DataGraph(None)
    graph.makeGraph()
    graph.app.MainLoop()
