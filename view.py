# -*- coding: utf-8 -*-
#!/usr/bin/env python

import wx

from ObjectListView import ObjectListView, ColumnDefn

from controls import FlatFile

class MyFrame(wx.Frame):
    def __init__(self, data, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.Init(data)

    def Init(self, data):
        self.InitModel(data)
        self.InitWidgets()
        self.InitObjectListView()

    def InitModel(self, data):
        self.files = data

    def InitWidgets(self):
        panel = wx.Panel(self, -1)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(panel, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer_1)

        self.myOlv = ObjectListView(panel, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL|wx.EXPAND, 4)
        panel.SetSizer(sizer_2)

        self.Layout()

    def InitObjectListView(self):
        self.myOlv.SetColumns([
            ColumnDefn("Title", "left", 220, "get_dispname", stringConverter='%s'),
            ColumnDefn("Raw File Name", "left", 220, "get_rawname", stringConverter='%s'),
        ])
        self.myOlv.SetObjects(self.files)
        self.myOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

if __name__ == '__main__':
    import os

    test_dir = 'test_demo'
    repo = FlatFile(test_dir)
    repo.add_path(os.path.expanduser('~'), '*.pdf, jpg,.png,')
    data = repo.meta_mng.get_filemeta()

    app = wx.PySimpleApp(1)
    wx.InitAllImageHandlers()

    frame_1 = MyFrame(data, None, -1, "Flat File Explorer")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
