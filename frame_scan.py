#! /usr/bin/env python
#coding: utf-8
import wx
from lib.book_scan import BookScan


class ScanFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Book Import",
                          pos=(100, 100), size=(1180, 600))
        self.lstDisks = [u'/media/document/QSanguosha']  # TODO
        self.scan = None
        self.buildUI()
        self.CenterOnScreen()

    def buildUI(self):
        self.box1 = wx.BoxSizer(wx.HORIZONTAL)
        frameStyle = wx.TE_AUTO_SCROLL | wx.TE_MULTILINE
        self.text = wx.TextCtrl(parent=self, style=frameStyle)
        self.text.SetEditable(False)
        self.box1.Add(self.text, 1, wx.ALL | wx.EXPAND, 5, 5)

        self.toolbox = wx.BoxSizer(wx.VERTICAL)
        self.startBtn = wx.Button(parent=self, label="Start")
        self.toolbox.Add(self.startBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.stopBtn = wx.Button(parent=self, label="Stop")
        self.toolbox.Add(self.stopBtn, 1, wx.ALL | wx.EXPAND, 5, 0)
        self.box1.Add(self.toolbox, 0, wx.NORMAL, 0, 0)
        self.startBtn.Enable()
        self.stopBtn.Disable()

        self.SetSizer(self.box1)

        self.startBtn.Bind(wx.EVT_BUTTON, self.OnStartScan)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.OnStopScan)

    def OnStartScan(self, event):
        self.startBtn.Disable()
        self.stopBtn.Enable()
        # 检测日志，超过指定日志大小，就清空日志列表
        if len(self.text.GetValue()) > 1024:
            self.text.SetValue('')
        dlg = wx.DirDialog(self, "Choose a directory:")
        #, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.scan = BookScan(dlg.GetPath(), self.text.AppendText)
            # daemonic 为 True 时，表示主线程结束时子线程也要跟着退出
            self.scan.start()
            self.startBtn.Enable()
            self.stopBtn.Disable()

    def OnStopScan(self, event):
        if self.scan:
            self.scan.StopScan()
            self.startBtn.Enable()
            self.stopBtn.Disable()


class TestApp(wx.App):

    def OnInit(self):
        frame = ScanFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = TestApp()
    app.MainLoop()
