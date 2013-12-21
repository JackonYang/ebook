# -*- coding: utf-8 -*-
#!/usr/bin/env python

import wx

from ObjectListView import ObjectListView, ColumnDefn

from controls import FlatFile

class MyFrame(wx.Frame):
    def __init__(self, file_repo, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.file_repo = file_repo
        self.Init()

    def Init(self):
        self.InitModel()
        self.InitWidgets()
        self.InitObjectListView()

    def InitModel(self):
        self.files = self.file_repo.get_filemeta()

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

        self.myOlv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnOpenFile)  # dlick to open a file

    def InitObjectListView(self):
        self.myOlv.SetColumns([
            ColumnDefn("Title", "left", 220, "get_dispname", stringConverter='%s', valueSetter='set_dispname'),
            ColumnDefn("Raw File Name", "left", 220, "get_rawname", stringConverter='%s', isEditable=False),
        ])
        self.myOlv.SetObjects(self.files)
        self.myOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

    def OnOpenFile(self, event):
        obj = self.myOlv.GetSelectedObject()
        self.file_repo.open_file(obj.file_id)
        
        #open_file(os.path.join(repo_path, self.idx2name[event.GetIndex()]))

if __name__ == '__main__':
    import os

    test_dir = 'test_demo'
    repo = FlatFile(test_dir)
    # add_path = '/media/document/book/calibre'
    add_path = os.path.expanduser('~')
    # repo.add_path(add_path, '*.pdf,')
    app = wx.PySimpleApp(1)
    wx.InitAllImageHandlers()

    frame_1 = MyFrame(repo, None, -1, "Flat File Explorer")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
