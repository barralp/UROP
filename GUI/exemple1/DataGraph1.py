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
    def __init__( self, parent, position ) :
        wx.Panel.__init__( self, parent, pos=position, size=(800,320) )
        # initialize matplotlib 
        self.figure = matplotlib.figure.Figure( None, facecolor="white" )
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg( self, -1, self.figure )
        self.dropDown = wx.ComboBox('Run ID', 'Iteration Num', 'Iteration Count', 'Running Counter', 
        #     'TOF', 'Comp Level', 'Img Freq', 'Dummy', 'Iodine Freq', 'Final B Field',
        #     'Camera Fudge Time', 'Load Time', 'Comp Time', 'Load Current', 'Time Stamp',
        #     'Wee', 'Mot Load Freq', 'Mot Comp Freq', 'Time', 'ZS Power', 'Image Time', 
        #     'MOT Level', 'Comp X', 'Comp Y', 'Loss Time', 'TC Freq', 'Comp Z', 'MOT Current Amps',
        #     'MOT Load Current Amps', 'Comp Time 2', 'Comp Level 2', 'MOT Comp Freq 2', 'Freq Comp Time 2',
        #     'Final Y Comp', 'Comp Hold Time', 'Wait Time', 'AS Power', 'AS Power mW', 'AS Power mW 2',
        #     'MOT Current 2', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Freq 1', 'Freq 2',
        #     'Freq 3', 'Freq 4', 'Freq 5', 'ODT Ramp', 'ODT Hold Time', 'ODT 1 Final', 'ODT 2 Final',
        #     'Evap Time 2', 'Evap Time 1', 'Evap Time 3', 'Big Z', 'SG On', 'SG On 2', 'Pump Time', 
        #     'Doppler Cool Freq', 'ODT 1 Init', 'ODT 1 Evap 1 End', 'ODT 2 Init', 'ODT 2 Evap 1 End',
        #     'Feshbach Current', 'Evap Time 4', 'AM Freq', 'AM Duration', 'ODT Ramp Up', 'Evap 2 Factor',
        #     'Tau', 'Total Exp', 'In Trap Cool Freq', 'In Trap Cool Time', 'Evap Time 5', 'Evap 1 End Gradient',
         'Var 60', 'Evap Scan', 'Evap Gradient Init', 'Evap Gradient 1', 'Evap Gradient 2',
             'Evap Gradient 3', 'Evap End Gradient', 'ODT TOF Gradient', 'ODT TOF Big Z', 
             'Evap 5 Big Z', 'Final ODT 1', 'Blincking Time', 'Blincking Freq', 'Molasses Level',
             'Blincking Duration', 'ODT Molasses', 'ODT Molasses Z Field', 'ODT Load MOT Freq',
             'ODT Comp X', 'ODT Comp Y', 'ODT Comp Z', 'Blincking Length', 'ODT Load MOT Freq', 
             'Evap 1 Comp Z', 'Pumping Freq', 'Comp X Earth', 'Comp Y Earth', 'Comp Z Earth',
        'Evap Time 6', 'Comp Z 2']))
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color="gray")
        self.axes.set_xbound( (0,5) )
        self.axes.set_ybound( (3,80) )
        self.axes.set_xlabel( "" ) ## change later
        self.axes.set_ylabel( "" )
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color="gray")
        self._SetSize()
        self.Bind( wx.EVT_SIZE, self._SetSize )
        self.XData = self.getX()
        self.YData = self.getY()

    #def retrieveData(self, value):
     #   self.TemperatureData.append( value )
      #  length = len(self.TemperatureData)
       # x = self.XData
#        y = self.YData

 #       yMin = round(min(y)) - 2
  #      yMax = round(max(y)) + 2            
    #    self.axes.plot(x,y, "-k")
   #     self.axes.set_ybound( (yMin,yMax) )
      #   self.canvas = FigureCanvas(self, -1, self.figure)

    #-----------------------------------------------------------------------------------
    def _SetSize( self, event=None ):
        pixels = self.GetSize() 
        self.SetSize( pixels )
        self.canvas.SetSize( pixels )

        dpi = self.figure.get_dpi()
        self.figure.set_size_inches( float( pixels[0] ) / dpi,float( pixels[1] ) / dpi )
    #------------------------------------------------------------------------------------

    def getY() :

    def getX() :





class MainWindow(wx.Frame):
    def __init__(self, parent):
        self.app = wx.App()
        #wx.Frame.__init__(self, *args, **kwargs)
        wx.Frame.__init__(self, parent, title="Fix this later", size=(1000,600))
        self.panel = wx.Panel(self)
        #self.spin = wx.SpinCtrl(self.panel)
        #self.button = wx.Button(self.panel, label="Update")
        #self.stop   = wx.Button(self.panel, label="Stop")

        self.sizer = wx.BoxSizer()
        #self.sizer.Add(self.button)
        #self.sizer.Add(self.stop)
        self.graph = PlotPanel( self, position=(20, 50) )
        self.panel.SetSizerAndFit(self.sizer)
        self.Show()

        # Use EVT_CHAR_HOOK on Frame insted of wx.EVT_KEY_UP on SpinCtrl
        # to disable "on Enter go to next widget" functionality
        #self.Bind(wx.EVT_CHAR_HOOK, self.OnKey) 
        #self.button.Bind(wx.EVT_BUTTON, self.OnUpdate)
        #self.stop.Bind(wx.EVT_BUTTON, self.OnStop)

    def OnKey(self, e):
        if e.GetKeyCode() == wx.WXK_RETURN:   # Is the key ENTER?
            self.value = self.spin.GetValue() # Read SpinCtrl and set internal value
        else:                                 # Else let the event out of the handler
            e.Skip()


app = wx.App(False)
win = MainWindow(None)
app.MainLoop()