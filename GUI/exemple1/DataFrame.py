
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


class DataFrame():
    def __init__(self) :
        self.dataFrame = [{}]

    def addToDataFrame(self, dropDownX, dropDownY) :
        #if ()
        self.dataFrame.update = {'x': self.graph.changeVar(dropDownX.GetStringSelection()), 
        'y': self.graph.changeVar(dropDownY.GetStringSelection())}
        df = pd.DataFrame(self.dataFrame)
        return df

    def getCoordinates(self, dropDownX, dropDownY) :
        varX = []
        varY = []
        length = len(self.dataFrame)
        for i in self.dataFrame :
            if (dropDownX != self.dataFrame[i{1}]) :
                if (i != self.dataFrame.length) :
                    i += 1
                else :
                    i = len(self.dataFrame)
                    self.dataFrame.__add__({'table' : 'ciceroOut', 'dropDown' : dropDownX, 
                        'values' : getEntireColumn(dropDownX, "ciceroOut")})
                    varX = self.dataFrame[i{2}]
            else :
                varX = self.dataFrame[0]
            
            if (dropDownY != self.dataFrame[i{1}]) :
                if (i != self.dataFrame.length) :
                    i += 1
                else :
                    i = len(self.dataFrame)
                    self.dataFrame.__add__({'table' : 'nCount', 'dropDown' : dropDownY, 
                        'values' : getEntireColumn(dropDownY, "nCounts")})
                    varY = self.dataFrame[i{2}]
            else :
                varY = self.dataFrame[0]
        return [varX, varY]

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