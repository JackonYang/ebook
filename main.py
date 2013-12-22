# -*- coding: utf-8-*-

import os
import settings

import wx
import view

from controls import FlatFile


repo = FlatFile(settings.repo_path)

repo.add_path(settings.cache_path, '*.pdf')
repo.save()

app = wx.PySimpleApp(redirect = False)
wx.InitAllImageHandlers()
frame_1 = view.FlatFileFrame(repo, None, -1, "Flat File Explorer")
app.SetTopWindow(frame_1)
frame_1.Show()
app.MainLoop()
