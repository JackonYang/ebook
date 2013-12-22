import os

import wx
import view
from controls import FlatFile
import settings

repo = FlatFile(settings.repo_path)

repo.add_path(settings.cache_path, '*.pdf')
app = wx.PySimpleApp(1)
wx.InitAllImageHandlers()

frame_1 = view.FlatFileFrame(repo, None, -1, "Flat File Explorer")
app.SetTopWindow(frame_1)
frame_1.Show()
app.MainLoop()
