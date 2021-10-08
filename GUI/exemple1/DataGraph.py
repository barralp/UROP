import sys
sys.path.insert(0, '../../database')
from communicate_database import getEntireColumn
import matplotlib
import numpy
import wx
import numpy as np
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotPanel( wx.Panel ) :
    def __init__( self, parent, position, xVar, yVar ) :
        wx.Panel.__init__( self, parent, pos=position, size=(800,320) )
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

def returnFuncVar(self) :
    return 0

class MainWindow(wx.Frame):
    def __init__(self, parent):
        self.app = wx.App()
        wx.Frame.__init__(self, parent, title="Database Variable Graphing", size=(1000,600))
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
        self.textX = wx.StaticText(self, label = "X Variable", pos = (20, 380))
        self.textY = wx.StaticText(self, label = "Y Variable", pos = (20, 405))  
        self.dropDownX = wx.ComboBox(self, choices = variables, pos = (80, 375))
        self.dropDownY = wx.ComboBox(self, choices = variables, pos = (80, 400))
        self.dropDownXRelations = wx.ComboBox(self, choices = relationsX, pos = (300, 375))
        self.dropDownYRelations = wx.ComboBox(self, choices = relationsY, pos = (300, 400))
        selectionX = self.dropDownX
        selectionY = self.dropDownY
        self.dropDownX.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        self.dropDownY.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        #self.spin = wx.SpinCtrl(self.panel)
        #self.button = wx.Button(self, label="Update Data", pos=[600, 600])
        #self.export   = wx.Button(self, label="Stop")
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer()
        #self.sizer.Add(self.button)
        #self.sizer.Add(self.stop)
        self.graph = PlotPanel( self, position=(20, 50), xVar=selectionX.GetStringSelection(), 
            yVar=selectionY.GetStringSelection())
        self.panel.SetSizerAndFit(self.sizer)
        self.updateDropDown(0)
        self.Show()

        # Use EVT_CHAR_HOOK on Frame insted of wx.EVT_KEY_UP on SpinCtrl
        # to disable "on Enter go to next widget" functionality
        #self.Bind(wx.EVT_CHAR_HOOK, self.OnKey) 
        #self.button.Bind(wx.EVT_BUTTON, self.OnUpdate)
        #self.stop.Bind(wx.EVT_BUTTON, self.OnStop)

    def updateDropDown(self, event) :
        self.graph.axes.cla()       
        self.graph.axes.set_title(self.dropDownX.GetStringSelection()
            + " vs. " + self.dropDownY.GetStringSelection()) 
        self.graph.axes.set_xlabel(self.dropDownX.GetStringSelection()) ## change later
        self.graph.axes.set_ylabel(self.dropDownY.GetStringSelection())
        #self.graph.axes.set_x(self.graph.changeVar(self.dropDownX.GetStringSelection()))
        #self.graph.axes.set_y(self.graph.changeVar(self.dropDownY.GetStringSelection()))
        if self.dropDownY.GetStringSelection() != "" and self.dropDownY.GetStringSelection() != "":
            self.graph.axes.plot(self.graph.changeVar(self.dropDownX.GetStringSelection()),
               self.graph.changeVar(self.dropDownY.GetStringSelection()), marker ='o', ls = '')
            self.graph.axes.plot([],[])
        else :
            self.graph.axes.plot([],[])
        self.graph.canvas.draw()

app = wx.App(False)
win = MainWindow(None)
app.MainLoop()