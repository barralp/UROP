import sys 
import wx
import wxmplot
import numpy

x = 0
y = 0

def axisLabel(data=None, selected=None, mask=None):
    print()
app = wx.App()

dataPlot = wxmplot.PlotFrame()
dataPlot.scatterplot()

dataPlot.panel.lasso_callback = axisLabel
