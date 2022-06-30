from re import X
from sqlalchemy import column
from wx.core import EVT_CHECKBOX

sys.path.insert(0, '../../database')
import os
import sys
# i found the following version more portable
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.path[0])),'database')) # goes 2 level up
from communicate_database import getEntireColumn
from communicate_database import getVariableList, getLastImageID, getLastXPoints
import matplotlib
import wx
import wx.lib.scrolledpanel
import numpy as np
import pandas as pd
import threading
import time

matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class DypoleDatabaseViewer(wx.Frame):
    def __init__(self, parent, title):
        self.app = wx.App()
        wx.Frame.__init__(self, parent, title = title, size = (1000, 500))
        self.start()
        
    def start(self):
        self.InitUI()
        self.Centre()
        self.Show()

    def checkForNewData(self) :
        self.graph1.axes.cla()
        self.graph2.axes.cla()
        self.graph3.axes.cla()
        while (True) :
            time.sleep(2)
            self.graph1.checkForNewData()
            self.graph2.checkForNewData()
            self.graph3.checkForNewData()

    def updatePointCount(self, event) :
        if int(self.numberOfPointsTextBox.GetValue()) > 0 :
            self.graph1.updateNumberOfPoints(self.numberOfPointsTextBox.GetValue())
            self.graph2.updateNumberOfPoints(self.numberOfPointsTextBox.GetValue())
            self.graph3.updateNumberOfPoints(self.numberOfPointsTextBox.GetValue())

    def InitUI(self):
        self.basePanel = wx.lib.scrolledpanel.ScrolledPanel(self, id = -1, size = (1,1))
        self.basePanel.SetupScrolling()
        self.mainWindowBoxSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.firstRowBox = wx.StaticBox(self.basePanel, label='Upper box')
        self.firstRowBoxSizer = wx.StaticBoxSizer(self.firstRowBox, wx.HORIZONTAL)
        
        self.Box11 = wx.StaticBox(self.basePanel, label='Graph 1')
        self.BoxSizer11 = wx.StaticBoxSizer(self.Box11, wx.HORIZONTAL)
        self.Box12 = wx.StaticBox(self.basePanel, label='Graph 2')
        self.BoxSizer12 = wx.StaticBoxSizer(self.Box12, wx.HORIZONTAL)
        
        self.graph1 = PlotPanel(self.basePanel)
        self.BoxSizer11.Add(self.graph1)
        self.graph2 = PlotPanel(self.basePanel)
        self.BoxSizer12.Add(self.graph2)
        
        self.firstRowBoxSizer.Add(self.BoxSizer11)
        self.firstRowBoxSizer.Add(self.BoxSizer12)
        
        self.secondRowBox = wx.StaticBox(self.basePanel, label='Lower box')
        self.secondRowBoxSizer = wx.StaticBoxSizer(self.secondRowBox, wx.HORIZONTAL)
        
        self.Box21 = wx.StaticBox(self.basePanel, label='Graph 3')
        self.BoxSizer21 = wx.StaticBoxSizer(self.Box21, wx.HORIZONTAL)

        self.graph3 = PlotPanel(self.basePanel)
        self.BoxSizer21.Add(self.graph3, flag=wx.ALL|wx.EXPAND, border = 5)

        self.Box22 = wx.StaticBox(self.basePanel, label='Control box')
        self.BoxSizer22 = wx.StaticBoxSizer(self.Box22, wx.HORIZONTAL)

        self.updateDataButton = wx.Button(self.basePanel, wx.ID_ANY, 'Check for new data')
        self.updateDataButton.SetBackgroundColour((255, 230, 180, 255))
        self.numberOfPointsTextBox = wx.TextCtrl(self.basePanel)
        self.textForPointCount = wx.StaticText(self.basePanel, label = '# of points to take from database')
        self.updateDataButtonStatus = 0

        self.numberOfPointsTextBox.Bind(wx.EVT_TEXT, self.updatePointCount)

        self.BoxSizer22.Add(self.updateDataButton, flag=wx.ALL|wx.EXPAND, border=5)
        self.BoxSizer22.Add(self.textForPointCount, flag=wx.ALL|wx.EXPAND, border=5)
        self.BoxSizer22.Add(self.numberOfPointsTextBox, flag=wx.ALL|wx.EXPAND, border=5)

        self.updateDataButton.Bind(wx.EVT_BUTTON, self.checkNewData)

        self.secondRowBoxSizer.Add(self.BoxSizer21)
        self.secondRowBoxSizer.Add(self.BoxSizer22)
        
        self.mainWindowBoxSizer.Add(self.firstRowBoxSizer)
        self.mainWindowBoxSizer.Add(self.secondRowBoxSizer)
        
        self.basePanel.SetSizer(self.mainWindowBoxSizer)

    def checkNewData(self, event) : # rename variables to make them more clear
        try :
            if (self.updateDataButtonStatus == 0) : # case where new data is being taken
                print(self.numberOfPointsTextBox.GetValue())
                self.updateDataButtonStatus = 1
                self.updateDataButton.SetBackgroundColour((70, 100, 200, 255)) # button is blue when new data is being checked for 
                self.checkForDataThread.start()
                print(self.updateDataButtonStatus)
            elif (self.updateDataButtonStatus == 1) : # case where existing data is used
                self.updateDataButtonStatus = 0
                self.updateDataButton.SetBackgroundColour((230, 230, 200, 255)) # button is red when taking old data
                self.checkForDataThread.join()
                time.sleep(3)
        except AttributeError :
            self.checkForDataThread = threading.Thread(target=self.checkForNewData)
            self.updateDataButtonStatus = 0 
            self.checkNewData(0)
        time.sleep(2)

class PlotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.initPlotPanel()
        data = {
            'x' : [],
            'y' : [],
            'runID_fk' : []
        }
        self.dataFrame = pd.DataFrame(data)
    
    def initPlotPanel(self):
        self.mainBoxSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.setUpFigure()

        self.menuBox = wx.StaticBox(self, label='Menu')
        self.menuBoxSizer = wx.StaticBoxSizer(self.menuBox, wx.HORIZONTAL)
        
        self.setUpMenu()
        
        self.mainBoxSizer.Add(self.canvas, flag=wx.ALL, border=5)
        self.mainBoxSizer.Add(self.menuBoxSizer)
    
        self.SetSizer(self.mainBoxSizer)

    def getDataFrame(self) :
        return self.dataFrame
    
    def setUpFigure(self):
        self.figure = matplotlib.figure.Figure(facecolor='white', figsize=(6    ,4))
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color='gray')
        self.axes.set_xbound( (0,2) )
        self.axes.set_ybound( (0,10) )
        self.axes.set_xlabel( 'X Var' ) ## change later
        self.axes.set_ylabel( 'Y Var' )
        self.axes.grid(True, color='gray')
    
    def updateDropDown(self, event) :
        self.axes.cla()
        dropDownX = self.getDropDownSelection()[0]
        dropDownY = self.getDropDownSelection()[1]
        self.axes.set_title(dropDownX + ' vs. ' + dropDownY) 
        self.axes.set_xlabel(dropDownX)
        self.axes.set_ylabel(dropDownY)
        if (dropDownX != '' and dropDownY != '') :
            self.changeVar()
            self.axes.plot(self.dataFrame['x'], self.dataFrame['y'], marker ='o', ls='')
        else :
            self.axes.plot([],[])
        self.canvas.draw()

    def setUpMenu(self):
        self.xBox = wx.StaticBox(self, label='X parameters')
        self.xBoxSizer = wx.StaticBoxSizer(self.xBox, wx.VERTICAL)
        self.yBox = wx.StaticBox(self, label='Y parameters')
        self.yBoxSizer = wx.StaticBoxSizer(self.yBox, wx.VERTICAL)

        self.numberOfPoints = 50
        
        self.textX1 = wx.StaticText(self, label = 'X Variable')
        self.textY1 = wx.StaticText(self, label = 'Y Variable')
    
        varsX = getVariableList('ciceroOut')
        varsY = getVariableList('nCounts')
        relationsX = ['x', 'ln(x)', 'x^2', 'sqrt(x)']
        relationsY = ['y', 'ln(y)', 'y^2', 'sqrt(y)']
        
        self.dropDownX1 = wx.ComboBox(self, choices = varsX)
        self.dropDownY1 = wx.ComboBox(self, choices = varsY)

        self.dropDownX1.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        self.dropDownY1.Bind(wx.EVT_COMBOBOX, self.updateDropDown)

        self.textXRelations = wx.StaticText(self, label = 'X Transformation')
        self.textYRelations = wx.StaticText(self, label = 'Y Transformation')

        self.dropDownXRelations1 = wx.ComboBox(self, choices = relationsX)
        self.dropDownYRelations1 = wx.ComboBox(self, choices = relationsY)
        
        self.dropDownXRelations1.Bind(wx.EVT_COMBOBOX, self.updateDropDown)
        self.dropDownYRelations1.Bind(wx.EVT_COMBOBOX, self.updateDropDown)

        self.copyGraphData = wx.Button(self, wx.ID_ANY, 'Copy Graph Data')

        self.copyGraphData.Bind(wx.EVT_BUTTON, self.copyData)
        
        self.xBoxSizer.Add(self.textX1)
        self.xBoxSizer.Add(self.dropDownX1)
        self.xBoxSizer.Add(self.textXRelations)
        self.xBoxSizer.Add(self.dropDownXRelations1)
        self.yBoxSizer.Add(self.textY1)
        self.yBoxSizer.Add(self.dropDownY1)
        self.yBoxSizer.Add(self.textYRelations)
        self.yBoxSizer.Add(self.dropDownYRelations1)
        self.xBoxSizer.Add(self.copyGraphData)
        
        self.menuBoxSizer.Add(self.xBoxSizer)
        self.menuBoxSizer.Add(self.yBoxSizer)
        self.updateDropDown(0)

    def copyData(self, event) :
        self.dataFrame.to_clipboard()

    # updates the number of points to be displayed
    def updateNumberOfPoints(self, pointCount) :
        self.numberOfPoints = pointCount
        self.updateDropDown(0)

    def getDropDownSelection(self) :
        dropDownX1 = self.dropDownX1.GetStringSelection()
        dropDownY1 = self.dropDownY1.GetStringSelection()
        return [dropDownX1, dropDownY1]

    # This will be the function that is used to check to see if there is new data in the database and adds it
    def checkForNewData(self) :
        if self.getDropDownSelection()[0] != '' and self.getDropDownSelection()[1] != '' :
            print(self.dataFrame)
            lastRunID_fk = self.dataFrame['runID_fk'].iloc[-1]
            lastRunID_fk_dataBase = getLastXPoints('runID_fk', 'nCounts', 1, "runID_fk")[0]
            if lastRunID_fk != lastRunID_fk_dataBase :
                #print(lastRunID_fk)
                #print(lastRunID_fk_dataBase)
                varX = getLastXPoints(self.getDropDownSelection()[0], 'ciceroOut', 1, 'runID')
                varY = getLastXPoints(self.getDropDownSelection()[1], 'nCounts', 1, 'runID_fk')
                lastRunID_fk = getLastXPoints('runID_fk', 'nCounts', 1, 'runID_fk')
                self.dataFrame.append({'x' : varX, 'y' : varY, 'runID_fk' : lastRunID_fk}, ignore_index=True)
                print(self.dataFrame)

    # This function will eventually use the number of data points to only get the last couple entries 
    def changeVar(self) :
        if (self.getDropDownSelection()[0] != '' and self.getDropDownSelection()[1] != '') :
            self.dataFrame.drop(columns=['x', 'y'], inplace=True)
            data = {
                'x' : getLastXPoints(self.getDropDownSelection()[0], 'ciceroOut', self.numberOfPoints, "runID"),
                'y' : getLastXPoints(self.getDropDownSelection()[1], 'nCounts', self.numberOfPoints, "runID_fk"),
                'runID_fk' :getLastXPoints('runID_fk', 'nCounts', self.numberOfPoints, "runID_fk")
            }
            if (self.dropDownXRelations1.GetStringSelection() != '') :
                if (self.dropDownXRelations1.GetStringSelection() == 'ln(x)') :
                    data['x'] = np.log(data['x'])
                elif (self.dropDownXRelations1.GetStringSelection() == 'x^2') :
                    data['x'] = np.power(data['x'], 2)
                elif (self.dropDownXRelations1.GetStringSelection() == 'sqrt(x)') :
                    data['x'] = np.power(data['x'], 0.5)
                else : 
                    data['x'] = data['x']
            
            if(self.dropDownYRelations1.GetStringSelection() != '') :
                if (self.dropDownYRelations1.GetStringSelection() == 'ln(y)') :
                    data['y'] = np.log(data['y'])
                elif (self.dropDownYRelations1.GetStringSelection() == 'y^2') :
                    data['y'] = np.power(data['y'], 2)
                elif (self.dropDownYRelations1.GetStringSelection() == 'sqrt(y)') :
                    data['y'] = np.power(data['y'], 0.5)
                else :
                    data['y'] = data['y']

            self.dataFrame = pd.DataFrame(data)
            
if __name__ == '__main__':
    ui = DypoleDatabaseViewer(None, title='Database viewer')
    ui.app.MainLoop()