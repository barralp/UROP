## Make it work in this file first, then add to the file with the rest of the displayconbgfvggggggggggggggggggvv           
import sys 
import wx
import wxmplot
import numpy

class DataPlotting : 

    def axisLabel(data=None, selected=None, mask=None):
        print()
        app = wx.App()

    def dataParser() ## create an array of tuples 
        return                                       

    dataPlot = wxmplot.PlotPanel() ## based on documentation it looks like this is te correct class
    dataPlot.scatterplot(x, y) ## x and y are an array of the values - take from sql file   

    dataPlot.panel.lasso_callback = axisLabel
    dataPlot.Show()
