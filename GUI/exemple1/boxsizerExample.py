from re import X
from sqlalchemy import column
from wx.core import EVT_CHECKBOX

sys.path.insert(0, '../../database')
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.path[0])),'database')) # goes 2 level up
from communicate_database import getVariableList, getLastImageID, getLastXPoints

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import wx
import wx.lib.scrolledpanel
import numpy as np
import pandas as pd
from datetime import date
from PIL import Image
import wx.grid as grid
import time
import threading
from PIL import Image

matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class DypoleDatabaseViewer(wx.Frame):
    def __init__(self, parent, title):
        self.app = wx.App()
        wx.Frame.__init__(self, parent, title = title, size = (1000, 500))
        self.start()
        
    def saveGraphImage(self, event) :
        self.graph1.saveDataImage(0)
        self.graph2.saveDataImage(0)
        self.graph3.saveDataImage(0)

    def start(self):
        self.InitUI()
        self.Centre()
        self.Show()

    def checkForNewData(self) :
        #self.graph1.emptyDataBase()
        #self.graph2.emptyDataBase()
        #self.graph3.emptyDataBase()
        while self.checkingData :
            self.graph1.checkForNewData()
            self.graph2.checkForNewData()
            self.graph3.checkForNewData()
            print('checked')
            time.sleep(3)

    def updatePointCount(self, event) :
        if self.numberOfPointsTextBox.GetValue().isdigit() and int(self.numberOfPointsTextBox.GetValue()) > 0 :
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

        self.selectionsGrid = grid.Grid(self.basePanel)
        self.selectionsGrid.CreateGrid(9, 7)
        
        self.graphDropDown = wx.ComboBox(self.basePanel, choices=['Graph 1', 'Graph 2', 'Graph 3'])
        #self.dropDownYSelections = wx.ComboBox(self.basePanel, choices=varsY)
        #self.dropDownXSelections = wx.ComboBox(self.basePanel, choices=varsX)
        #self.dropDownZSelections = wx.ComboBox(self.basePanel, choices=[])
        #self.lowZValue = wx.TextCtrl()
        #self.highZValue = wx.TextCtrl()

        self.selectionsGrid.SetColLabelValue(col=0, value='Graph')
        self.selectionsGrid.SetColLabelValue(col=1, value='X')
        self.selectionsGrid.SetColLabelValue(col=2, value='Y')
        self.selectionsGrid.SetColLabelValue(col=3, value='Z')
        self.selectionsGrid.SetColLabelValue(col=4, value='Z Min')
        self.selectionsGrid.SetColLabelValue(col=5, value='Z Max')
        self.selectionsGrid.SetColLabelValue(col=6, value='Parameters')

        #self.selectionsGrid.SetRowLabelValue(row=0, value=self.graphDropDown)

        self.parameterCollection = []

        #self.gridCol = {
         #   'Graph' : self.graphDropDown,
          #  'X' : self.dropDownXSelections,
           # 'Y' : self.dropDownYSelections,
            #'Z' : self.dropDownZSelections,
            #'Z Min' : self.lowZValue,
            #'Z Max' : self.highZValue,
            #'Parameters' : ''
        #}
        # this should go under the graph label 
        # each one of the dictionary should go in a different row 
        
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
        self.TitleBox = wx.StaticBox(self.basePanel, label='Title Box')

        varsX = getVariableList('ciceroOut')
        varsY = getVariableList('nCounts')

        self.updateDataButton = wx.Button(self.basePanel, wx.ID_ANY, 'Check for new data')
        self.updateDataButton.SetBackgroundColour((255, 230, 180, 255))
        self.numberOfPointsTextBox = wx.TextCtrl(self.basePanel)
        self.textForPointCount = wx.StaticText(self.basePanel, label = '# of points to take from database')
        self.updateDataButtonStatus = False

        self.numberOfPointsTextBox.Bind(wx.EVT_TEXT, self.updatePointCount)

        self.saveImageButton = wx.Button(self.basePanel, wx.ID_ANY, 'Save All Graph Images')
        self.saveImageButton.Bind(wx.EVT_BUTTON, self.saveGraphImage)

        self.BoxSizer22.Add(self.updateDataButton, flag=wx.ALL|wx.EXPAND, border=5)
        self.BoxSizer22.Add(self.textForPointCount, flag=wx.ALL|wx.EXPAND, border=5)
        self.BoxSizer22.Add(self.numberOfPointsTextBox, flag=wx.ALL|wx.EXPAND, border=5)
        self.BoxSizer22.Add(self.saveImageButton, flag=wx.ALL|wx.EXPAND, border=5)
        self.BoxSizer22.Add(self.selectionsGrid)

        self.updateDataButton.Bind(wx.EVT_BUTTON, self.checkNewData)

        self.secondRowBoxSizer.Add(self.BoxSizer21)
        self.secondRowBoxSizer.Add(self.BoxSizer22)

        self.mainWindowBoxSizer.Add(self.firstRowBoxSizer)
        self.mainWindowBoxSizer.Add(self.secondRowBoxSizer)
        
        self.basePanel.SetSizer(self.mainWindowBoxSizer)
        self.checkingData = False

    def checkNewData(self, event) : # rename variables to make them more clear
        try :
            if not self.updateDataButtonStatus : # case where new data is being taken
                self.updateDataButtonStatus = True
                self.updateDataButton.SetBackgroundColour((70, 100, 200, 255)) # button is blue when new data is being checked for 
                self.checkForDataThread.start()
                self.checkingData = True
            else : # case where existing data is used
                self.updateDataButtonStatus = False
                self.updateDataButton.SetBackgroundColour((230, 230, 200, 255)) # button is red when taking old data
                self.checkingData = False
                time.sleep(3)
                self.checkForDataThread.join()
                del(self.checkForDataThread)
                time.sleep(1)
        except AttributeError :
            self.checkForDataThread = threading.Thread(target=self.checkForNewData)
            self.updateDataButtonStatus = False
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

    def dropDownsFilled(self) :
        return self.getDropDownSelection()[0] != '' and self.getDropDownSelection()[1] != ''
    
    def setUpFigure(self):
        self.figure = matplotlib.figure.Figure(facecolor='white', figsize=(6,4))
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color='gray')
        self.axes.set_xbound( (0,2) )
        self.axes.set_ybound( (0,10) )
        self.axes.set_xlabel( 'X Var' ) ## change later
        self.axes.set_ylabel( 'Y Var' )
        self.axes.grid(True, color='gray')

    # change update dropdown to use the info from the grid and check to see if there is multiple x and y selected
    def updateDropDown(self, event) :
        self.axes.cla()
        dropDownX = self.getDropDownSelection()[0]
        dropDownY1 = self.getDropDownSelection()[1] 
        self.axes.set_title(dropDownX + ' vs. ' + dropDownY1) 
        self.axes.set_xlabel(dropDownX)
        self.axes.set_ylabel(dropDownY1)
        if (self.dropDownsFilled()) :
            self.changeVar()
            self.axes.plot(self.dataFrame['x'], self.dataFrame['y'], marker ='o', ls='')
            #self.axes.plot(self.dataFrame['x'], self.dataFrame['y'], ls='') call this to make multiple graphs
        else :
            self.axes.plot([],[])
        self.canvas.draw()

    def graphData(self, graph) :
        #if (x and y are both selected) :
            #updateDropDown()  
        #if (graph)
        return 0

    def handleGridInput(self) :
        #if selectedGraph == graph1 :
                #graphData(graph)
        #elif selectedGraph == graph2 :
            #graphData(graph)
        #elif selectedGraph == graph3 :
            #graphData(graph)
        return 0

    def setUpMenu(self):
        self.xBox = wx.StaticBox(self, label='X Parameters')
        self.xBoxSizer = wx.StaticBoxSizer(self.xBox, wx.VERTICAL)
        self.yBox = wx.StaticBox(self, label='Y Parameters')
        self.yBoxSizer = wx.StaticBoxSizer(self.yBox, wx.VERTICAL)
        self.controlsBox = wx.StaticBox(self, label='Controls Box')
        self.controlsBoxSizer = wx.StaticBoxSizer(self.controlsBox, wx.VERTICAL)

        #self.gridBox = wx.StaticBox(self, label='Grid Box')
        #self.gridBoxSizer = wx.StaticBoxSizer(self.gridBox, wx.VERTICAL)

        self.numberOfPoints = 50
        
        self.textX1 = wx.StaticText(self, label = 'X Variable 1')
        self.textY1 = wx.StaticText(self, label = 'Y Variable 1')
    
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
        self.saveGraphImage = wx.Button(self, wx.ID_ANY, 'Save Graph Image')

        self.copyGraphData.Bind(wx.EVT_BUTTON, self.copyData)
        self.saveGraphImage.Bind(wx.EVT_BUTTON, self.saveDataImage)
        
        self.xBoxSizer.Add(self.textX1)
        self.xBoxSizer.Add(self.dropDownX1)

        self.xBoxSizer.Add(self.textXRelations)
        self.xBoxSizer.Add(self.dropDownXRelations1)
        self.yBoxSizer.Add(self.textY1)
        self.yBoxSizer.Add(self.dropDownY1)
        self.yBoxSizer.Add(self.textYRelations)
        self.yBoxSizer.Add(self.dropDownYRelations1)

        self.controlsBoxSizer.Add(self.copyGraphData)
        self.controlsBoxSizer.Add(self.saveGraphImage)

        self.menuBoxSizer.Add(self.xBoxSizer)
        self.menuBoxSizer.Add(self.yBoxSizer)
        self.menuBoxSizer.Add(self.controlsBoxSizer)

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

    def makeSecondPlot(self) :
        if (self.secondPlotCheckbox.GetValue() != '' and self.dropDownsFilled()) :
            make = 0 

        return 0

    # This will be the function that is used to check to see if there is new data in the database and adds it
    def checkForNewData(self) :
        if self.dropDownsFilled() and len(self.dataFrame) != 0 :
            #print(self.dataFrame)
            lastRunID_fk = self.dataFrame['runID_fk'].iloc[-1]
            lastRunID_fk_dataBase = getLastXPoints('runID_fk', 'nCounts', 1, 'runID_fk')[0]
            if lastRunID_fk != lastRunID_fk_dataBase :
                varX = getLastXPoints(self.getDropDownSelection()[0], 'ciceroOut', 1, 'runID')
                varY = getLastXPoints(self.getDropDownSelection()[1], 'nCounts', 1, 'runID_fk')
                lastRunID_fk = getLastXPoints('runID_fk', 'nCounts', 1, 'runID_fk')
                self.dataFrame.append({'x' : varX, 'y' : varY, 'runID_fk' : lastRunID_fk}, ignore_index=True)
        elif self.dropDownsFilled() and len(self.dataFrame) == 0 :
            varX = getLastXPoints(self.getDropDownSelection()[0], 'ciceroOut', 1, 'runID')
            varY = getLastXPoints(self.getDropDownSelection()[1], 'nCounts', 1, 'runID_fk')
            lastRunID_fk = getLastXPoints('runID_fk', 'nCounts', 1, 'runID_fk')

    def saveDataImage(self, event) : #eps
        width = 200 
        height = 200
        bmp = wx.Bitmap(width, height)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        today = date.today()
        dateOfGraph = today.strftime("%Y-%b-%d")
        if self.dropDownsFilled() :
            imageName = dateOfGraph + " " + self.dropDownX1.GetStringSelection() + " vs. " + self.dropDownY1.GetStringSelection()
            bmp.SaveFile(imageName, wx.BITMAP_TYPE_PNG)

    # This function will eventually use the number of data points to only get the last couple entries 
    def changeVar(self) :
        if (self.dropDownsFilled()) :
            self.dataFrame.drop(columns=['x', 'y'], inplace=True)
            data = {
                'x' : getLastXPoints(self.getDropDownSelection()[0], 'ciceroOut', self.numberOfPoints, 'runID'),
                'y' : getLastXPoints(self.getDropDownSelection()[1], 'nCounts', self.numberOfPoints, 'runID_fk'),
                'y1' : getLastXPoints(self.getDropDownSelection()[1], 'nCounts', self.numberOfPoints, 'runID_fk'),
                'runID_fk' : getLastXPoints('runID_fk', 'nCounts', self.numberOfPoints, 'runID_fk')
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

