import sys
sys.path.insert(0, '../../database')
import os
# i found the following version more portable
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.path[0])),'database')) # goes 2 level up
from communicate_database import getEntireColumn
import matplotlib
import numpy
import wx
import numpy as np
import pandas as pd

matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotPanel( wx.Panel ) :
    def __init__( self, parent, position, xVar, yVar ) :
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
        #self.XData = self.getX()
        #self.YData = self.getY()
    #-----------------------------------------------------------------------------------
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

class MainWindow(wx.Frame):
    def __init__(self, parent):
        self.app = wx.App()
        wx.Frame.__init__(self, parent, title="Database Variable graphing", size=(2000,1200))
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

        self.textX1 = wx.StaticText(self, label = "X Variable", pos = (10, 275))
        self.textY1 = wx.StaticText(self, label = "Y Variable", pos = (10, 300))  
        self.textX2 = wx.StaticText(self, label = "X Variable", pos = (10, 595))
        self.textY2 = wx.StaticText(self, label = "Y Variable", pos = (10, 620))
        #self.textX3 = wx.StaticText(self, label = "X Variable", pos = ())
        #self.textY3 = wx.StaticText(self, label = "Y Variable"), pos = ())

        self.dropDownX1 = wx.ComboBox(self, choices = variables, pos = (70, 270))
        self.dropDownY1 = wx.ComboBox(self, choices = variables, pos = (70, 295))
        self.dropDownX2 = wx.ComboBox(self, choices = variables, pos = (70, 590))
        self.dropDownY2 = wx.ComboBox(self, choices = variables, pos = (70, 615))
        #self.dropDownX3 = wx.ComboBox(self, choices = variables, pos = ())
        #self.dropDownY3 = wx.ComboBox(self, choices = variables, pos = ())

        self.textXRelations1 = wx.StaticText(self, label = "X Transformation", pos = (240, 275))
        self.textYRelations1 = wx.StaticText(self, label = "Y Transformation", pos = (240, 300))
        self.textXRelations2 = wx.StaticText(self, label = "X Transformation", pos = (240, 595))
        self.textYRelations2 = wx.StaticText(self, label = "Y Transformation", pos = (240, 620))
        #self.textXRelations3 = wx.StaticText(self, label = "X Transformation", pos = ())
        #self.textYRelations3 = wx.StaticText(self, label = "Y Transformation", pos = ())

        self.dropDownXRelations1 = wx.ComboBox(self, choices = relationsX, pos = (340, 270))
        self.dropDownYRelations1 = wx.ComboBox(self, choices = relationsY, pos = (340, 295))
        self.dropDownXRelations2 = wx.ComboBox(self, choices = relationsX, pos = (340, 590))
        self.dropDownYRelations2 = wx.ComboBox(self, choices = relationsY, pos = (340, 615))
        #self.dropDownXRelations3 = wx.ComboBox(self, choices = relationsX, pos = ())
        #self.dropDownYRelations3 = wx.ComboBox(self, choices = relationsY, pos = ())
        
        selectionX1 = self.dropDownX1
        selectionY1 = self.dropDownY1
        
        self.dropDownX1.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        self.dropDownY1.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        self.dropDownX2.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        self.dropDownY2.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        
        self.updateButton1 = wx.Button(self, label="Update Data", pos=(1000, 330))
        self.boundBoxX = wx.StaticText(self, label="X bounds", pos=(660, 335))
        #self.lowerBoundX = wx.text
        self.boundBoxY = wx.StaticText(self, label="Y bounds", pos=(660, 360))

        #self.export   = wx.Button(self, label="Stop")
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer()
        self.graph1 = PlotPanel( self, position=(10, 10), xVar=selectionX1.GetStringSelection(), 
            yVar=selectionY1.GetStringSelection())
        self.graph2 = PlotPanel( self, position=(10, 330), xVar=selectionX1.GetStringSelection(), 
            yVar=selectionY1.GetStringSelection())
        self.panel.SetSizerAndFit(self.sizer)
        
        self.exportDataButton1 = wx.Button(self, label="Copy Data", pos=(410, 295))
        self.exportDataButton1.Bind(event = wx.EVT_BUTTON, handler = self.copyToClipboard(graph = self.graph1, 
            dropDownX = self.dropDownX1, dropDownY = self.dropDownY1, event = 0))
        self.exportDataButton2 = wx.Button(self, label="Copy Data", pos=(410, 615))
        self.exportDataButton2.Bind(event = wx.EVT_BUTTON, handler = self.copyToClipboard(graph = self.graph2,
            dropDownX = self.dropDownX2, dropDownY = self.dropDownY2, event = 0))

        self.updateDropDown(0)

        self.Show()

    def updateDropDown(self, event) :
        self.graph1.axes.cla()       
        self.graph1.axes.set_title(self.dropDownX1.GetStringSelection()
            + " vs. " + self.dropDownY1.GetStringSelection()) 
        self.graph1.axes.set_xlabel(self.dropDownX1.GetStringSelection()) ## change later
        self.graph1.axes.set_ylabel(self.dropDownY1.GetStringSelection())
        if self.dropDownY1.GetStringSelection() != "" and self.dropDownY1.GetStringSelection() != "":
            self.graph1.axes.plot(self.graph1.changeVar(self.dropDownX1.GetStringSelection()),
               self.graph1.changeVar(self.dropDownY1.GetStringSelection()), marker ='o', ls = '')
            self.graph1.axes.plot([],[])
        else :
            self.graph1.axes.plot([],[])
        self.graph1.canvas.draw()

        self.graph2.axes.cla()       
        self.graph2.axes.set_title(self.dropDownX2.GetStringSelection()
            + " vs. " + self.dropDownY2.GetStringSelection()) 
        self.graph2.axes.set_xlabel(self.dropDownX2.GetStringSelection()) ## change later
        self.graph2.axes.set_ylabel(self.dropDownY2.GetStringSelection())
        if self.dropDownY2.GetStringSelection() != "" and self.dropDownY2.GetStringSelection() != "":
            self.graph2.axes.plot(self.graph2.changeVar(self.dropDownX2.GetStringSelection()),
               self.graph2.changeVar(self.dropDownY2.GetStringSelection()), marker ='o', ls = '')
            self.graph2.axes.plot([],[])
        else :
            self.graph2.axes.plot([],[])
        self.graph2.canvas.draw()

        #self.graph3.axes.cla()       
        #self.graph3.axes.set_title(self.dropDownX3.GetStringSelection()
        #    + " vs. " + self.dropDownY3.GetStringSelection()) 
        #self.graph3.axes.set_xlabel(self.dropDownX3.GetStringSelection()) ## change later
        #self.graph3.axes.set_ylabel(self.dropDownY3.GetStringSelection())
        #if self.dropDownY3.GetStringSelection() != "" and self.dropDownY3.GetStringSelection() != "":
         #   self.graph3.axes.plot(self.graph3.changeVar(self.dropDownX3.GetStringSelection()),
          #     self.graph3.changeVar(self.dropDownY3.GetStringSelection()), marker ='o', ls = '')
           # self.graph3.axes.plot([],[])
        #else :
         #   self.graph3.axes.plot([],[])
        #self.graph3.canvas.draw()
    
    def applyTransformation(self) : # use for plotting different 
        xChoice = self.dropDownXRelations1.GetStringSelection()
        yChoice = self.dropDownYRelations1.GetStringSelection()
        #if (xChoice != '' & 'x') :
        
        #if (yChoice != '' & 'y') :
            #if (yChoice == 'log(y)') :
                
            #elif (yChoice == 'y^2') :
            
            #elif (yChoice == 'ln(y)') :
    # Modify this to check if button is pressed then save to clipboard
    def copyToClipboard(self, graph, dropDownX, dropDownY, event) :
        dictionary = {'x': graph.changeVar(dropDownX.GetStringSelection()), 
            'y': graph.changeVar(dropDownY.GetStringSelection())}
        ds = pd.DataFrame(dictionary)
        if (dropDownY != '' and dropDownX != '') :  
            ds.to_clipboard()


app = wx.App(False)
win = MainWindow(None)
app.MainLoop()
