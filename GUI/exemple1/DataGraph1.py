import sys
sys.path.insert(0, '../../database')
from communicate_database import getAMDuration, getAMFreq, getASPower, getASPowermW, getASPowermW2, getBigZ, getBlinckingDuration, getBlinckingFreq, getBlinckingLength, getBlinckingTime, getCameraFudgeTime, getCompHoldTime, getCompLevel, getCompLevel2, getCompTime, getCompTime2, getCompX, getCompXEarth, getCompY, getCompYEarth, getCompZ, getCompZ2, getCompZEarth, getDopplerCoolFreq, getDummy, getEvap1CompZ, getEvap1EndGradient, getEvap2Factor, getEvap5BigZ, getEvapEndGradient, getEvapGradient1, getEvapGradient2, getEvapGradient3, getEvapGradientInit, getEvapScan, getEvapTime1, getEvapTime2, getEvapTime3, getEvapTime4, getEvapTime5, getEvapTime6, getFeshbachCurrent, getFinalBField, getFinalODT1, getFinalYComp, getFreq1, getFreq2, getFreq3, getFreq4, getFreq5, getFreqCompTime2, getImageTime, getImgFreq, getInTrapCoolFreq, getInTrapCoolTime, getIodineFreq, getIterationCount, getIterationNum, getLevel1, getLevel2, getLevel3, getLevel4, getLevel5, getLoadCurrent, getLoadTime, getLossTime, getMOTCompFreq, getMOTCompFreq2, getMOTCurrentAmps, getMOTLevel, getMOTLoadCurrentAmps, getMolassesLevel, getMotLoadFreq, getODT1Evap1End, getODT1Final, getODT1Init, getODT2Evap1End, getODT2Final, getODT2Init, getODTCompX, getODTCompY, getODTCompZ, getODTHoldTime, getODTLoad_MOTFreq, getODTLoad_MOT_Freq, getODTMolasses, getODTMolassesZField, getODTRamp, getODTRampUp, getODTTOFBigZ, getODTTOFGradient, getPumpTime, getPumpingFreq, getRunID, getRunningCounter, getSGOn, getSGOn2, getTCFreq, getTOF, getTau, getTime, getTimeStamp, getTotalExp, getVar60, getWaitTime, getWee, getZSPower
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
        data = []
        if (selection == 'Run ID') :
            data = getRunID()
        elif (selection == 'Iteration Num') :
            data = getIterationNum()
        elif (selection == 'Iteration Count') :
            data = getIterationCount()
        elif (selection == 'Running Counter') :
            data = getRunningCounter()
        elif (selection == 'TOF') :
            data = getTOF()
        elif (selection == 'Comp Level') :
            data = getCompLevel()
        elif (selection == 'Img Freq') :
            data = getImgFreq()
        elif (selection == 'Dummy') :
            data = getDummy()
        elif (selection == 'Iodine Freq') :
            data = getIodineFreq()
        elif (selection == 'Final B Field') :
            data = getFinalBField()
        elif (selection == 'Camera Fudge Time') :
            data = getCameraFudgeTime()
        elif (selection == 'Load Time') :
            data = getLoadTime()
        elif (selection == 'Comp Time') :
            data = getCompTime()
        elif (selection == 'Load Current') :
            data = getLoadCurrent()
        elif (selection == 'Time Stamp') :
            data = getTimeStamp()
        elif (selection == 'Wee') :
            data = getWee()
        elif (selection == 'Mot Load Freq') :
            data = getMotLoadFreq()
        elif (selection == 'Mot Comp Freq') :
            data = getMOTCompFreq()
        elif (selection == 'Time') :
            data = getTime()
        elif (selection == 'ZS Power') :
            data = getZSPower()
        elif (selection == 'Image Time') :
            data = getImageTime()
        elif (selection == 'MOT Level') :
            data = getMOTLevel()
        elif (selection == 'Comp X') :
            data = getCompX()
        elif (selection == 'Comp Y') :
            data = getCompY()
        elif (selection == 'Loss Time') :
            data = getLossTime()
        elif (selection == 'TC Freq') :
            data = getTCFreq()
        elif (selection == 'Comp Z') :
            data = getCompZ()
        elif (selection == 'MOT Current Amps') :
            data = getMOTCurrentAmps()
        elif (selection == 'MOT Load Current Amps') :
            data = getMOTLoadCurrentAmps()
        elif (selection == 'Comp Time 2') :
            data = getCompTime2()
        elif (selection == 'Comp Level 2') :
            data = getCompLevel2()
        elif (selection == 'MOT Comp Freq 2') :
            data = getMOTCompFreq2()
        elif (selection == 'Freq Comp Time 2') :
            data = getFreqCompTime2()
        elif (selection == 'Final Y Comp') :
            data = getFinalYComp()
        elif (selection == 'Comp Hold Time') :
            data = getCompHoldTime()
        elif (selection == 'Wait Time') :
            data = getWaitTime()
        elif (selection == 'AS Power') :
            data = getASPower()
        elif (selection == 'AS Power mW') :
            data = getASPowermW()
        elif (selection == 'AS Power mW 2') :
            data = getASPowermW2()
        elif (selection == 'Level 1') :
            data = getLevel1()
        elif (selection == 'Level 2') :
            data = getLevel2()
        elif (selection == 'Level 3') :
            data = getLevel3()
        elif (selection == 'Level 4') :
            data = getLevel4()
        elif (selection == 'Level 5') :
            data = getLevel5()
        elif (selection == 'Freq 1') :
            data = getFreq1()
        elif (selection == 'Freq 2') :
            data = getFreq2()
        elif (selection == 'Freq 3') :
            data = getFreq3()
        elif (selection == 'Freq 4') :
            data = getFreq4()
        elif (selection == 'Freq 5') :
            data = getFreq5()
        elif (selection == 'ODT Ramp') :
            data = getODTRamp()
        elif (selection == 'ODT Hold Time') :
            data = getODTHoldTime()
        elif (selection == 'ODT 1 Final') :
            data = getODT1Final()
        elif (selection == 'ODT 2 Final') :
            data = getODT2Final()
        elif (selection == 'Evap Time 2') :
            data = getEvapTime2()
        elif (selection == 'Evap Time 1') :
            data = getEvapTime1()
        elif (selection == 'Evap Time 3') :
            data = getEvapTime3()
        elif (selection == 'Big Z') :
            data = getBigZ()
        elif (selection == 'SG On') :
            data = getSGOn()
        elif (selection == 'SG On 2') :
            data = getSGOn2()
        elif (selection == 'Pump Time') :
            data = getPumpTime()
        elif (selection == 'Doppler Cool Freq') :
            data = getDopplerCoolFreq()
        elif (selection == 'ODT 1 Init') :
            data = getODT1Init()
        elif (selection == 'ODT 1 Evap 1 End') :
            data = getODT1Evap1End()
        elif (selection == 'ODT 2 Init') :
            data = getODT2Init()
        elif (selection == 'ODT 2 Evap 1 End') :
            data = getODT2Evap1End()
        elif (selection == 'Feshbach Current') :
            data = getFeshbachCurrent()
        elif (selection == 'Evap Time 4') :
            data = getEvapTime4()
        elif (selection == 'AM Freq') :
            data = getAMFreq()
        elif (selection == 'AM Duration') :
            data = getAMDuration()
        elif (selection == 'ODT Ramp Up') :
            data = getODTRampUp()
        elif (selection == 'Evap 2 Factor') :
            data = getEvap2Factor()
        elif (selection == 'Tau') :
            data = getTau()
        elif (selection == 'Total Exp') :
            data = getTotalExp()
        elif (selection == 'In Trap Cool Freq') :
            data = getInTrapCoolFreq()
        elif (selection == 'In Trap Cool Time') :
            data = getInTrapCoolTime()
        elif (selection == 'Evap Time 5') :
            data = getEvapTime5()
        elif (selection == 'Evap 1 End Gradient') :
            data = getEvap1EndGradient()
        elif (selection == 'Var 60') :
            data = getVar60()
        elif (selection == 'Evap Scan') :
            data = getEvapScan()
        elif (selection == 'Evap Gradient Init') :
            data = getEvapGradientInit()
        elif (selection == 'Evap Gradient 1') :
            data = getEvapGradient1()
        elif (selection == 'Evap Gradient 2') :
            data = getEvapGradient2()
        elif (selection == 'Evap Gradient 3') :
            data = getEvapGradient3()
        elif (selection == 'Evap End Gradient') :
            data = getEvapEndGradient()
        elif (selection == 'ODT TOF Gradient') :
            data = getODTTOFGradient()
        elif (selection == 'ODT TOF Big Z') :
            data = getODTTOFBigZ()
        elif (selection == 'Evap 5 Big Z') :
            data = getEvap5BigZ()
        elif (selection == 'Final ODT 1') :
            data = getFinalODT1()
        elif (selection == 'Blincking Time') :
            data = getBlinckingTime()
        elif (selection == 'Blincking Freq') :
            data = getBlinckingFreq()
        elif (selection == 'Molasses Level') :
            data = getMolassesLevel()
        elif (selection == 'Blincking Duration') :
            data = getBlinckingDuration()
        elif (selection == 'ODT Molasses') :
            data = getODTMolasses()
        elif (selection == 'ODT Molasses Z Field') :
            data = getODTMolassesZField()
        elif (selection == 'ODT Load_MOT_Freq') :
            data = getODTLoad_MOT_Freq()
        elif (selection == 'ODT Comp X') :
            data = getODTCompX()
        elif (selection == 'ODT Comp Y') :
            data = getODTCompY()
        elif (selection == 'ODT Comp Z') :
            data = getODTCompZ()
        elif (selection == 'Blincking Length') :
            data = getBlinckingLength()
        elif (selection == 'ODT Load_MOT Freq') :
            data = getODTLoad_MOTFreq()
        elif (selection == 'Evap 1 Comp Z') :
            data = getEvap1CompZ()
        elif (selection == 'Pumping Freq') :
            data = getPumpingFreq()
        elif (selection == 'Comp X Earth') :
            data = getCompXEarth()
        elif (selection == 'Comp Y Earth') :
            data = getCompYEarth()
        elif (selection == 'Comp Z Earth') :
            data = getCompZEarth()
        elif (selection == 'Evap Time 6') :
            data = getEvapTime6()
        elif (selection == 'Comp Z 2') :
            data = getCompZ2()
        else :
            data = []
            print('no matching')
        return data

