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

class ImageUI(wx.Frame):
    def __init__(self, parent, title):
        self.app = wx.App()
        super(ImageUI, self).__init__(parent, title = title, size=(200, 200))
        self.start()


    def InitUI(self):
        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self, id = -1, size = (1,1)) # does the size even matter?
        self.panel.SetupScrolling()
        self.mainBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.textCtrl = wx.TextCtrl(self.panel, style = wx.TE_READONLY)
        self.text = wx.StaticText(self.panel, label = "Hello")
        self.mainBoxSizer.Add(self.text, flag = wx.ALL)
        self.mainBoxSizer.Add(self.textCtrl, flag = wx.ALL)
        self.panel.SetSizer(self.mainBoxSizer)
    
    def start(self):
        self.InitUI()
        self.Centre()
        self.Show()

if __name__ == '__main__':
    print("here1")
    # app = wx.App()
    print("here2")
    ui = ImageUI(None, title='Atom Image Analysis Dy v2')
    print("here3")
    ui.app.MainLoop()
    print("here4")

