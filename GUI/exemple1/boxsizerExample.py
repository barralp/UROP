
from wx.core import EVT_CHECKBOX

sys.path.insert(0, '../../database')
import os
import sys
# i found the following version more portable
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.path[0])),'database')) # goes 2 level up
from communicate_database import getEntireColumn
import DataFrame
#from DataFrame import getVariableList
import matplotlib
import numpy
import wx
import wx.lib.scrolledpanel
import numpy as np
import pandas as pd

matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class DypoleDatabaseViewer(wx.Frame):
    def __init__(self, parent, title):
        self.app = wx.App()
        wx.Frame.__init__(self, parent, title = title, size = (1000, 500))
        self.start()
        
    def start(self):
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
    
        self.basePanel = wx.lib.scrolledpanel.ScrolledPanel(self, id = -1, size = (1,1))
        self.basePanel.SetupScrolling()
        self.mainWindowBoxSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.firstRowBox = wx.StaticBox(self.basePanel, label='Upper box')
        self.firstRowBoxSizer = wx.StaticBoxSizer(self.firstRowBox, wx.HORIZONTAL)
        
        self.Box11 = wx.StaticBox(self.basePanel, label='Graph 1')
        self.BoxSizer11 = wx.StaticBoxSizer(self.Box11, wx.HORIZONTAL)
        self.Box12 = wx.StaticBox(self.basePanel, label='Graph 2')
        self.BoxSizer12 = wx.StaticBoxSizer(self.Box12, wx.HORIZONTAL)
        
        self.graph1 = PlotPanel(self.basePanel)
        self.BoxSizer11.Add(self.graph1)
        self.graph2 = PlotPanel(self.basePanel)
        self.BoxSizer12.Add(self.graph2)
        
        self.firstRowBoxSizer.Add(self.BoxSizer11)
        self.firstRowBoxSizer.Add(self.BoxSizer12)
        
        self.secondRowBox = wx.StaticBox(self.basePanel, label='Lower box')
        self.secondRowBoxSizer = wx.StaticBoxSizer(self.secondRowBox, wx.VERTICAL)
        
        self.Box21 = wx.StaticBox(self.basePanel, label='Graph 3')
        self.BoxSizer21 = wx.StaticBoxSizer(self.Box21, wx.HORIZONTAL)

        self.graph3 = PlotPanel(self.basePanel)
        self.BoxSizer21.Add(self.graph3, flag=wx.ALL|wx.EXPAND, border = 5)
        
        self.secondRowBoxSizer.Add(self.BoxSizer21)
        
        self.mainWindowBoxSizer.Add(self.firstRowBoxSizer)
        self.mainWindowBoxSizer.Add(self.secondRowBoxSizer)
        
        self.basePanel.SetSizer(self.mainWindowBoxSizer)
        

class PlotPanel(wx.Panel):
    dataFrame = DataFrame.DataFrame()
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.initPlotPanel()
    
    def initPlotPanel(self):
        self.mainBoxSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.setUpFigure()

        self.menuBox = wx.StaticBox(self, label='Menu')
        self.menuBoxSizer = wx.StaticBoxSizer(self.menuBox, wx.HORIZONTAL)
        
        self.setUpMenu()
        
        self.mainBoxSizer.Add(self.canvas, flag=wx.ALL, border=5)
        self.mainBoxSizer.Add(self.menuBoxSizer)
    
        self.SetSizer(self.mainBoxSizer)
    
    def setUpFigure(self):
        self.figure = matplotlib.figure.Figure(facecolor="white", figsize=(4,4))
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color="gray")
        self.axes.set_xbound( (0,2) )
        self.axes.set_ybound( (0,10) )
        self.axes.set_xlabel( "X Var" ) ## change later
        self.axes.set_ylabel( "Y Var" )
        self.axes.grid(True, color="gray")
    
    def updateDropDown(self, event) :
        self.axes.cla()  
        dropDownX = self.dropDownX1.GetStringSelection()
        dropDownY = self.dropDownY1.GetStringSelection()
        self.axes.set_title(dropDownX + " vs. " + dropDownY) 
        self.axes.set_xlabel(dropDownX) ## change later
        self.axes.set_ylabel(dropDownY)
        if (dropDownY != "" and dropDownX != "") :
            self.axes.plot(self.changeVar(dropDownX),
            self.changeVar(dropDownY), marker ='o', ls = '')
            self.axes.plot([],[])
        else :
            self.axes.plot([],[])
            self.canvas.draw()

    def setUpMenu(self):
        self.xBox = wx.StaticBox(self, label='X parameters')
        self.xBoxSizer = wx.StaticBoxSizer(self.xBox, wx.VERTICAL)
        self.yBox = wx.StaticBox(self, label='Y parameters')
        self.yBoxSizer = wx.StaticBoxSizer(self.yBox, wx.VERTICAL)
        
        self.textX1 = wx.StaticText(self, label = "X Variable")
        self.textY1 = wx.StaticText(self, label = "Y Variable")
    
        varsX = self.dataFrame.getVariableList("CiceroOut")
        varsY = self.dataFrame.getVariableList("nCount")
        relationsX = ["x", "log(x)", "x^2", "x^0.5"]
        relationsY = ["y", "log(y)", "y^2", "y^0.5"]
        
        self.dropDownX1 = wx.ComboBox(self, choices = varsX)
        self.dropDownY1 = wx.ComboBox(self, choices = varsY)

        self.dropDownX1.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        self.dropDownY1.Bind(wx.EVT_COMBOBOX, self.updateDropDown)

        self.textXRelations = wx.StaticText(self, label = "X Transformation")
        self.textYRelations = wx.StaticText(self, label = "Y Transformation")

        self.dropDownXRelations1 = wx.ComboBox(self, choices = relationsX)
        self.dropDownYRelations1 = wx.ComboBox(self, choices = relationsY)
        
        self.xBoxSizer.Add(self.textX1)
        self.xBoxSizer.Add(self.dropDownX1)
        self.xBoxSizer.Add(self.textXRelations)
        self.xBoxSizer.Add(self.dropDownXRelations1)
        self.yBoxSizer.Add(self.textY1)
        self.yBoxSizer.Add(self.dropDownY1)
        self.yBoxSizer.Add(self.textYRelations)
        self.yBoxSizer.Add(self.dropDownYRelations1)
        
        self.menuBoxSizer.Add(self.xBoxSizer)
        self.menuBoxSizer.Add(self.yBoxSizer)
        self.updateDropDown(0)
    
    def changeVar(self, selection) :
        if (selection != '') :
            data = self.dataFrame.getCoordinates(self.dropDownX1, self.dropDownY1)
        else :
            data = []
            print('no matching')
        return data
        
if __name__ == '__main__':
    ui = DypoleDatabaseViewer(None, title='"Database viewer"')
    ui.app.MainLoop()