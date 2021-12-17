import sys

from wx.core import EVT_CHECKBOX
sys.path.insert(0, '../../database')
import os
# i found the following version more portable
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.path[0])),'database')) # goes 2 level up
from communicate_database import getEntireColumn
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
    def __init__( self, parent, position) :
        wx.Panel.__init__( self, parent, pos=position, size=(625,250) )
        # initialize matplotlib 
        self.figure = matplotlib.figure.Figure( None, facecolor="white" )
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg( self, -1, self.figure )
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color="gray")
        self.axes.set_xbound( (0,5) )
        self.axes.set_ybound( (3,80) )
        self.axes.set_xlabel( "X Var" ) ## change later
        self.axes.set_ylabel( "Y Var" )
        self.axes.grid(True, color="gray")
        self._SetSize()
        self.Bind( wx.EVT_SIZE, self._SetSize )
        variables = ['runID', 'IterationNum', 'IterationCount', 'RunningCounter', 
            'TOF', 'CompLevel', 'ImgFreq', 'dummy', 'IodineFreq', 'FinalBField',
            'CameraFudgeTime', 'LoadTime', 'CompTime', 'LoadCurrent', 'timestamp',
            'wee', 'MotLoadFreq', 'MotCompFreq', 'time', 'ZSPower', 'imageTime', 
            'MOTLevel', 'compx', 'compy', 'LossTime', 'TCFreq', 'compz', 'MOTCurrent_Amps',
            'MOTLoadCurrent_Amps', 'CompTime2', 'CompLevel2', 'MOTCompFreq2', 'FreqCompTime2',
            'FinalYComp', 'CompHoldTime', 'WaitTime', 'ASPower', 'ASPower_mW', 'ASPower_mW_2',
            'MOTCurrent2', 'level1', 'level2', 'level3', 'level4', 'level5', 'freq1', 'freq2',
            'freq3', 'freq4', 'freq5', 'ODT_Ramp', 'ODTHoldTime', 'ODT1_Final', 'ODT2_Final',
            'EvapTime2', 'EvapTime1', 'EvapTime3', 'BigZ', 'SGOn', 'SGOn2', 'PumpTime', 
            'DopplerCoolFreq', 'ODT1_Init', 'ODT1_Evap1_End', 'ODT2_Init', 'ODT2_Evap1_End',
            'FeshbachCurrent', 'EvapTime4', 'AMFreq', 'AMDuration', 'ODTRampUp', 'Evap2Factor',
            'tau', 'totalExp', 'InTrapCoolFreq', 'InTrapCoolTime', 'EvapTime5', 'Evap1_End_Gradient',
            'Var60', 'EvapScan', 'EvapGradientInit', 'Evap_Gradient1', 'Evap_Gradient2',
            'Evap_Gradient3', 'Evap_End_Gradient', 'ODT_TOF_Gradient', 'ODT_TOF_BigZ', 
            'Evap5_BigZ', 'FinalODT1', 'BlinckingTime', 'Blincking_freq', 'Molasses_level',
            'Blincking_duration', 'ODT_Molasses', 'ODT_Molasses_ZField', 'ODTLoad_MOT_Freq',
            'ODTcompx', 'ODTcompy', 'ODTcompz', 'Blinckinglength', 'ODTLoad_MOTFreq', 
            'Evap1_CompZ', 'Pumping_Freq', 'compx_Earth', 'compy_Earth', 'compz_Earth',
            'EvapTime6', 'compz2']
        relationsX = ["x", "log(x)", "x^2", "x^0.5"]
        relationsY = ["y", "log(y)", "y^2", "y^0.5"]

        self.textX = wx.StaticText(self, label = "X Variable", pos = (10, 200))
        self.textY = wx.StaticText(self, label = "Y Variable", pos = (10, 620))

        self.dropDownX = wx.ComboBox(self, choices = variables, pos = (70, 590))
        self.dropDownY = wx.ComboBox(self, choices = variables, pos = (70, 615))

        self.textXRelations = wx.StaticText(self, label = "X Transformation", pos = (240, 275))
        self.textYRelations = wx.StaticText(self, label = "Y Transformation", pos = (240, 300))

        self.dropDownXRelations1 = wx.ComboBox(self, choices = relationsX, pos = (340, 270))
        self.dropDownYRelations1 = wx.ComboBox(self, choices = relationsY, pos = (340, 295))
        
        #selectionX1 = self.dropDownX1
        #selectionY1 = self.dropDownY1
        
        self.dropDownX.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        self.dropDownY.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        #self.dropDownX2.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        #self.dropDownY2.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        
        self.updateButton1 = wx.Button(self, label="Update Data", pos=(1000, 330))
        self.boundBoxX = wx.StaticText(self, label="X bounds", pos=(660, 335))
        #self.lowerBoundX = wx.text
        self.boundBoxY = wx.StaticText(self, label="Y bounds", pos=(660, 360))

        self.export = wx.Button(self, label="Stop")
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer()
        self.panel.SetSizerAndFit(self.sizer)
        
        self.exportDataButton1 = wx.Button(self, label="Copy Data", pos=(410, 295))
        self.exportDataButton1.Bind(wx.EVT_BUTTON, lambda event: self.copyToClipboard(1))
        self.exportDataButton2 = wx.Button(self, label="Copy Data", pos=(410, 615))
        self.exportDataButton2.Bind(wx.EVT_BUTTON, lambda event: self.copyToClipboard(2))

        self.doublePlot1 = wx.CheckBox(self, label="Display Two Plots", pos=(410, 270))
        self.doublePlot1.Bind(event=wx.EVT_CHECKBOX, handler=self.toggleSecondPlot)

        self.updateDropDown(0)

        self.dropDownX = wx.ComboBox(self, choices = [], pos = (70, 270))
        self.dropDownY = wx.ComboBox(self, choices = [], pos = (70, 295))

        self.textX1 = wx.StaticText(self, label = "X Variable", pos = (10, 275))
        self.textY1 = wx.StaticText(self, label = "Y Variable", pos = (10, 300))  

        self.Show()
    #-----------------------------------------------------------------------------------

    def applyTransformation(self, event) : # use for plotting different 
        xChoice = self.dropDownXRelations.GetStringSelection()
        yChoice = self.dropDownYRelations.GetStringSelection()
        #if (xChoice != '' & self.GetDropDownX Y) :
        
        #if (yChoice != '' & 'y') :
            #if (yChoice == 'log(y)') :
                
            #elif (yChoice == 'y^2') :
            
            #elif (yChoice == 'ln(y)') :
    
    # Modify this to check if button is pressed then save to clipboard

    def _SetSize( self, event=None ):
        pixels = self.GetSize() 
        self.SetSize( pixels )
        self.canvas.SetSize( pixels )

        dpi = self.figure.get_dpi()
        self.figure.set_size_inches( float( pixels[0] ) / dpi,float( pixels[1] ) / dpi )
    #------------------------------------------------------------------------------------

    def changeVar(self, selection) :
        if (selection != '') :
            data = getEntireColumn(selection, 'ciceroOut')
        else :
            data = []
            print('no matching')
        return data

    def updateDropDown(self, event) :
        self.axes.cla()  
        dropDownX = self.dropDownX.GetStringSelection()
        dropDownY = self.dropDownY.GetStringSelection()
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

    def copyToClipboardSecond(self, event):
        #event.GetEventObject() = self.ExportDataButtonX
        print(event.GetEventObject())
        dictionary = {'x': self.graph1.changeVar(self.dropDownX.GetStringSelection()), 
            'y': self.graph1.changeVar(self.dropDownY.GetStringSelection())}
        ds = pd.DataFrame(dictionary)
        if (self.dropDownY.GetStringSelection() != '' and self.dropDownX.GetStringSelection() != '') :  
            ds.to_clipboard()

    def createDataFrame(self, dropDownX, dropDownY, graph):
        dictionary = {'x': self.graph.changeVar(dropDownX.GetStringSelection()), 
            'y': self.graph.changeVar(dropDownY.GetStringSelection())}
        df = pd.DataFrame(dictionary)
        return df

    def copyToClipboard(self, index) :
        df = self.createDataFrame(self.dropDownX, self.dropDownY)
    
    def toggleSecondPlot(self, event) :
        checked = self.doublePlot1.Get3StateValue()
        print(checked)
        #if checked:
        #    self.graph1.
        #else :

class MainWindow(wx.Frame):
    def __init__(self, parent):
        self.app = wx.App()
        wx.Frame.__init__(self, parent, title="Database Variable graphing", size=(500,300))
        self.graph1 = PlotPanel(self, position=(10, 10))
        self.graph2 = PlotPanel(self, position=(700, 10))
        self.graph3 = PlotPanel(self, position=(10, 400))
        self.Show()

app = wx.App(False)
win = MainWindow(None)
app.MainLoop()
