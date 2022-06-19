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

    #def modifyDataframe(self, xVar, yVar) :

    def updateData(self) :
        self.graph1.updateData()
        self.graph2.updateData()
        self.graph3.updateData()

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

        self.updateButton = wx.Button(self.basePanel, wx.ID_ANY, 'Check for new data')
        self.textBox = wx.TextCtrl(self.basePanel)
        self.buttonStatus = 0

        self.BoxSizer22.Add(self.updateButton, flag=wx.ALL|wx.EXPAND, border=5)
        self.BoxSizer22.Add(self.textBox, flag=wx.ALL|wx.EXPAND, border=5)

        self.updateButton.Bind(wx.EVT_BUTTON, self.checkNewData)

        self.secondRowBoxSizer.Add(self.BoxSizer21)
        self.secondRowBoxSizer.Add(self.BoxSizer22)
        
        self.mainWindowBoxSizer.Add(self.firstRowBoxSizer)
        self.mainWindowBoxSizer.Add(self.secondRowBoxSizer)
        
        self.basePanel.SetSizer(self.mainWindowBoxSizer)
    
    def helloFunction(self) :
        while(self.buttonStatus == 1) :
            time.sleep(2)
            print('hello')

    def checkNewData(self, event) : # rename variables to make them more clear
        try :
            if (self.buttonStatus == 0) : # case where new data is being taken
                self.buttonStatus = 1
                self.t1.start()
                print(self.buttonStatus)
            elif (self.buttonStatus == 1) : # case where existing data is used
                print('trying to join')
                self.buttonStatus = 0
                self.t1.join()
                time.sleep(3)
                print('done')
        except AttributeError :
            self.t1 = threading.Thread(target=self.helloFunction)
            self.buttonStatus = 0 
            self.checkNewData(0)
        time.sleep(2)

class PlotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.initPlotPanel()
        data = {
            'x' : [],
            'y' : []
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
        dropDownX = self.dropDownX1.GetStringSelection()
        dropDownY = self.dropDownY1.GetStringSelection()
        self.axes.set_title(dropDownX + ' vs. ' + dropDownY) 
        self.axes.set_xlabel(dropDownX)
        self.axes.set_ylabel(dropDownY)
        if (dropDownY != '' and dropDownX != '') :
            self.changeVar()
            self.axes.plot(self.dataFrame['x'], self.dataFrame['y'], marker ='o', ls='')
            #self.axes.plot([],[])
        else :
            self.axes.plot([],[])
        self.canvas.draw()

    def setUpMenu(self):
        self.xBox = wx.StaticBox(self, label='X parameters')
        self.xBoxSizer = wx.StaticBoxSizer(self.xBox, wx.VERTICAL)
        self.yBox = wx.StaticBox(self, label='Y parameters')
        self.yBoxSizer = wx.StaticBoxSizer(self.yBox, wx.VERTICAL)
        
        self.textX1 = wx.StaticText(self, label = 'X Variable')
        self.textY1 = wx.StaticText(self, label = 'Y Variable')
    
        varsX = getVariableList('ciceroOut')
        varsY = getVariableList('ciceroOut')
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
        
        self.xBoxSizer.Add(self.textX1)
        self.xBoxSizer.Add(self.dropDownX1)
        self.xBoxSizer.Add(self.textXRelations)
        self.xBoxSizer.Add(self.dropDownXRelations1)
        self.yBoxSizer.Add(self.textY1)
        self.yBoxSizer.Add(self.dropDownY1)
        self.yBoxSizer.Add(self.textYRelations)
        self.yBoxSizer.Add(self.dropDownYRelations1)
        
        self.menuBoxSizer.Add(self.xBoxSizer)
        self.menuBoxSizer.Add(self.yBoxSizer)
        self.updateDropDown(0)

    def updateData(self) :
        self.changeVar()

    def checkForNewData(self) :
        while True:
            time.sleep(2)
            # change this so that the image id can be used to pull the next point
            lenX = len(getEntireColumn(self.dropDownX1.GetStringSelection(), 'ciceroOut'))
            lenY = len(getEntireColumn(self.dropDownY1.GetStringSelection(), 'ciceroOut'))

            lastImageID = 0

            if lastImageID != getLastImageID() :
                self.dataFrame['Y'].append(getEntireColumn(self.dropDownY1.GetStringSelection(), 'ciceroOut')[lenX - 1])
                self.dataFrame['X'].append(getEntireColumn(self.dropDownX1.GetStringSelection(), 'ciceroOut')[lenY - 1])

    
    def changeVar(self) :
        if (self.dropDownX1.GetStringSelection() != '' and self.dropDownY1.GetStringSelection() != '') :
            self.dataFrame.drop(columns=['x', 'y'], inplace=True)
            data = {
                'x' : getEntireColumn(self.dropDownX1.GetStringSelection(), 'ciceroOut'),
                'y' : getEntireColumn(self.dropDownY1.GetStringSelection(), 'ciceroOut')
                #'imageIDs' : getEntireColumn()
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