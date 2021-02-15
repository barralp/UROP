#!/usr/bin/python
# -*- coding: utf-8 -*-
# inspired by the snippet code provided on https://wiki.wxpython.org/ModelViewPresenter

#####WX IMPORTS#####
#wx- GUI toolkit for the Python programming language. wxPython can be used  to create graphical user interfaces (GUI).
import wx
#wx.lib.scrolledpanel- fills a “hole” in the implementation of ScrolledWindow.
#providing automatic scrollbar and scrolling behavior and the tab traversal management that ScrolledWindow lacks.

import wx.grid


class MyDatabaseBoxSizer(wx.StaticBoxSizer):
    def __init__(self, parentPanel, label = "Database"):
        databaseBox = wx.StaticBox(parentPanel, label = label)
        super(MyDatabaseBoxSizer, self).__init__(databaseBox, wx.VERTICAL)
        self.panel = parentPanel
        self.init_databaseBox_databaseBox()
        
    def init_databaseBox_databaseBox(self):
        ## Current file info
        fileInfoText = wx.StaticBox(self.panel,label='Currently displayed file informations')
        fileInfoBoxSizer = wx.StaticBoxSizer(fileInfoText, wx.VERTICAL)
        
        self.infoDBGrid = wx.grid.Grid(self.panel, -1, size=(300,150))
        self.infoDBGrid.CreateGrid(5,2)
        self.infoDBGrid.SetColLabelValue(0, 'Variable')
        self.infoDBGrid.SetColLabelValue(1, 'DB Value')
        for i in range(5):
            self.infoDBGrid.SetReadOnly(i,0,True)
            self.infoDBGrid.SetReadOnly(i,1,True)
        self.infoDBGrid.SetCellValue(0,0,"imageID")
        self.infoDBGrid.SetCellValue(1,0,"runID")
        self.infoDBGrid.SetCellValue(2,0,"sequenceID")
        self.infoDBGrid.SetCellValue(3,0,"Timestamp")
        self.infoDBGrid.SetCellValue(4,0,"nCount")
        self.infoDBGrid.SetRowLabelSize(0)
        fileInfoBoxSizer.Add(self.infoDBGrid, wx.ALIGN_CENTER | wx.ALL,0 )
        
        self.updateAnalysisButton = wx.Button(self.panel, label = 'Update analysis')
        fileInfoBoxSizer.Add(self.updateAnalysisButton, flag=wx.ALL, border=5)
        self.Add(fileInfoBoxSizer, flag=wx.ALL| wx.EXPAND, border=0)

        listText = wx.StaticText(self.panel, label='Image List')
        self.imageListBox = wx.ListBox(self.panel, size = (265, 100))
        self.Add(listText, flag=wx.ALL, border=5)
        self.Add(self.imageListBox, 1, wx.ALL, border=5)
        # self.updateImageListBox()  This cannot be coming from self anymore
    
    def setDatabaseImageID(self, imageID):
        self.infoDBGrid.SetCellValue(0,1,imageID)
    
    def setDatabaseRunID(self, runID):
        self.infoDBGrid.SetCellValue(1,1,runID)

    def setDatabaseSequenceID(self, sequenceID):
        self.infoDBGrid.SetCellValue(2,1,sequenceID)
        
    def setDatabaseTimestamp(self, timestamp):
        self.infoDBGrid.SetCellValue(3,1,timestamp)
        
    def setDatabaseNCount(self, NCount):
        self.infoDBGrid.SetCellValue(4,1,NCount)
    
    def setImageList(self, imageIDList):
        self.imageListBox.Clear()
        for imageID in self.imageIDList:    # Need to reverse?
                 self.imageListBox.Append(str(imageID))
