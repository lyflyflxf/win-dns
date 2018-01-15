#!/usr/bin/env python
# -*- coding: gbk -*-

from tkinter import *
import lid
import hosts_update as hu

class StdRedirector:
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.config(state=DISABLED)

class MyApp:
    def __init__(self, parent):
        self.c = Frame(parent)
        self.c.pack()
        self.top_text = StringVar()
        self.text = Message(self.c, width=600, textvariable=self.top_text,
                            font=('Times', '12'))
        self.text.grid(row=0, column=0, sticky=W, padx=1)
        text_list = ["Tencent/PaBo间切换", "PING剪切板上的地址", "PING当前DNS",
                          "刷新DNS", "更新hosts",'清空hosts','编辑default.txt','查看hosts']
        for (i, text) in enumerate(text_list):
            sn = str(i + 1)
            self.button = Button(self.c, text='%s. %s' % (sn, text),
                                 background="tan", width=20)  # 按钮宽度，字符数
            eval('self.button.bind("<Button-1>", self.button%s)'%sn)
            eval('self.button.bind("<Key-%s>", self.button%s)'% (sn,sn))
            # eval('self.button1.bind("<Return>", self.button' + str(i + 1) + ')')
            self.button.grid(row=i + 1, column=0, sticky=NW)

        self.textbox = Text(self.c, width=60, height=15)
        self.textbox.grid(row=0, column=1, sticky=NW, rowspan=len(text_list) + 1)
        self.textbox.grid_remove()

        self.dns = lid.Dns()
        self.head = u'当前DNS：'
        self.result = ''
        self.set_text()

    def button1(self, event):
        self.set_text(self.dns.switch())
        self.dns = lid.Dns()

    def button2(self, event):
        import pyperclip
        self.textbox.grid()
        run_ping(self.textbox, pyperclip.paste())

    def button3(self, event):
        self.textbox.grid()
        self.textbox.delete('1.0', END)
        for ip in self.dns.server:
            run_ping(self.textbox, ip, multi=True)

    def button4(self, event):
        self.set_text(self.dns.refresh())

    def button5(self, event):
        self.set_text('正在更新...')
        hu.update()
        self.set_text('更新成功')

    def button6(self, event):
        hu.write()
        self.set_text('hosts已清空')

    def button7(self, event):
        hu.edit()

    def button8(self, event):
        hu.view()

    def set_text(self, update=None):
        if update:
            self.result='\n'+update
        self.top_text.set(self.head + str(self.dns) + self.result)
        self.text.update()


def run_ping(widget, url, count=3, multi=False):
    def ping(url, first_line=False):
        text = ''
        if first_line:
            text = u'Ping ' + lid.url2domain(url) + u' ' + str(count) + u' Times:\n'
            widget.insert(END,text)
            text = ''
            widget.update()

        result = lid.ping(url)
        if result['ip']:
            text = text + 'IP: %(ip)s ,Time: %(time)d\n' % result
        else:
            text = text + u'Timeout.' + '\n'
        return text

    if multi:
        widget.insert(END, u'\n')
    else:
        widget.delete("1.0", END)

    try:
        widget.insert(END, ping(url, first_line=True))
    except ValueError as e_message:
        widget.insert(END, u'网址有误：'+str(e_message))
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