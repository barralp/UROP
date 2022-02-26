
from wx.core import EVT_CHECKBOX
sys.path.insert(0, '../../database')
import os
# i found the following version more portable
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.path[0])),'database')) # goes 2 level up
from communicate_database import getEntireColumn, getVariableList
import numpy
import numpy as np
import pandas as pd
import sys

class DataFrame():
    def addToDataFrame(self, dropDownX, dropDownY, graph) :
        dictionary = {'x': self.graph.changeVar(dropDownX.GetStringSelection()), 
            'y': self.graph.changeVar(dropDownY.GetStringSelection())}
        df = pd.DataFrame(dictionary)
        return df

    def getDataFrame(self) :
        return 

    def copyToClipboard(self, index) :
        df = self.createDataFrame(self.dropDownX, self.dropDownY)

    def copyToClipboardSecond(self, event):
        #event.GetEventObject() = self.ExportDataButtonX
        print(event.GetEventObject())
        dictionary = {'x': self.graph1.changeVar(self.dropDownX.GetStringSelection()), 
            'y': self.graph1.changeVar(self.dropDownY.GetStringSelection())}
        ds = pd.DataFrame(dictionary)
        if (self.dropDownY.GetStringSelection() != '' and self.dropDownX.GetStringSelection() != '') :  
            ds.to_clipboard()

    def getVariablesList(self) :
        return getVariableList()