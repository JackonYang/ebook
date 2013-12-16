import wx
import sys
import os
import controls

class BookListFrame(wx.Frame):
    def __init__(self, repo_path):
        controls.build_repo(repo_path)
        wx.Frame.__init__(self, None, -1, 'Flat File')
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(1001, '', format=wx.LIST_FORMAT_LEFT, width=500) 

        self.idx2name = {}
        for book in controls.get_filelist():
            for bookname in controls.get_rawname(book):
                self.idx2name[self.list.InsertStringItem(sys.maxint, bookname)] = book

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnOpenFile, self.list)  # dlick to open a file

    def OnOpenFile(self, event):
        controls.open_file(self.idx2name[event.GetIndex()])

def main(repo_path):
    app = wx.PySimpleApp()
    frm = BookListFrame(repo_path)
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main('a')
