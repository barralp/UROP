# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:40:00 2021

@author: Dypole
"""
#####WX IMPORTS#####
import wx
import wx.lib.scrolledpanel
import matplotlib
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
        self.figure = matplotlib.figure.Figure(facecolor="white", figsize=(3,3))
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color="gray")
        self.axes.set_xbound( (0,2) )
        self.axes.set_ybound( (0,10) )
        self.axes.set_xlabel( "X Var" ) ## change later
        self.axes.set_ylabel( "Y Var" )
        self.axes.grid(True, color="gray")
        
    def setUpMenu(self):
        self.xBox = wx.StaticBox(self, label='X parameters')
        self.xBoxSizer = wx.StaticBoxSizer(self.xBox, wx.VERTICAL)
        self.yBox = wx.StaticBox(self, label='Y parameters')
        self.yBoxSizer = wx.StaticBoxSizer(self.yBox, wx.VERTICAL)
        
        self.textX1 = wx.StaticText(self, label = "X Variable")
        self.textY1 = wx.StaticText(self, label = "Y Variable")
    
        variables = ['1', '2']
        relationsX = ['3', '4']
        relationsY = ['5', '6']
        
        self.dropDownX1 = wx.ComboBox(self, choices = variables)
        self.dropDownY1 = wx.ComboBox(self, choices = variables)

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
        
        self.menuBoxSizer.Add(self.yBoxSizer)
        self.menuBoxSizer.Add(self.xBoxSizer)
    
        
if __name__ == '__main__':
    ui = DypoleDatabaseViewer(None, title='"Database viewer"')
    ui.app.MainLoop()
