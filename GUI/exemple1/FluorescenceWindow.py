#!/usr/bin/python
# -*- coding: utf-8 -*-
# inspired by the snippet code provided on https://wiki.wxpython.org/ModelViewPresenter

#####WX IMPORTS#####
#wx- GUI toolkit for the Python programming language. wxPython can be used  to create graphical user interfaces (GUI).
import wx

#FigureCanvas- the FigureCanvas contains the figure and does event handling.
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#I honestlt can't find this in documentation.

import numpy as np

#Figure- provides the top-level Artist, the Figure, which contains all the plot elements.
from matplotlib.figure import Figure


class MyFluorescenceBoxSizer(wx.StaticBoxSizer):
    def __init__(self, parentPanel, label = 'Fluorescence monitor'):
        fluorescenceBox = wx.StaticBox(parentPanel, label = label)
        super(MyFluorescenceBoxSizer, self).__init__(fluorescenceBox, wx.VERTICAL)
        self.panel = parentPanel

        self.snapButton = wx.Button(self.panel, label = 'Snap')
        self.fluorescenceButton = wx.Button(self.panel, label = 'Turn On')
        self.Add(self.snapButton, flag=wx.ALL|wx.EXPAND, border= 5)
        self.Add(self.fluorescenceButton, flag=wx.ALL|wx.EXPAND, border= 5)
        
        fluorescenceButtonsBox = wx.BoxSizer(wx.HORIZONTAL)
        fluorescenceButtonsBox.Add(self.snapButton, flag = wx.ALL, border = 5)
        fluorescenceButtonsBox.Add(self.fluorescenceButton, flag = wx.ALL, border = 5)
        
        flurorescenceNCountBox = wx.BoxSizer(wx.HORIZONTAL) # wx.ALIGN_LEFT
        fluorescenceNumberLabel = wx.StaticText(self.panel, label='Total nCount: ')
        self.fluorescenceNumberText = wx.TextCtrl(self.panel,  style=wx.TE_READONLY|wx.TE_CENTRE, size=(100,34))
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.fluorescenceNumberText.SetFont(font)
        flurorescenceNCountBox.Add(fluorescenceNumberLabel, flag = wx.ALL, border = 5)
        flurorescenceNCountBox.Add(self.fluorescenceNumberText, flag = wx.ALL, border = 5)
        self.Add(flurorescenceNCountBox, flag=wx.ALL|wx.EXPAND, border= 5)

        self.figure_fluorescence = Figure(figsize = (2,2))
        self.axes_fluorescence = self.figure_fluorescence.add_subplot(111)
        self.axes_fluorescence.set_title('Fluorescence count', fontsize=12)
        for label in (self.axes_fluorescence.get_xticklabels() + self.axes_fluorescence.get_yticklabels()):
            label.set_fontsize(10)
        self.linePlot_fluorescence, = self.axes_fluorescence.plot(np.zeros(20))
        self.canvas_fluorescence = FigureCanvas(self.panel, -1, self.figure_fluorescence)
        self.Add(self.canvas_fluorescence, flag=wx.ALL|wx.EXPAND, border=5)
    
    def setFluorescenceButton(self):
        if self.fluorescenceButton.GetLabel() == 'Turn On':
            self.fluorescenceButton.SetLabel('Turn Off')
        else:
            self.fluorescenceButton.SetLabel('Turn On')
    
    def setFluorescenceNCount(self, nCount):
        self.fluorescenceNumberText.SetValue(str(nCount))
        
    def setFluorescenceGraph(self, nCountList):
        xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.axes_fluorescence.clear()
        self.axes_fluorescence.plot(xdata, self.nCountList)
        self.canvas_fluorescence.draw()
        self.axes_fluorescence.relim()
        self.axes_fluorescence.autoscale_view()