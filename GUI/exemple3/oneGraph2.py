import sys

from wx.core import EVT_CHECKBOX
import os
import matplotlib
import numpy
import wx
import wx.lib.scrolledpanel
import numpy as np
import pandas as pd

matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotPanel( wx.Panel ) :
    def __init__( self, parent):
        wx.Panel.__init__( self, parent, size=(625, 350))

        #self.figure = matplotlib.figure.Figure(facecolor="white", figsize=(6,6))
        
        self.mainBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #self.figureBox = wx.StaticBox(self, label='Graph box')
        #self.figureBoxSizer = wx.StaticBoxSizer(self.figureBox, wx.HORIZONTAL)

        #self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg( self, -1, self.figure )
        #self.axes = self.figure.add_subplot(111)
        #self.axes.grid(True, color="gray")
        #self.axes.set_xbound( (0,5) )
        #self.axes.set_ybound( (3,80) )
        #self.axes.set_xlabel( "X Var" )
        #self.axes.set_ylabel( "Y Var" )
        #self.axes.grid(True, color="gray")

        #self.figureBoxSizer.Add(self.canvas, flag=wx.ALL, border=5)

        self.menuBox = wx.StaticBox(self, label='Menu')
        self.menuBoxSizer = wx.StaticBoxSizer(self.menuBox, wx.HORIZONTAL)

        self.xBox = wx.StaticBox(self, label='X parameters')
        self.xBoxSizer = wx.StaticBoxSizer(self.xBox, wx.VERTICAL)
        self.yBox = wx.StaticBox(self, label='Y parameters')
        self.yBoxSizer = wx.StaticBoxSizer(self.yBox, wx.VERTICAL)

        self.textX1 = wx.StaticText(self, label = "X Variable")#, pos = (10, 285))
        self.textY1 = wx.StaticText(self, label = "Y Variable")#, pos = (10, 310))  
    
        variables = ['1', '2']
        relationsX = ['3', '4']
        relationsY = ['5', '6']
        
        self.dropDownX1 = wx.ComboBox(self, choices = variables)#, pos = (70, 590))
        self.dropDownY1 = wx.ComboBox(self, choices = variables)#, pos = (70, 615))

        self.textXRelations = wx.StaticText(self, label = "X Transformation")#, pos = (200, 285))
        self.textYRelations = wx.StaticText(self, label = "Y Transformation")#, pos = (200, 310))

        self.dropDownXRelations1 = wx.ComboBox(self, choices = relationsX)#, pos = (340, 270))
        self.dropDownYRelations1 = wx.ComboBox(self, choices = relationsY)#, pos = (340, 295))
        
        self.xBoxSizer.Add(self.textX1)#, flag=wx.ALL|wx.EXPAND, border = 5)
        self.xBoxSizer.Add(self.dropDownX1)#, flag=wx.ALL|wx.EXPAND, border = 5)
        self.xBoxSizer.Add(self.textXRelations)#, flag=wx.ALL|wx.EXPAND, border = 5)
        self.xBoxSizer.Add(self.dropDownXRelations1)#, flag=wx.ALL|wx.EXPAND, border = 5)
        self.yBoxSizer.Add(self.textY1)#, flag=wx.ALL|wx.EXPAND, border = 5)
        self.yBoxSizer.Add(self.dropDownY1)#, flag=wx.ALL|wx.EXPAND, border = 5)
        self.yBoxSizer.Add(self.textYRelations)#, flag=wx.ALL|wx.EXPAND, border = 5)
        self.yBoxSizer.Add(self.dropDownYRelations1)#, flag=wx.ALL|wx.EXPAND, border = 5)

        self.menuBoxSizer.Add(self.yBoxSizer)#, flag=wx.ALL|wx.EXPAND, border = 5)
        self.menuBoxSizer.Add(self.xBoxSizer)#, flag=wx.ALL|wx.EXPAND, border = 5)

        #self.mainBoxSizer.Add(self.figureBoxSizer, flag=wx.ALL|wx.EXPAND, border = 5)

class MainWindow(wx.Frame):
    def __init__(self, parent):
        self.app = wx.App()
        wx.Frame.__init__(self, parent, title="Database Variable graphing", size=(500,300))
        self.mainWindowBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.firstRowBox = wx.StaticBox(self, label='Upper box')
        self.firstRowBoxSizer = wx.StaticBoxSizer(self.firstRowBox, wx.VERTICAL)

        self.Box11 = wx.StaticBox(self, label='Graph 1')
        self.BoxSizer11 = wx.StaticBoxSizer(self.Box11, wx.HORIZONTAL)
        #self.Box12 = wx.StaticBox(self, label='Graph 2')
        #self.BoxSizer12 = wx.StaticBoxSizer(self.Box12, wx.HORIZONTAL)
        self.firstRowBoxSizer.Add(self.BoxSizer11, flag=wx.ALL|wx.EXPAND, border = 5)
        #self.firstRowBoxSizer.Add(self.BoxSizer12, flag=wx.ALL|wx.EXPAND, border = 5)

        #self.secondRowBox = wx.StaticBox(self, label='Lower box')
        #self.secondRowBoxSizer = wx.StaticBoxSizer(self.secondRowBox, wx.VERTICAL)

        #self.Box21 = wx.StaticBox(self, label='Graph 3')
        #self.BoxSizer21 = wx.StaticBoxSizer(self.Box21, wx.HORIZONTAL)
        #self.Box22 = wx.StaticBox(self, label='The rest')
        #self.BoxSizer22 = wx.StaticBoxSizer(self.Box22, wx.HORIZONTAL)
        #self.secondRowBoxSizer.Add(self.BoxSizer21, flag=wx.ALL|wx.EXPAND, border = 5)
        #self.secondRowBoxSizer.Add(self.BoxSizer22, flag=wx.ALL|wx.EXPAND, border = 5)

        self.graph1 = PlotPanel(self)#, position=(10, 10))
        self.BoxSizer11.Add(self.graph1, flag=wx.ALL|wx.EXPAND, border = 5)
        #self.graph2 = PlotPanel(self)#, position=(700, 10))
        #self.BoxSizer12.Add(self.graph2, flag=wx.ALL|wx.EXPAND, border = 5)
        #self.graph3 = PlotPanel(self)#, position=(10, 400))
        #self.BoxSizer21.Add(self.graph3, flag=wx.ALL|wx.EXPAND, border = 5)

        self.mainWindowBoxSizer.Add(self.firstRowBoxSizer, flag=wx.ALL|wx.EXPAND, border = 5)
        #self.mainWindowBoxSizer.Add(self.secondRowBoxSizer, flag=wx.ALL|wx.EXPAND, border = 5)

        self.Show()

app = wx.App(False)
win = MainWindow(None)
app.MainLoop()
