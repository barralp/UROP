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


class MyConfigurationBoxSizer(wx.StaticBoxSizer):
    def __init__(self, parentPanel, label = 'Configuration'):
        configurationBox = wx.StaticBox(parentPanel, label = label)
        super(MyConfigurationBoxSizer, self).__init__(configurationBox, wx.VERTICAL)
        self.panel = parentPanel
        self.init_configurationBox_cameraBox()
        self.init_configurationBox_fittingParametersBox()
        self.init_configurationBox_readingBox()
        # self.init_configurationBox_fluorescenceMonitorBox()
        
    def init_configurationBox_cameraBox(self):
        ## camera configuration
        cameraConfigBox = wx.StaticBox(self.panel, label = 'Camera')
        cameraConfigBoxSizer = wx.StaticBoxSizer(cameraConfigBox, wx.VERTICAL)
        
        # Camera Type
        cameraTypeList = ["FLIR", "Andor", "Other"] 
                # plan for another type of camera in case it needs a reading
                # from folders as both FLIR and Andor are planned to read directly
        self.cameraTypeRadioBox = wx.RadioBox(self.panel, 
                                              label = 'Type',
                                              choices = cameraTypeList,
                                              style = wx.RA_SPECIFY_COLS) 
        
        # camera position (for FLIR camera)
        cameraPositionList = ["Vertical", "Horizontal", "Test"]
        self.cameraPositionRadioBox = wx.RadioBox(self.panel, 
                                              label = 'Positon',
                                              choices = cameraPositionList,
                                              style = wx.RA_SPECIFY_COLS) 

        self.saveDummyCheckBox = wx.CheckBox(self.panel, label="Save dummy")
        # self.checkBoxSaveDummy.SetValue(False)

        self.FLIRToggleButton = wx.ToggleButton(self.panel, label = 'Start FLIR camera')

        cameraConfigBoxSizer.Add(self.cameraTypeRadioBox, flag=wx.ALL| wx.EXPAND, border = 5)
        cameraConfigBoxSizer.Add(self.cameraPositionRadioBox, flag=wx.ALL| wx.EXPAND, border = 5)
        cameraConfigBoxSizer.Add(self.saveDummyCheckBox, border=5)
        cameraConfigBoxSizer.Add(self.FLIRToggleButton, flag = wx.ALL, border = 5)
        
        self.Add(cameraConfigBoxSizer, flag=wx.ALL| wx.EXPAND, border = 5)
    
    def init_configurationBox_fittingParametersBox(self):
        fittingParametersBox = wx.StaticBox(self.panel, label = 'Fitting parameters')
        fittingParametersBoxSizer = wx.StaticBoxSizer(fittingParametersBox, wx.VERTICAL)
        
        # Type of fit: statistics
        fittingTypeList = ["Fermion", "Boson", "Gaussian"]
        self.fittingTypeRadioBox = wx.RadioBox(self.panel, 
                                              label = 'Type of statistics',
                                              choices = fittingTypeList,
                                              style = wx.RA_SPECIFY_COLS) 
        
        # Type of fit: normalization
        self.normalizationCheckBox = wx.CheckBox(
            self.panel, label="Normalization (matching " + u"\u03BC" + " , " + u"\u03C3"+ " of atom shot && ref.)")
        self.displayRadialAvgCheckBox = wx.CheckBox(
            self.panel, label="Display radially averaged profile")
        
        fittingParametersBoxSizer.Add(self.fittingTypeRadioBox, flag=wx.ALL| wx.EXPAND, border = 5)
        fittingParametersBoxSizer.Add(self.normalizationCheckBox, flag = wx.ALL | wx.EXPAND, border = 5)
        fittingParametersBoxSizer.Add(self.displayRadialAvgCheckBox, flag = wx.ALL | wx.EXPAND, border = 5)
        self.Add(fittingParametersBoxSizer, 0, wx.ALL|wx.EXPAND, 5)

    def init_configurationBox_readingBox(self):
        readingBox = wx.StaticBox(self.panel, label = 'Reading')
        readingBoxSizer = wx.StaticBoxSizer(readingBox,  wx.VERTICAL)

        self.autoReadToggleButton = wx.Button(self.panel, label = 'Start Auto Read')
            # Should disable the auto read button if the camera used allows direct reading
        readingBoxSizer.Add(self.autoReadToggleButton, flag=wx.ALL|wx.EXPAND, border= 5)
        self.Add(readingBoxSizer, 0, wx.ALL|wx.EXPAND, 5)
    
    def setFLIRCameraButton(self):
        if self.autoReadToggleButton.GetLabel() == 'Start FLIR camera':
            self.autoReadToggleButton.SetLabel('Stop FLIR camera')
        else:
            self.autoReadToggleButton.SetLabel('Start FLIR camera')
            
    def setAutoReadButton(self):
        if self.autoReadToggleButton.GetLabel() == 'Start Auto Read':
            self.autoReadToggleButton.SetLabel('Stop Auto Read')
        else:
            self.autoReadToggleButton.SetLabel('Start Auto Read')
