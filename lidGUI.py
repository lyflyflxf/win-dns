#!/usr/bin/env python
# -*- coding: gbk -*-

from tkinter import *
import lid


class StdRedirector():
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.config(state=DISABLED)


class MyApp:
    def __init__(self, parent):
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()

        self.dns = lid.Dns()
        self.curr = u'当前DNS为：'
        self.intro = u'\n\n请选择:'

        self.topText = StringVar()
        self.topText.set(self.showCurrent())
        self.text = Message(self.myContainer1, width=600, textvariable=self.topText)
        self.text.grid(row=0, column=0, sticky=W, padx=1)

        self.text_list = [u"在ALI和ONE之间切换", u"PING剪切板上的地址", u"PING当前DNS和百度",
                          u"刷新DNS", u"更新hosts"]
        for (i, text) in enumerate(self.text_list):
            self.button1 = Button(self.myContainer1, text=text,
                                  background="tan", width=20)  # 按钮宽度，字符数
            eval('self.button1.bind("<Button-1>", self.button' + str(i + 1) + 'Click)')
            eval('self.button1.bind("<Return>", self.button' + str(i + 1) + 'Click)')
            self.button1.grid(row=i + 1, column=0, sticky=NW)

        self.pingOut = Text(self.myContainer1, width=60, height=15)
        self.pingOut.grid(row=0, column=1, sticky=NW, rowspan=len(self.text_list) + 1)
        self.pingOut.grid_remove()

    def button1Click(self, event):
        result = self.dns.switch()
        self.dns = lid.Dns()
        self.topText.set(result + u'\n' + self.showCurrent())

    def button2Click(self, event):
        import pyperclip
        self.pingOut.grid()
        run_ping(self.pingOut, pyperclip.paste())

    def button3Click(self, event):
        self.pingOut.grid()
        self.pingOut.delete('1.0', END)
        run_ping(self.pingOut, self.dns.server, multi=True)
        run_ping(self.pingOut, 'www.baidu.com', multi=True)

    def button4Click(self, event):
        self.topText.set(self.dns.refresh() + u'\n' + self.showCurrent())

    def button5Click(self, event):
        self.topText.set(u'正在更新...\n' + self.showCurrent())
        self.myContainer1.update_idletasks()
        lid.update()
        self.topText.set(u'更新成功\n' + self.showCurrent())

    def showCurrent(self):
        return self.curr + str(self.dns) + self.intro


def run_ping(widget, url, count=3, multi=False):
    def ping(url, first_line=False):
        text = ''
        if first_line:
            text = u'Ping ' + lid.url2domain(url) + u' ' + str(count) + u' Times:\n\n'

        result = lid.ping(url)
        if result['ip'] == '':
            text = text + u'Timeout.' + '\n'
        else:
            text = text + u'IP:' + result['ip'] + u' ,Time:' + str(result['time']) + '\n'
        return text

    if multi:
        widget.insert(END, u'\n')
    else:
        widget.delete("1.0", END)

    try:
        widget.insert(END, ping(url, first_line=True))
    except ValueError as e_message:
        widget.insert(END, u'网址有误：'+unicode(e_message))
    else:
        for i in range(count - 1):
            widget.insert(END, ping(url))


if __name__ == '__main__':
    root = Tk()
    root.title(u'DNS')
    myapp = MyApp(root)

    # # get screen width and height
    ws = str(int(root.winfo_screenwidth() / 3))
    hs = str(int(root.winfo_screenheight() / 3))

    root.geometry('+' + ws + '+' + hs)
    root.mainloop()