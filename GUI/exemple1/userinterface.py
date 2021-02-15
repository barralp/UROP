#!/usr/bin/python
# -*- coding: utf-8 -*-
# inspired by the snippet code provided on https://wiki.wxpython.org/ModelViewPresenter

#####WX IMPORTS#####
#wx- GUI toolkit for the Python programming language. wxPython can be used  to create graphical user interfaces (GUI).
import wx
#wx.lib.scrolledpanel- fills a “hole” in the implementation of ScrolledWindow.
#providing automatic scrollbar and scrolling behavior and the tab traversal management that ScrolledWindow lacks.
import wx.lib.scrolledpanel

import wx.grid


from ConfigurationWindow import MyConfigurationBoxSizer
from FluorescenceWindow import MyFluorescenceBoxSizer
from ImageWindow import MyImageBoxSizer
from DatabaseWindow import MyDatabaseBoxSizer

class ImageUI(wx.Frame):
    def __init__(self, parent, title):
        self.app = wx.App()
        super(ImageUI, self).__init__(parent, title = title, size=(1700, 1120))
        
        self.isMouseClicked = False
        
        ## New parameters added by Pierre
        self.isDummyImage = True  # when the image is simply a 1 by 1 pixel or that
                                    # no image has yet been selected
        self.cameraPosition = "TEST" # HORIZONTAL or VERTICAL
        self.cameraType = "FLIR" # FLIR or Andor
        self.isFluorescenceOn = False

        ## new parameters added by Hyungmok
        self.magnification = 1
        self.rawAtomNumber = 1

        self.chosenLayerNumber = 4

        self.imageDisplayed = None

        # self.currentXProfile = None
        # self.currentYProfile = None
        # self.currentXProfileFit = None
        # self.currentYProfileFit = None
        
        # self.isRotationNeeded = False
        # self.prevImageAngle = 0.
        # self.imageAngle = 0.
        # self.imagePivotX = 1
        # self.imagePivotY = 1

        self.xLeft_Primary = None
        self.xRight_Primary = None
        self.yBottom_Primary = None
        self.yTop_Primary = None
        
        self.rect_Primary =  None
        
        self.xLeft_Secondary = None
        self.xRight_Secondary = None
        self.yBottom_Secondary = None
        self.yTop_Secondary = None
        
        self.rect_Secondary =  None
        
        # self.defringingRefPath = None
        self.imageID = None
        self.imageIDIndex = 0
        self.data = None
        self.currentImg = None   # To merge with imageDisplayed
        
        # The list of files in the chosen filetype
        self.imageIDList = []

        ######
        ## Initialize dummy data and image
        # self.initializeDummyData()

        #################
        ## Initialize the UI


        # self.fitMethodGaussian.SetValue(True)
        # self.layer4Button.SetValue(True)
        self.autoRunning = False

        # self.FLIRCamera.SetValue(True) # doesn't exist anymore
        
        ####################
        ## for defringing ##
        # self.defringer = defringer()
        # self.betterRef = None
        
        # ## degenerate Fitter
        # self.degenFitter = degenerateFitter()
        # self.x_tOverTc = -1.
        # self.x_thomasFermiRadius = 1.
        # self.x_becPopulationRatio= 0.
        
        # self.y_tOverTc = -1.
        # self.y_thomasFermiRadius = 1.
        # self.y_becPopulationRatio= 0.
        
        #####################
        ## for filters ##
        # self.isMedianFilterOn = False
        # self.isNormalizationOn = False
        self.start()


    def InitUI(self):
#        self.panel = wx.Panel(self)
        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self, id = -1, size = (1,1)) # does the size even matter?
        self.panel.SetupScrolling()

        # self.SetIcon(wx.Icon('./icons/wxwin.ico', wx.BITMAP_TYPE_ICO))

        self.mainBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        # this is the general box: its left part are the setting, 
        # and its right part the image/Ncounts
        self.configFluoBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.configuration = MyConfigurationBoxSizer(self.panel)    # this is the setting vertical box
        self.fluorescence = MyFluorescenceBoxSizer(self.panel)
        self.configFluoBoxSizer.Add(self.configuration, 0, wx.ALL|wx.EXPAND, 5)
        self.configFluoBoxSizer.Add(self.fluorescence, 0, wx.ALL|wx.EXPAND, 5)
        
        self.image = MyImageBoxSizer(self.panel)
        self.database = MyDatabaseBoxSizer(self.panel)
        # vbox0 = wx.BoxSizer(wx.VERTICAL)
        self.mainBoxSizer.Add(self.configFluoBoxSizer, 2, wx.ALL|wx.EXPAND, 5)  # 2 here means that the relative width of the box will be 2
        # self.mainBoxSizer.Add(self.configuration, 2, wx.ALL|wx.EXPAND, 5)
        self.mainBoxSizer.Add(self.image, 4, wx.ALL)
        self.mainBoxSizer.Add(self.database, 2, wx.ALL, 5)  # 2 here means that the relative width of the box will be 2
        self.panel.SetSizer(self.mainBoxSizer)
    
    def start(self):
        self.InitUI()
        self.Centre()
        self.Show()
    
    def setFluorescenceNCount(self, nCount):
        self.fluorescenceMonitor.setFluorescenceNCount(nCount)
    
    def setFluorescenceGraph(self, nCountList):
        self.fluorescence.setFluorescenceGraph(nCountList)
    
    def clearImage(self):
        self.image.clearImage()
    
    def setImage(self, image):
        self.image.setImage(image)
    
    def getImageLayerSelection(self):
        self.image.getImageLayerSelection()
    
    def setPrimaryAOIDraw(self, cornersArray = None):
        self.image.setPrimaryAOIDraw(cornersArray)
    
    def setSecondaryAOIDraw(self, cornersArray = None):
        self.image.setSecondaryAOIDraw(cornersArray)
    
    def updateCursorValues(self, X, Y, Z):
        self.image.setCursorValues(X, Y, Z)
    
    def setPrimaryAOIValues(self, cornersArray = None):
        self.image.setPrimaryAOIValues(cornersArray)
    
    def setSecondaryAOIValues(self, cornersArray = None):
        self.image.setSecondaryAOIValues(cornersArray)
    
    def setMagnification(self, magnification):
        self.image.setMagnification(magnification)
    
    def setPixelSize(self, pixelSize):
        self.image.setPixelSize(pixelSize)
    
    def setAtomNumber(self, atomNumber):
        self.image.setAtomNumber(atomNumber)
    
    def setDatabaseImageID(self, imageID):
        self.database.setDatabaseImageID(imageID)
    
    def setDatabaseRunID(self, runID):
        self.database.setDatabaseRunID(runID)
    
    def setDatabaseSequenceID(self, sequenceID):
        self.database.setDatabaseSequenceID(sequenceID)
    
    def setDatabaseTimestamp(self, timestamp):
        self.database.setDatabaseTimestamp(timestamp)
    
    def setDatabaseNCount(self, NCount):
        self.database.setDatabaseNCount(NCount)
    
    def setImageList(self, imageIDList):
        self.database.setImageList(imageIDList)



if __name__ == '__main__':
    print("here1")
    # app = wx.App()
    print("here2")
    ui = ImageUI(None, title='Atom Image Analysis Dy v2')
    print("here3")
    ui.setMagnification("3")
    ui.app.MainLoop()
    print("here4")

