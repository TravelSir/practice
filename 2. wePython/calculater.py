# -*- coding: utf-8 -*-
import wx
import math
"""待实现sqrt，log，平方，cos，sin，取模等功能"""


class CalcFrame(wx.Frame):
    def __init__(self, title):
        self.equation =''
        super(CalcFrame, self).__init__(None, title=title, size=(300, 250))
        self.init_ui()
        self.Center()
        self.Show()

    def init_ui(self):
        """
        首先定义BoxSizer，这个东西可以允许我们以行或列放置控件。我们先放个TextCtrl文本框，再放个GridSizer用来放置按钮。
        gridsizer允许我们以二维布局控件。四个参数分别是
        rows, 行数
        cols, 列数
        vgap, 格子之间垂直间隔
        hgap, 格子之间水平间隔
        因为定义了5行4列，因此依次放置20个按钮。
        """
        v_box = wx.BoxSizer(wx.VERTICAL)
        self.textprint = wx.TextCtrl(self, -1, style=wx.TE_RIGHT|wx.TE_READONLY)
        v_box.Add(self.textprint, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
        grid_box = wx.GridSizer(5, 4, 5, 5)
        labels = ['AC', 'DEL', 'pi', 'CLOSE', '7', '8', '9', '/', '4', '5', '6',
                  '*', '1', '2', '3', '-', '0', '.', '=', '+']
        # 计算器的重点在于Button的回调函数。点击不同按钮我们希望根据按钮的label选择不同的回调函数进行绑定。因此我们可以这样实现放置按钮到grid_box
        for label in labels:
            button_item = wx.Button(self, label=label)
            self.create_handler(button_item, label)
            grid_box.Add(button_item, 1, wx.EXPAND)
        v_box.Add(grid_box, proportion=1, flag=wx.EXPAND)
        self.SetSizer(v_box)

    def create_handler(self, button, labels):
        """根据label的不同，我们把按钮分别绑定到5个不同的回调函数上。"""
        item = 'DEL AC = CLOSE'
        if labels not in item:
            self.Bind(wx.EVT_BUTTON, self.on_append, button)
        elif labels == 'DEL':
            self.Bind(wx.EVT_BUTTON, self.on_del, button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON, self.on_ac, button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON, self.on_target, button)
        elif labels == 'CLOSE':
            self.Bind(wx.EVT_BUTTON, self.on_exit, button)

    def on_append(self, event):
        """添加运算符与数字"""
        event_button = event.GetEventObject()
        label = event_button.GetLabel()
        self.equation += label
        self.textprint.SetValue(self.equation)

    def on_del(self, event):
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def on_ac(self, event):
        self.textprint.Clear()
        self.equation = ''

    def on_target(self, event):
        string = self.equation
        try:
            target = eval(string)  # eval函数将字符串string对象转化为有效的表达式参与求值运算返回计算结果
            self.equation = str(target)
            self.textprint.SetValue(self.equation)
        except SyntaxError:
            dlg = wx.MessageDialog(self, '格式错误，请输出正确的等式！', '请注意', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def on_exit(self, event):
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    CalcFrame(title='Calculater')
    app.MainLoop()
