# -*- coding: utf-8 -*-
#!/usr/bin/env python

import wx

from ObjectListView import ObjectListView, ColumnDefn
from ObjectListView import Filter

from controls import FlatFile

class FlatFileFrame(wx.Frame):
    def __init__(self, file_repo, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.file_repo = file_repo
        self.Init()

    def Init(self):
        self.InitModel()
        self.InitWidgets()
        self.InitObjectListView()
        self.InitSearchCtrls()

    def InitModel(self):
        self.files = self.file_repo.get_filemeta()

    def InitWidgets(self):
        panel = wx.Panel(self, -1)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(panel, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer_1)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.SearchFile = wx.SearchCtrl(panel)
        sizer_2.Add(self.SearchFile, 1, wx.ALL|wx.EXPAND, 2)
        self.myOlv = ObjectListView(panel, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        sizer_2.Add(self.myOlv, 20, wx.ALL|wx.EXPAND, 4)

        # self.BtnAddPath = wx.Button(panel, -1, 'select path to add files')
        # sizer_2.Add(self.BtnAddPath, 1, wx.ALL|wx.EXPAND, 2)
        panel.SetSizer(sizer_2)

        self.Layout()

        self.myOlv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnOpenFile)  # dlick to open a file
        # self.Bind(wx.EVT_BUTTON, self.OnAddPath, self.BtnAddPath)

    def InitObjectListView(self):
        self.myOlv.SetColumns([
            ColumnDefn("Title", "left", 420, "get_dispname", stringConverter='%s', valueSetter='set_dispname'),
            ColumnDefn("Raw File Name", "left", 420, "get_rawname", stringConverter='%s', isEditable=False),
        ])
        self.myOlv.SetObjects(self.files)
        self.myOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

    def OnOpenFile(self, event):
        obj = self.myOlv.GetSelectedObject()
        self.file_repo.open_file(obj.file_id)

    def OnAddPath(self, event):
        dialog = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.file_repo.add_path(path)
            self.file_repo.save()
        dialog.Destroy()
        self.myOlv.RefreshObject(self.file_repo.get_filemeta())

    def OnTextSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.ShowCancelButton(len(searchCtrl.GetValue()))
        olv.GetFilter().SetText(searchCtrl.GetValue())
        olv.RepopulateList()

    def OnCancelSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.SetValue("")
        self.OnTextSearchCtrl(event, searchCtrl, olv)

    def InitSearchCtrls(self):
        """Initialize the search controls"""
        for (searchCtrl, olv) in [(self.SearchFile, self.myOlv)]:
            # Use default parameters to pass extra information to the event handler
            def _handleText(evt, searchCtrl=searchCtrl, olv=olv):
                self.OnTextSearchCtrl(evt, searchCtrl, olv)
            def _handleCancel(evt, searchCtrl=searchCtrl, olv=olv):
                self.OnCancelSearchCtrl(evt, searchCtrl, olv)
            searchCtrl.Bind(wx.EVT_TEXT, _handleText)
            searchCtrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, _handleCancel)
            olv.SetFilter(Filter.TextSearch(olv, olv.columns[0:4]))

        
        #open_file(os.path.join(repo_path, self.idx2name[event.GetIndex()]))

if __name__ == '__main__':
    import os
    import sys

    print sys.getdefaultencoding()

    test_dir = 'demo_repo'
    repo = FlatFile(test_dir)
    # add_path = '/media/document/book/calibre'
    add_path = os.path.expanduser('~')
    repo.add_path(add_path, '*.pdf,')
    repo.save()

    # app = wx.PySimpleApp(1)
    app = wx.PySimpleApp(redirect = False)
    wx.InitAllImageHandlers()
    frame_1 = FlatFileFrame(repo, None, -1, "Flat File Explorer")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
