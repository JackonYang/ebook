# -*- coding: utf-8 -*-
#!/usr/bin/python
import wx


class ConnectDialog(wx.Dialog):

    def __init__(self, db, parent=None):
        self.db = db
        wx.Dialog.__init__(self, parent=parent, id=-1)
        self.SetTitle("Connect Mongo")

        input_style = wx.TE_PROCESS_ENTER
        label_host = wx.StaticText(self, label="Host: ")
        label_port = wx.StaticText(self, label="Port: ")
        self.input_host = wx.TextCtrl(self, size=(150, -1),
                                      value='localhost', style=input_style)
        self.input_port = wx.TextCtrl(self, size=(150, -1),
                                      value='27017', style=input_style)

        # connet if user press enter
        self.input_host.Bind(wx.EVT_TEXT_ENTER, self.OnConnect)
        self.input_port.Bind(wx.EVT_TEXT_ENTER, self.OnConnect)

        self.button_connect = wx.Button(self, label='Connect')
        self.button_connect.Bind(wx.EVT_BUTTON, self.OnConnect)

        self.input_host.SetFocus()

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        flexgrid_inputs = wx.FlexGridSizer(3, 2, 10, 10)
        flexgrid_inputs.SetFlexibleDirection = wx.HORIZONTAL
        flexgrid_inputs.AddMany([(label_host),
                                 (self.input_host, 0, wx.EXPAND),
                                 (label_port),
                                 (self.input_port, 0, wx.EXPAND),
                                 (wx.StaticText(self)),  # 样式占位
                                 (self.button_connect)
                                 ])
        sizer_main.Add(flexgrid_inputs, 1, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(sizer_main)

        self.SetAutoLayout(1)
        sizer_main.Fit(self)

    def OnConnect(self, event=None):
        host = self.input_host.GetValue()
        port = int(self.input_port.GetValue())
        if db.connect(host, port):
            self.EndModal(1)
        else:
            msg_error = 'Error connecting to host(%s)' % host
            wx.MessageBox(msg_error, 'Error', wx.OK | wx.ICON_ERROR)


if __name__ == '__main__':
    from lib.mongo_hdlr import MongodbHandler
    db = MongodbHandler()
    app = wx.PySimpleApp()
    dlg = ConnectDialog(db, parent=None)
    res = dlg.ShowModal()
    print 'run %s' % res
    dlg.Destroy()
