
from wx.core import EVT_CHECKBOX
import sys
sys.path.insert(0, '../../database')
import os
# i found the following version more portable
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.path[0])),'database')) # goes 2 level up
from communicate_database import getEntireColumn, getVariableList
import numpy
import numpy as np
import pandas as pd


class DataFrame(pd.DataFrame):
    def __init__(self) :
        xData = {
            "variable:" : "X",
            "data" : []
        }
        yData = {
            "variable: " : "Y",
            "data" : []
        }
        #self.dataFrame.add
        
    def addToDataFrame(self, dropDownX, dropDownY) :
        self.dataFrame.update = {'x': self.graph.changeVar(dropDownX.GetStringSelection()), 
        'y': self.graph.changeVar(dropDownY.GetStringSelection())}
        df = pd.DataFrame(self.dataFrame)
        return df

    def appendDataFrame(self, dropDownX, dropDownY) :
        if (dropDownX != self.dataFrame) :
            self.dataFrame.append()
            self.dataFrame.__add__({'table' : 'ciceroOut', 'dropDown' : dropDownX, 
                'values' : getEntireColumn(dropDownX, "ciceroOut")})

        if (dropDownY != self.dataFrame) :
            self.dataFrame.append
            self.dataFrame.__add__({'table' : 'nCount', 'dropDown' : dropDownY, 
                'values' : getEntireColumn(dropDownY, "nCount")})

    def getDataFrame(self) :
        return self.dataFrame

    #def copyToClipboard(self, index) :
        #df = self.createDataFrame(self.dropDownX, self.dropDownY)

    def copyToClipboardSecond(self, event):
        #event.GetEventObject() = self.ExportDataButtonX
        print(event.GetEventObject())
        ds = pd.DataFrame(self.dataFrame)
        if (self.dropDownY.GetStringSelection() != '' and self.dropDownX.GetStringSelection() != '') :  
            ds.to_clipboard()

    def getVariableList(self, table) :
        var1 = []
        var2 = []
        for i in self.dataFrame :
            if self.dataFrame[i-1] == "ciceroOut" :
                var1.__add__(self.dataFrame[i-1][0])
            elif self.dataFrame[i-1] == "nCount" :
                var2.__add__(self.dataFrame[i-1][0])
        if table == "ciceroOut" :
            return var1
        else :
            return var2