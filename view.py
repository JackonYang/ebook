# -*- coding: utf-8 -*-
#!/usr/bin/env python

import wx

from ObjectListView import ObjectListView, ColumnDefn
from ObjectListView import Filter
import model


class FlatFileFrame(wx.Frame):
    def __init__(self, controller):
        FrameStyle = wx.CAPTION | wx.RESIZE_BORDER | wx.SYSTEM_MENU |\
                     wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="Flat File Explorer", pos=(100, 100), size=(500,600), style=FrameStyle)
        self.controller = controller
        self.Init()

    def Init(self):
        self.InitModel()
        self.InitWidgets()
        self.InitObjectListView()
        self.InitSearchCtrls()

    def InitModel(self):
        self.elements = model.get_all()

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
        self.myOlv.Bind(wx.EVT_LIST_KEY_DOWN, self.OnKeyDown)
        # self.Bind(wx.EVT_BUTTON, self.OnAddPath, self.BtnAddPath)

    def InitObjectListView(self):
        self.myOlv.SetColumns([
            ColumnDefn("Title", "left", 330, "get_dispname", stringConverter='%s', valueSetter='set_dispname'),
            ColumnDefn("Language", "left", 80, "get_book_language", stringConverter='%s', valueSetter='set_book_language'),
            ColumnDefn("Size (MB)", "center", 80, "get_sizeInMb", stringConverter='%.1f', isEditable=False),
            ColumnDefn("MD5", "center", 320, "get_md5", stringConverter='%s', isEditable=False),
            # ColumnDefn("Raw File Name", "left", 420, "get_rawname", stringConverter='%s', isEditable=False),
        ])
        self.myOlv.SetObjects(self.elements)
        self.myOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

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
            searchCtrl.SetFocus()
            olv.SetFilter(Filter.TextSearch(olv, olv.columns[0:4]))

    def OnOpenFile(self, event):
        obj = self.myOlv.GetSelectedObject()
        filename = '%s%s' % (obj.file_id, obj.file_ext)
        self.controller.open_file(filename)

    def OnKeyDown(self, event):
        objs = self.myOlv.GetSelectedObjects()
        key = event.GetKeyCode()
        if wx.WXK_DELETE == key:
            self.DoDelete(objs)
        elif 3 == key:  # wx.WXK_CONTROL_C
            self.DoCopyFileid(objs)

    def DoDelete(self, objs):
        for obj in objs:
            self.controller.delete(obj.file_id, obj.file_ext)
        self.myOlv.RemoveObjects(objs)

    def DoCopyFileid(self, objs):
        self.dataObj = wx.TextDataObject()
        file_ids = ','.join([obj.file_id for obj in objs])
        wx.MessageBox(file_ids, "MD5 code")
        # self.dataObj.SetText(file_ids)
        # if wx.TheClipboard.Open():
        #   wx.TheClipboard.SetData(self.dataObj)
        #    wx.TheClipboard.Close()
        #else:
        #    wx.MessageBox("Unable to open the clipboard", "Error")

    def OnTextSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.ShowCancelButton(len(searchCtrl.GetValue()))
        olv.GetFilter().SetText(searchCtrl.GetValue())
        olv.RepopulateList()

    def OnCancelSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.SetValue("")
        self.OnTextSearchCtrl(event, searchCtrl, olv)


class FlatApp(wx.App):

    def __init__(self, controller):
        self.controller = controller
        wx.App.__init__(self)

    def OnInit(self):
        frame = FlatFileFrame(self.controller)
        self.SetTopWindow(frame)
        frame.Show()
        return True


if __name__ == '__main__':
    import storage
    repo_path = r'/media/document/booklist'
    controller = storage.build_repo(repo_path)
    app = FlatApp(controller)
    app.MainLoop()
