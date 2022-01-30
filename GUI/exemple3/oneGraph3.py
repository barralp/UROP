import wx

class Screen(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(900,500))

        self.SetBackgroundColour("#E4F1FE")
        self.Show(True)

        self.InitUI()

    def InitUI(self):

        pnlMain = wx.Panel(self, size=(900,500))

        # Setup Font
        #font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        #font.SetPointSize(9)

        # Setup horizontal box sizer
        self.bsMain = wx.BoxSizer(wx.HORIZONTAL)
        self.bsMain.SetDimension(0,0,900,500)

        # Setup LEFT box sizer
        self.bsLeft = wx.BoxSizer(wx.VERTICAL)
        self.bsLeft.SetMinSize((3*(self.GetSize()[0]/4),self.GetSize()[1]))

        # Make add button
        btnAdd = wx.Button(pnlMain, label="+", size=(50,50))

        # Add all the components to the LEFT sizer
        self.bsLeft.Add(btnAdd, flag = wx.ALIGN_LEFT )

        # Setup RIGHT bsMain sizer
        self.bsRight = wx.BoxSizer(wx.VERTICAL)
        self.bsRight.SetMinSize((self.GetSize()[0]/4,self.GetSize()[1]))

        # Make users headline
        stUsers = wx.StaticText(pnlMain, label="USERS")
        #stUsers.SetFont(font)

        # Make users list control
        lcUsers = wx.ListCtrl(pnlMain,style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        lcUsers.Show(True)
        lcUsers.InsertColumn(0,"user")
        lcUsers.InsertColumn(1,"status")

        # Add all the components to the RIGHT sizer
        self.bsRight.Add((-1,10))
        self.bsRight.Add(stUsers, flag=wx.LEFT | wx.EXPAND, border=5)
        self.bsRight.Add((-1,10))
        self.bsRight.Add(lcUsers, flag=wx.EXPAND)


        # Add the vertical sizers to the horizontal sizer
        self.bsMain.Add(self.bsLeft)
        self.bsMain.Add(self.bsRight)

        # Add the vertical sizer to the panel
        pnlMain.SetSizer(self.bsMain)
        self.bsMain.Layout()

if __name__ == '__main__':
    app = wx.App(False)
    frame = Screen(None, 'Layout')
    app.MainLoop()