class MainWindow(wx.Frame):
    def __init__(self, parent):
        self.app = wx.App()
        wx.Frame.__init__(self, parent, title="Database Variable Graphing", size=(1000,600))
        variables = ['Run ID', 'Iteration Num', 'Iteration Count', 'Running Counter', 
            'TOF', 'Comp Level', 'Img Freq', 'Dummy', 'Iodine Freq', 'Final B Field',
            'Camera Fudge Time', 'Load Time', 'Comp Time', 'Load Current', 'Time Stamp',
            'Wee', 'Mot Load Freq', 'Mot Comp Freq', 'Time', 'ZS Power', 'Image Time', 
            'MOT Level', 'Comp X', 'Comp Y', 'Loss Time', 'TC Freq', 'Comp Z', 'MOT Current Amps',
            'MOT Load Current Amps', 'Comp Time 2', 'Comp Level 2', 'MOT Comp Freq 2', 'Freq Comp Time 2',
            'Final Y Comp', 'Comp Hold Time', 'Wait Time', 'AS Power', 'AS Power mW', 'AS Power mW 2',
            'MOT Current 2', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Freq 1', 'Freq 2',
            'Freq 3', 'Freq 4', 'Freq 5', 'ODT Ramp', 'ODT Hold Time', 'ODT 1 Final', 'ODT 2 Final',
            'Evap Time 2', 'Evap Time 1', 'Evap Time 3', 'Big Z', 'SG On', 'SG On 2', 'Pump Time', 
            'Doppler Cool Freq', 'ODT 1 Init', 'ODT 1 Evap 1 End', 'ODT 2 Init', 'ODT 2 Evap 1 End',
            'Feshbach Current', 'Evap Time 4', 'AM Freq', 'AM Duration', 'ODT Ramp Up', 'Evap 2 Factor',
            'Tau', 'Total Exp', 'In Trap Cool Freq', 'In Trap Cool Time', 'Evap Time 5', 'Evap 1 End Gradient',
            'Var 60', 'Evap Scan', 'Evap Gradient Init', 'Evap Gradient 1', 'Evap Gradient 2',
            'Evap Gradient 3', 'Evap End Gradient', 'ODT TOF Gradient', 'ODT TOF Big Z', 
            'Evap 5 Big Z', 'Final ODT 1', 'Blincking Time', 'Blincking Freq', 'Molasses Level',
            'Blincking Duration', 'ODT Molasses', 'ODT Molasses Z Field', 'ODT Load MOT Freq',
            'ODT Comp X', 'ODT Comp Y', 'ODT Comp Z', 'Blincking Length', 'ODT Load MOT Freq', 
            'Evap 1 Comp Z', 'Pumping Freq', 'Comp X Earth', 'Comp Y Earth', 'Comp Z Earth',
            'Evap Time 6', 'Comp Z 2']
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
        #self.button = wx.Button(self.panel, label="Update")
        #self.stop   = wx.Button(self.panel, label="Stop")
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer()
        #self.sizer.Add(self.button)
        #self.sizer.Add(self.stop)
        self.graph = PlotPanel( self, position=(20, 50), xVar=selectionX.GetStringSelection(), 
            yVar=selectionY.GetStringSelection() )
        self.panel.SetSizerAndFit(self.sizer)
        self.updateDropDown(0)
        self.Show()

        # Use EVT_CHAR_HOOK on Frame insted of wx.EVT_KEY_UP on SpinCtrl
        # to disable "on Enter go to next widget" functionality
        #self.Bind(wx.EVT_CHAR_HOOK, self.OnKey) 
        #self.button.Bind(wx.EVT_BUTTON, self.OnUpdate)
        #self.stop.Bind(wx.EVT_BUTTON, self.OnStop)

    def updateDropDown(self, event) :       
        self.graph.axes.set_title(self.dropDownX.GetStringSelection()
            + " vs. " + self.dropDownY.GetStringSelection()) 
        self.graph.axes.set_xlabel(self.dropDownX.GetStringSelection()) ## change later
        self.graph.axes.set_ylabel(self.dropDownY.GetStringSelection())
        #self.graph.axes.set_x(self.graph.changeVar(self.dropDownX.GetStringSelection()))
        #self.graph.axes.set_y(self.graph.changeVar(self.dropDownY.GetStringSelection()))
        self.graph.axes.plot(self.graph.changeVar(self.dropDownX.GetStringSelection()),
            self.graph.changeVar(self.dropDownY.GetStringSelection()))
        self.graph.canvas.draw()
        print(getAMDuration())
        print(getAMFreq())




app = wx.App(False)
win = MainWindow(None)
app.MainLoop()