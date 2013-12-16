import wx
import sys
import os
import controls

class BookListFrame(wx.Frame):
    def __init__(self, repo_path):
        controls.build_repo(repo_path)
        wx.Frame.__init__(self, None, -1, 'Flat File')
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_EDIT_LABELS|wx.LC_NO_HEADER)
        self.list.InsertColumn(1001, '', format=wx.LIST_FORMAT_LEFT, width=500) 

        self.LoadData()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnOpenFile, self.list)  # dlick to open a file
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.SaveDispname, self.list)  # dlick to open a file

    def OnOpenFile(self, event):
        controls.open_file(self.idx2name[event.GetIndex()])

    def SaveDispname(self, event):
        dispname = event.GetLabel()
        idx_name = self.idx2name[event.GetIndex()]
        if not event.IsEditCancelled() and dispname:
            controls.update_dispname(idx_name, dispname)

        self.list.DeleteAllItems()
        self.LoadData()

    def LoadData(self, dataset=None):
        if dataset is None:
            dataset = controls.get_filelist()
        self.idx2name = {}
        for book in dataset:
            for bookname in controls.get_dispname(book):
                self.idx2name[self.list.InsertStringItem(sys.maxint, bookname)] = book

def main(repo_path):
    app = wx.PySimpleApp()
    frm = BookListFrame(repo_path)
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main('../book_repo')
