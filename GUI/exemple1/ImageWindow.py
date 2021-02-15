#!/usr/bin/python
# -*- coding: utf-8 -*-
# inspired by the snippet code provided on https://wiki.wxpython.org/ModelViewPresenter

#####WX IMPORTS#####
#wx- GUI toolkit for the Python programming language. wxPython can be used  to create graphical user interfaces (GUI).
import wx

#####MATPLOTLIB IMPORTS#####
import matplotlib
#matplotlib.use- sets the matplotlib backend to one of the known backends.
matplotlib.use('WXAgg')

#FigureCanvas- the FigureCanvas contains the figure and does event handling.
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import gridspec


class MyImageBoxSizer(wx.StaticBoxSizer):
    def __init__(self, parentPanel, label = 'Image'):
        imageBox = wx.StaticBox(parentPanel, label = label)
        super(MyImageBoxSizer, self).__init__(imageBox, wx.VERTICAL)
        self.panel = parentPanel
        self.init_imageBox_imagePlot()
        self.init_imageBox_imageInfo()
        self.init_imageBox_fittingResult()
        
    def init_imageBox_imagePlot(self):
    ######### images ##################
        self.figureImage = Figure(figsize = (8,8))
        gs = gridspec.GridSpec(2, 2, width_ratios=(7, 2), height_ratios=(7, 2), wspace = 0.05, hspace = 0.08)

        self.axes1 = self.figureImage.add_subplot(gs[0, 0])
        self.axes1.set_title('Original Image', fontsize=12)
        for label in (self.axes1.get_xticklabels() + self.axes1.get_yticklabels()):
            label.set_fontsize(10)

        self.axes2 = self.figureImage.add_subplot(gs[1, 0])
        self.axes2.grid(True)
        for label in (self.axes2.get_xticklabels() + self.axes2.get_yticklabels()):
            label.set_fontsize(10)

        self.axes3 = self.figureImage.add_subplot(gs[0, 1])
        self.axes3.grid(True)
        for label in (self.axes3.get_xticklabels()):
            label.set_fontsize(10)
        for label in (self.axes3.get_yticklabels()):
            label.set_visible(False)
            
        self.canvasImage = FigureCanvas(self.panel, -1, self.figureImage)
        self.Add(self.canvasImage, flag=wx.ALL|wx.SHAPED, border=5)
        # self.press= None find a new home for this one

    def init_imageBox_imageInfo(self):
        # 4 layer radio buttons
        imageConfigurationBoxSizer = wx.BoxSizer(wx.VERTICAL)
        layerTypeList = ["Probe With Atoms", "Probe Without Atoms",
                          "Dark Field", "Absorption Image"] 
        self.layerTypeRadioBox = wx.RadioBox(self.panel, 
                                              label = "Image layer",
                                              choices = layerTypeList,
                                              style = wx.RA_SPECIFY_COLS) 
        imageConfigurationBoxSizer.Add(self.layerTypeRadioBox, flag=wx.CENTER, border=5)
        
        imageReader = wx.BoxSizer(wx.HORIZONTAL)
        cursorXText = wx.StaticText(self.panel, label='X:')
        self.cursorX = wx.TextCtrl(self.panel,  style=wx.TE_READONLY|wx.TE_CENTRE, size = (50, 22))
        cursorYText = wx.StaticText(self.panel, label='Y:')
        self.cursorY = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_CENTRE,  size = (50, 22))
        cursorZText = wx.StaticText(self.panel, label='Value:')
        self.cursorZ = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_CENTRE,  size = (80, 22))
        imageReader.Add(cursorXText, flag=wx.ALL, border=5)
        imageReader.Add(self.cursorX, flag=wx.ALL, border=5)
        imageReader.Add(cursorYText, flag=wx.ALL, border=5)
        imageReader.Add(self.cursorY, flag=wx.ALL, border=5)
        imageReader.Add(cursorZText, flag=wx.ALL, border=5)
        imageReader.Add(self.cursorZ, flag=wx.ALL, border=5)
        smallBoldFont = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.cursorX.SetFont(smallBoldFont)
        self.cursorY.SetFont(smallBoldFont)
        self.cursorZ.SetFont(smallBoldFont)
        imageConfigurationBoxSizer.Add(imageReader,flag= wx.CENTER, border=5)
        self.Add(imageConfigurationBoxSizer, flag=wx.ALL|wx.EXPAND, border=5)
        # Maybe re-add the apply defringing reset AOI and median Filter options
        
        ###  AOI
        aoi_Box = wx.StaticBox(self.panel)
        aoi_BoxSizer = wx.StaticBoxSizer(aoi_Box, wx.HORIZONTAL)
        ### PRIMARY AOI
        aoi_PrimaryBox = wx.BoxSizer(wx.HORIZONTAL)
        aoi_PrimaryText = wx.StaticText(self.panel, label = 'Primary (blue) AOI: (x,y)->(x,y)')
        aoi_PrimaryBox.Add(aoi_PrimaryText, flag=wx.ALL, border=5)

        self.AOI1_Primary = wx.TextCtrl(self.panel, value='-1', size=(40,22))
        self.AOI2_Primary = wx.TextCtrl(self.panel, value='-1', size=(40,22))
        self.AOI3_Primary = wx.TextCtrl(self.panel, value='-1', size=(40,22))
        self.AOI4_Primary = wx.TextCtrl(self.panel, value='-1', size=(40,22))
        aoi_PrimaryBox.Add(self.AOI1_Primary, flag=wx.ALL, border=2)
        aoi_PrimaryBox.Add(self.AOI2_Primary, flag=wx.ALL, border=2)
        aoi_PrimaryBox.Add(self.AOI3_Primary, flag=wx.ALL, border=2)
        aoi_PrimaryBox.Add(self.AOI4_Primary, flag=wx.ALL, border=2)
        aoi_BoxSizer.Add(aoi_PrimaryBox, flag=wx.EXPAND|wx.ALL, border=5)

        ### SECONDARY AOI
        aoi_SecondaryBox = wx.BoxSizer(wx.HORIZONTAL)
        aoi_SecondaryText = wx.StaticText(self.panel, label = 'Secondary (color) AOI: (x,y)->(x,y)')
        aoi_SecondaryBox.Add(aoi_SecondaryText, flag=wx.ALL, border=5)

        self.AOI1_Secondary = wx.TextCtrl(self.panel, value='-1', size=(40,22))
        self.AOI2_Secondary = wx.TextCtrl(self.panel, value='-1', size=(40,22))
        self.AOI3_Secondary = wx.TextCtrl(self.panel, value='-1', size=(40,22))
        self.AOI4_Secondary = wx.TextCtrl(self.panel, value='-1', size=(40,22))
        aoi_SecondaryBox.Add(self.AOI1_Secondary, flag=wx.ALL, border=2)
        aoi_SecondaryBox.Add(self.AOI2_Secondary, flag=wx.ALL, border=2)
        aoi_SecondaryBox.Add(self.AOI3_Secondary, flag=wx.ALL, border=2)
        aoi_SecondaryBox.Add(self.AOI4_Secondary, flag=wx.ALL, border=2)
        aoi_BoxSizer.Add(aoi_SecondaryBox, flag=wx.EXPAND|wx.ALL, border=5)
        
        self.Add(aoi_BoxSizer, flag=wx.ALL| wx.EXPAND, border= 5)
        # imagesBoxSizer.Add(rotationBoxSizer, flag = wx.ALL | wx.EXPAND, border = 5)
        
        
        
    def init_imageBox_fittingResult(self):
        # Atom number
        atomNum = wx.StaticBox(self.panel, label='# of Atoms')
        atomNumBoxSizer = wx.StaticBoxSizer(atomNum, wx.HORIZONTAL)
        
        magnificationText = wx.StaticText(self.panel, label = 'Mag:')
        self.magnificationBox = wx.TextCtrl(self.panel, value = "1", size=(30,22))
        pixelSizeText = wx.StaticText(self.panel, label = u"\u00B5"+"m/pix:")
        self.pixelSizeBox = wx.TextCtrl(self.panel, value= "3.45", size=(35,22))
        # beware to bind that to something
        atomNumBoxSizer.Add(magnificationText, flag = wx.ALL, border = 5)
        atomNumBoxSizer.Add(self.magnificationBox, flag = wx.ALL, border = 5)
        atomNumBoxSizer.Add(pixelSizeText, flag = wx.ALL, border = 5)
        atomNumBoxSizer.Add(self.pixelSizeBox, flag = wx.ALL, border = 5)
        
        atomCountLabel = wx.StaticText(self.panel, label='Atom #:')
        self.atomCountText = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_CENTRE, size=(115,34))
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.atomCountText.SetFont(font)
        self.atomCountText.SetForegroundColour(wx.RED)
        atomNumBoxSizer.Add(atomCountLabel, flag=wx.ALL, border=5)
        atomNumBoxSizer.Add(self.atomCountText, flag=wx.ALL, border=5)
        
        self.Add(atomNumBoxSizer, flag=wx.ALL| wx.EXPAND, border=5)
        '''
        # Curve fit
        fittingResultDisplay = wx.StaticBox(self.panel, label = "Fitting results")
        fittingResultDisplaySizer = wx.StaticBoxSizer(fittingResultDisplay, wx.VERTICAL)
        
#        widthPeakStaticBox = wx.StaticBox(self.panel)
#        widthPeakSizer = wx.StaticBoxSizer(widthPeakStaticBox, wx.HORIZONTAL)
#
#        paramStaticBox = wx.StaticBox(self.panel)
#        parameterSettingSizer = wx.StaticBoxSizer(paramStaticBox, wx.HORIZONTAL)
#        tempStaticBox = wx.StaticBox(self.panel)
#        tempSizer = wx.StaticBoxSizer(tempStaticBox, wx.HORIZONTAL)
                
        TOFText = wx.StaticText(self.panel, label = 'TOF (ms): ' )
        self.TOFBox = wx.TextCtrl(self.panel, value = str(self.TOF), size=(40,22))
        self.TOFBox.Bind(wx.EVT_TEXT, self.setTOF)
        
        xTrapFreqText = wx.StaticText(self.panel, label = 'X trap freq.(Hz): ')
        self.xTrapFreqBox = wx.TextCtrl(self.panel, value = str(self.xTrapFreq), size=(40,22))
        self.xTrapFreqBox.Bind(wx.EVT_TEXT, self.setXTrapFreq)
        
        yTrapFreqText = wx.StaticText(self.panel, label = 'Y trap freq.(Hz): ')
        self.yTrapFreqBox = wx.TextCtrl(self.panel, value = str(self.yTrapFreq), size=(40,22))
        self.yTrapFreqBox.Bind(wx.EVT_TEXT, self.setYTrapFreq)

        widthText = wx.StaticText(self.panel, label = "Width (" + u"\u00B5"+ "m):")
        self.widthBox = wx.TextCtrl(self.panel,value = str(1)+",  " + str(1) , style=wx.TE_READONLY|wx.TE_CENTRE, size = (90, 22))
        peakText = wx.StaticText(self.panel, label = 'Peak (arb.): ')
        self.peakBox = wx.TextCtrl(self.panel,value = str(1)+",  " +str(1), style=wx.TE_READONLY|wx.TE_CENTRE, size = (85, 22))
        
        TcText = wx.StaticText(self.panel, label = "(T/Tc, Nc/N) :")
#        self.TcBox = wx.TextCtrl(self.panel,value = str(1)+",  " +str(1), style=wx.TE_READONLY|wx.TE_CENTRE, size = (90, 22))
        self.TcBox = wx.TextCtrl(self.panel,value = str(1)+",  " +str(0), style=wx.TE_READONLY|wx.TE_CENTRE, size = (75, 22))
        TFRadiusText = wx.StaticText(self.panel, label = "TF rad. (" + u"\u00B5"+ "m):")
#        self.TFRadiusBox = wx.TextCtrl(self.panel,value = str(1)+",  " +str(1), style=wx.TE_READONLY|wx.TE_CENTRE, size = (90, 22))
        self.TFRadiusBox = wx.TextCtrl(self.panel,value = str(1), style=wx.TE_READONLY|wx.TE_CENTRE, size = (55, 22))
        
        TempText = wx.StaticText(self.panel, label = "Temperature (" + u"\u00B5"+"K): ")
        TempText2 = wx.StaticText(self.panel, label = "long time limit (" +u"\u00B5" + "K): ")
        self.tempBox = wx.TextCtrl(self.panel, value = "(" + str(self.temperature[0])+", " +str(self.temperature[1]) + ")", style=wx.TE_READONLY|wx.TE_CENTRE, size = (160, 35))
        self.tempBox2 = wx.TextCtrl(self.panel, value = "(" + str(self.temperature[0])+", " +str(self.temperature[1]) + ")", style=wx.TE_READONLY|wx.TE_CENTRE, size = (160, 35))
        bigfont2 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.tempBox.SetFont(bigfont2)
        
        
        # hbox45 = wx.BoxSizer(wx.HORIZONTAL)
        # hbox45.Add(widthText, flag = wx.ALL, border = 5)
        # hbox45.Add(self.widthBox, flag = wx.ALL, border = 5)
        # hbox45.Add(peakText, flag = wx.ALL, border = 5)
        # hbox45.Add(self.peakBox, flag = wx.ALL, border = 5)
        # hbox45.Add(TcText, flag = wx.ALL, border = 5)
        # hbox45.Add(self.TcBox, flag = wx.ALL, border = 5)
        # hbox45.Add(TFRadiusText, flag = wx.ALL, border = 5)
        # hbox45.Add(self.TFRadiusBox, flag = wx.ALL, border = 5)
                        
        # hbox455 = wx.BoxSizer(wx.HORIZONTAL)
        # hbox455.Add(TOFText, flag = wx.ALL, border = 5)
        # hbox455.Add(self.TOFBox, flag = wx.ALL, border = 5)
        # hbox455.Add(xTrapFreqText, flag = wx.ALL, border = 5)
        # hbox455.Add(self.xTrapFreqBox, flag = wx.ALL, border = 5)
        # hbox455.Add(yTrapFreqText, flag = wx.ALL, border = 5)
        # hbox455.Add(self.yTrapFreqBox, flag = wx.ALL, border = 5)
        
        # hbox46 = wx.BoxSizer(wx.HORIZONTAL)
        # hbox46.Add(TempText, flag = wx.ALL, border = 5)
        # hbox46.Add(self.tempBox, flag = wx.ALL, border = 5)
        # hbox46.Add(TempText2, flag = wx.ALL, border = 5)
        # hbox46.Add(self.tempBox2, flag = wx.ALL, border = 5)
        
#        widthPeakSizer.Add(hbox45,  flag=wx.ALL|wx.EXPAND, border = 5)
#        parameterSettingSizer.Add(hbox455, flag=wx.ALL|wx.EXPAND, border = 5)
#        tempSizer.Add(hbox46, flag=wx.ALL|wx.EXPAND, border = 5)
        
        # fittingResultDisplaySizer.Add(hbox45, flag=wx.ALL| wx.EXPAND, border=5)
        # fittingResultDisplaySizer.Add(hbox455, flag=wx.ALL| wx.EXPAND, border=5)
        # fittingResultDisplaySizer.Add(hbox46, flag=wx.ALL| wx.EXPAND, border=5)
        
        # CHANGE THIS LINE TO ADD BACK THE FITTING RESULT DISPLAYER
        # imagesBoxSizer.Add(fittingResultDisplaySizer, flag=wx.ALL| wx.EXPAND, border=5)
        ## final step to add everything
        self.tempBox2.SetFont(bigfont2)
        
        '''
    def clearImage(self):
        self.axes1.cla()
    
    def setImage(self, image):
        self.axes1.imshow(image, cmap='gray_r', aspect='auto', vmin=-1, vmax=1)
    
    def setPrimaryAOIDraw(self, cornersArray = None):
        xLeft_Primary, xRight_Primary, yTop_Primary, yBottom_Primary = cornersArray
        if self.rect_Primary is None:
            self.rect_Primary = matplotlib.patches.Rectangle((0,0), 1, 1, facecolor="none",linewidth=2, edgecolor="#0000ff")
        self.axes1.add_patch(self.rect_Primary)
        self.rect_Primary.set_width(self.xRight_Primary - self.xLeft_Primary)
        self.rect_Primary.set_height(self.yBottom_Primary - self.yTop_Primary)
        self.rect_Primary.set_xy((self.xLeft_Primary, self.yTop_Primary))
        self.canvasImage.draw()
    
    def setSecondaryAOIDraw(self, cornersArray = None):
        xLeft_Secondary, xRight_Secondary, yTop_Secondary, yBottom_Secondary = cornersArray
        if self.rect_Secondary is None:
            self.rect_Secondary = matplotlib.patches.Rectangle((0,0), 1, 1, facecolor="none",linewidth=2, edgecolor="red")
            
        self.axes1.add_patch(self.rect_Secondary)
        self.rect_Secondary.set_width(self.xRight_Secondary - self.xLeft_Secondary)
        self.rect_Secondary.set_height(self.yBottom_Secondary - self.yTop_Secondary)
        self.rect_Secondary.set_xy((self.xLeft_Secondary, self.yTop_Secondary))
        self.canvasImage.draw()
    
    def getImageLayerSelection(self):
        return self.image.layerTypeRadioBox.GetSelection()
    
    def updateCursorValues(self, X, Y, Z):
        self.cursorX.SetValue(X)
        self.cursorY.SetValue(Y)
        self.cursorZ.SetValue(Z)
    
    def setMagnification(self, magnification):
        self.magnificationBox.SetValue(str(magnification))
    
    def setPixelSize(self, pixelSize):
        self.pixelSizeBox.SetValue(str(pixelSize))
        
    def setAtomNumber(self, atomNumber):
        self.atomCountText.SetValue(str(atomNumber))
    