import wx
import sys
import os
import json
import shutil
from util.kkfile import md5_for_file, open_file

base_path = os.path.realpath('..')

cache_path = os.path.join(base_path, 'book_cache')
repo_path = os.path.join(base_path, 'book_repo')
backup_path = os.path.join(repo_path, 'backup')


for path in [cache_path, repo_path]:
    if not os.path.exists(path):
        os.makedirs(path)

class BookIdx:

    def __init__(self, repo_path,
            json_name='archive.json',
            backup_basename='backup'):

        self.json_file = os.path.join(repo_path, json_name)
        self.backup_path = os.path.join(repo_path, backup_basename)

        if not os.path.exists(backup_path):
            os.makedirs(backup_path)


        self.idx = self.loads()  # auto load

    def add(self, md5_file, orig_name):
        if md5_file in self.idx:
            self.idx[md5_file].append(orig_name)
        else:
            self.idx[md5_file] = [orig_name]

    def backup(self):
        backup_file = os.path.join(self.backup_path, '%s.bak' % md5_for_file(self.json_file))
        if not os.path.isfile(backup_file):
            shutil.move(self.json_file, backup_file)

    def loads(self):
        try:
            with open(self.json_file, 'r') as f:
                content = f.read()
        except IOError:
            content = '{}'
        else:
            self.backup()
        return json.loads(content)

    def save(self):
        with open(self.json_file, 'w') as f:
            f.write(json.dumps(self.idx, indent=4, sort_keys=True))


def mv_ebook(orig_file, md5_file):
    # catch except when attempting to remove a file that is in use
    md5_file_full = os.path.join(repo_path, md5_file)
    orig_file_full = os.path.join(cache_path, orig_file)
    if not os.path.isfile(md5_file_full):
        shutil.move(orig_file_full, md5_file_full)
        print 'info | mv %s' % orig_file
    else:
        # log it, warning
        print 'warning | rm %s' % orig_file
        os.remove(orig_file_full)


def load_books():
    for bookfile in os.listdir(cache_path):
        md5 = md5_for_file(os.path.join(cache_path, bookfile))
        orig_name, ext = os.path.splitext(bookfile)
        md5_file = '%s%s' % (md5, ext)
        booklist.add(md5_file, orig_name)
        mv_ebook(bookfile, md5_file)



class BookListFrame(wx.Frame):
    def __init__(self, bookinfo):
        wx.Frame.__init__(self, None, -1, 'lean book')
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(1001, 'book list', format=wx.LIST_FORMAT_LEFT, width=500) 

        self.idx2name = {}
        for filename, showname in bookinfo.idx.items():
            for book in showname:
                self.idx2name[self.list.InsertStringItem(sys.maxint, book)] = filename
                
                
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnOpenFile, self.list)  # dlick to open a file

    def OnOpenFile(self, event):
        open_file(os.path.join(repo_path, self.idx2name[event.GetIndex()]))

booklist = BookIdx(repo_path)

app = wx.PySimpleApp()
frm = BookListFrame(booklist)
frm.Show()
app.MainLoop()
