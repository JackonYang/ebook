# -*- coding: utf-8-*-

import os
import settings

import wx
import view

from control import FlatFile


controller = FlatFile(settings.repo_path)

for path in settings.to_add:
    print 'begin to add path %s' % path
    print controller.add_path(path, '*.pdf')
controller.save()

app = wx.PySimpleApp(redirect = False)
wx.InitAllImageHandlers()
frame_1 = view.FlatFileFrame(controller, None, -1, "Flat File Explorer")
app.SetTopWindow(frame_1)
frame_1.Show()
app.MainLoop()
