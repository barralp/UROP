## needs to be implemented into the user interface so that it displays with the rest of the data
import wx
## file that deals with all the aspects of the graph 
from wx.lib.plot import PlotCanvas, PlotGraphics

def PlotData() :
    points = [] ## Will take 2d worth of points. For now will only plot BECHoldTime and nCount 

    return PlotGraphics("Title graph", "BECHoldTime", "nCount") ## eventually should figure out title switching depending on box that is selected

class DataGraph(wx.frame) :
    def __init__(self) :
        wx.frame.__init__(self, None, wx.ID_ANY, 'Data plotting tool')
        ## Add panel to make formatting correct
        panel = wx.Panel(self, wx.ID_ANY)

        self.canvas = PlotCanvas(panel)
        self.canvas.Draw()## figure out the points equivalent of bar graph
        toggleGrid = wx.CheckBox(panel, label="Show Grid")
        toggleGrid.Bind(wx.EVT_CHECKBOX, self.onToggleGrid)
    def onToggleGrid(self, event) :
        """"""
        self.canvas.SetEnableGrid(event.IsChecked())
    def selectVariables(self, widget, objects) :
        """"""
        for i in objects:
            widget.Append(i.make, i)
        widget.Bind(wx.EVT_COMBOBOX, self.varSwitch)
    
    def varSwitch(self, event) :
        """"""
    
    def retrieveData() :

