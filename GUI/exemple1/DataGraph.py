import sys
import wx
import wxmplot
import numpy
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

def f(x) :
    return x
class DataGraph(wx.Frame) :
    def __init__(self, parent):
        self.app = wx.App()
        super(DataGraph, self).__init__(parent, size=(450, 300))
        # m_x = x
        # m_y = y

    def makeGraph(self) :
        interact(f, x=['runID', 'IterationNum', 'IterationCount', 'RunningCounter',
            'TOF', 'CompLevel', 'ImgFreq', 'dummy', 'IodineFreq', 'finalBField',
            'CameraFudgeTime', 'LoadTime', 'CompTime', 'LoadCurrent', 'timestamp', 
            'wee', 'MotLoadFreq', 'MotCompFreq', 'time', 'ZSPower', 'imageTime', 
            'MOTLevel', 'compx', 'compy', 'LossTime', 'TCFreq', 'compz', 'MOTCurrent_Amps',
            'MOTLoadCurrent_Amps', 'CompTime2', 'CompLevel2', 'MOTCompFreq2', 'FreqCompTime2',
            'FinalYComp', 'CompHoldTime', 'WaitTime', 'ASPower', 'ASPower_mW', 'ASPower_mW_2', 
            'level1', 'level2', 'level3', 'level3', 'level4', 'level5', 'freq1', 'freq2',
            'freq3', 'freq4', 'freq5', 'ODT_Ramp', 'ODTHoldTime', 'ODT1_Final', 'ODT2_Final', 
            'EvapTime2', 'EvapTime1', 'EvapTime3', 'BigZ', 'SGOn', 'SGOn2', 'PumpTime',
            'DopplerCoolFreq', 'ODT1_Init', 'ODT1_Evap1_End', 'ODT2_Init', 'ODT2_Evap1_End',
            'FeshbachCurrent', 'EvapTime4', 'AMFreq', 'AMDuration', 'ODTRampUp', 'Evap2Factor',
            'tau', 'totalExp', 'InTrapCoolFreq', 'InTrapCoolTime', 'EvapTime5', 'Evap1_End_Gradient',
            'Var60', 'EvapScan', 'Evap_Gradient_Init', 'Evap_Gradient1', 'Evap_Gradient2',
            'Evap_Gradient3', 'Evap_End_Gradient', 'ODT_TOF_Gradient', 'ODT_TOF_BigZ', 
            'Evap5_BigZ', 'FinalODT1', 'BlinckingTime', 'Blincking_Freq', 'Molasses_level',
            'Blincking_duration', 'ODT_Molasses', 'ODT_Molasses_ZField', 'ODTLoad_MOT_Freq',
            'ODTCompx', 'ODTCompy', 'ODTCompz', 'Blinckinglength', 'ODTLoad_MOTFreq', 
            'Evap1_CompZ', 'Pumping_Freq', 'compx_Earth', 'compy_Earth', 'compz_Earth',
            'EvapTime6', 'compz2'])
        x1 = [0, 1, 2, 3]
        y1 = [0, 3, 4, 1]
        x2 = [0, 1, 2, 3]
        y2 = [5, 2, 3, 3]

        varGraph = wxmplot.PlotPanel(self, (1750, 1600))
        ## here have a series of ifs that will check the current variables selected
        varGraph.scatterplot(x1, y1, title = 'x vs y graph', xLabel = 'x', yLabel = 'y')
        varGraph.scatterplot(x2, y2, color = "red", edgecolor = "red")


        self.Show()

if __name__ == '__main__':
    graph = DataGraph(None)
    graph.makeGraph()
    graph.app.MainLoop()
