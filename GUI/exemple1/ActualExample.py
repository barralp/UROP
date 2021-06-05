import sys
import wx
import wxmplot
import numpy

class ActualExample(wx.Frame) :
    def __init__(self, parent):
        self.App = wx.App()
        super(ActualExample, self).__init__(parent, size=(450, 300))
        
    def makeGraph(self) :
        x = [0, 1, 2, 3]
        y = [0, 3, 4, 1]

        varGraph = wxmplot.PlotPanel(self, (450, 300))

        varGraph.plot(x, y, title = 'x vs y graph', xLabel = 'x', yLabel = 'y')

        ##varGraph.Show()

if __name__ == '__main__':
    graph = ActualExample(None)
    graph.makeGraph()
    graph.app.MainLoop()
