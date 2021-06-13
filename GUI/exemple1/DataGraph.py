import sys
import wx
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

def f(x) :
    return x
def g(y) :
    return y

class DataGraph(wx.Frame) :
    def __init__(self, parent):
        self.app = wx.App()
        super(DataGraph, self).__init__(parent, size=(450, 300))
        # m_x = x
        # m_y = y

    def makeGraph(self) :
        interact(f, x=['run ID', 'Iteration Num', 'Iteration Count', 'Running Counter',
            'TOF', 'Comp Level', 'Img Freq', 'dummy', 'Iodine Freq', 'Final B Field',
            'Camera Fudge Time', 'Load Time', 'Comp Time', 'Load Current', 'time stamp', 
            'wee', 'Mot Load Freq', 'Mot Comp Freq', 'time', 'ZSPower', 'image Time', 
            'MOT Level', 'comp x', 'comp y', 'Loss Time', 'TCFreq', 'compz', 'MOT Current Amps',
            'MOT Load Current Amps', 'Comp Time 2', 'Comp Level 2', 'MOT Comp Freq 2', 'Freq Comp Time 2',
            'Final Y Comp', 'Comp Hold Time', 'Wait Time', 'AS Power', 'AS Power mW', 'AS Power mW 2', 
            'level 1', 'level 2', 'level 3', 'level 4', 'level 5', 'freq 1', 'freq 2',
            'freq 3', 'freq 4', 'freq 5', 'ODT_Ramp', 'ODT Hold Time', 'ODT 1 Final', 'ODT 2 Final', 
            'Evap Time 2', 'Evap Time 1', 'Evap Time 3', 'Big Z', 'SGOn', 'SGOn2', 'Pump Time',
            'Doppler Cool Freq', 'ODT1_Init', 'ODT 1 Evap 1 End', 'ODT 2 Init', 'ODT 2 Evap 1 End',
            'Feshbach Current', 'Evap Time 4', 'AM Freq', 'AM Duration', 'ODT Ramp Up', 'Evap 2 Factor',
            'tau', 'total Exp', 'In Trap Cool Freq', 'In Trap Cool Time', 'Evap Time 5', 'Evap 1 End Gradient',
            'Var60', 'Evap Scan', 'Evap_Gradient_Init', 'Evap Gradient 1', 'Evap Gradient 2',
            'Evap Gradient 3', 'Evap End Gradient', 'ODT TOF Gradient', 'ODT TOF BigZ', 
            'Evap 5 Big Z', 'Final ODT 1', 'Blincking Time', 'Blincking freq', 'Molasses level',
            'Blincking duration', 'ODT Molasses', 'ODT Molasses Z Field', 'ODT Load MOT Freq',
            'ODT Comp x', 'ODT Comp y', 'ODT Comp z', 'Blincking length', 'ODT Load MOT Freq', 
            'Evap 1 Comp Z', 'Pumping Freq', 'comp x Earth', 'comp y Earth', 'comp z Earth',
            'Evap Time 6', 'comp z 2'])
        interact(g, y=['run ID', 'Iteration Num', 'Iteration Count', 'Running Counter', 
            'TOF', 'Comp Level', 'Img Freq', 'dummy', 'Iodine Freq', 'Final B Field',
            'Camera Fudge Time', 'Load Time', 'CompTime', 'Load Current', 'time stamp',
            'wee', 'Mot Load Freq', 'Mot Comp Freq', 'time', 'ZSPower', 'image Time', 
            'MOT Level', 'comp x', 'comp y', 'Loss Time', 'TCFreq', 'compz', 'MOT Current Amps',
            'MOT Load Current Amps', 'Comp Time 2', 'Comp Level 2', 'MOT Comp Freq 2', 'Freq Comp Time 2',
            'Final Y Comp', 'Comp Hold Time', 'Wait Time', 'AS Power', 'AS Power mW', 'AS Power mW 2',
            'MOTCurrent2', 'level 1', 'level 2', 'level 3', 'level 4', 'level 5', 'freq 1', 'freq 2',
            'freq 3', 'freq 4', 'freq 5', 'ODT Ramp', 'ODT Hold Time', 'ODT 1 Final', 'ODT 2 Final',
            'Evap Time 2', 'Evap Time 1', 'Evap Time 3', 'Big Z', 'SGOn', 'SGOn2', 'PumpTime', 
            'Doppler Cool Freq', 'ODT1_Init', 'ODT 1 Evap 1 End', 'ODT 2 Init', 'ODT 2 Evap 1 End',
            'Feshbach Current', 'Evap Time 4', 'AM Freq', 'AM Duration', 'ODT Ramp Up', 'Evap 2 Factor',
            'tau', 'total Exp', 'In Trap Cool Freq', 'In Trap Cool Time', 'Evap Time 5', 'Evap 1 End Gradient',
            'Var 60', 'Evap Scan', 'Evap Gradient Init', 'Evap_Gradient1', 'Evap Gradient 2',
            'Evap Gradient 3', 'Evap End Gradient', 'ODT TOF Gradient', 'ODT TOF Big Z', 
            'Evap 5 Big Z', 'Final ODT 1', 'BlinckingTime', 'Blincking freq', 'Molasses level',
            'Blincking duration', 'ODT Molasses', 'ODT Molasses Z Field', 'ODT Load MOT Freq',
            'ODT comp x', 'ODT comp y', 'ODT comp z', 'Blincking length', 'ODT Load MOT Freq', 
            'Evap 1 CompZ', 'Pumping freq', 'comp x Earth', 'comp y Earth', 'comp z Earth',
            'Evap Time 6', 'comp z 2'])

        x1 = [0, 1, 2, 3]
        y1 = [0, 3, 4, 1]
        x2 = [0, 1, 2, 3]
        y2 = [5, 2, 3, 3]

        ##varGraph = wxmplot.interactive.PlotPanel(self, (1750, 1600))
        ## here have a series of ifs that will check the current variables selected

        plt.plot(x1, y1, 'o', color='black')
        plt.xlabel("x variable")
        plt.ylabel("Y Variable")
        plt.title("X vs. Y Graph")
        ##plt.scatterplot(x2, y2, color = "red", edgecolor = "red")

        self.Show()

if __name__ == '__main__':
    graph = DataGraph(None)
    graph.makeGraph()
    graph.app.MainLoop()
