#!/usr/bin/env python
# -*- coding: gbk -*-

"""
TODO:
    multi-threading
"""
from tkinter import *
# import time
import hosts_update as hu
import subprocess


class MyApp:
    def __init__(self, parent):
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()

        self.topText = StringVar()
        self.text = Message(self.myContainer1, width=600, aspect=600, textvariable=self.topText)
        self.topText.set(u'��������...')

        self.text.grid(row=0, column=0, columnspan=3, sticky=E + W)

        self.text_list = [u"��ʾhosts", u"ǿ��ˢ��", u"��add�б�", u"PING���а��ϵĵ�ַ", u"����hosts"]
        for (i, text) in enumerate(self.text_list):
            if i % 2:
                bg = "tan"
            else:
                bg = "#FF8000"
            self.button1 = Button(self.myContainer1, text=text, background=bg,
                                  width=15) # ��ť��ȣ��ַ���
            eval('self.button1.bind("<Button-1>", self.button' + str(i + 1) + 'Click)')
            eval('self.button1.bind("<Return>", self.button' + str(i + 1) + 'Click)')
            self.button1.grid(row=1, column=i)

        root.update_idletasks()
        self.dl = hu.dlhosts()
        self.judge_update()

    def update(self):
        error= hu.update(self.dl)
        if error==None:
            text=u'��ˢ�� hosts'
        else:
            text=u'��ˢ�� hosts\n'+str(error)
        self.topText.set(text)

    def judge_update(self):
        if hu.judge(self.dl):
            self.update()
        else:
            import time
            self.topText.set(('δ���� hosts\n' + '�ϴΣ�' + self.dl[2].split(' ')[-1] +
                              '���죺' + time.strftime('%Y-%m-%d')).decode('gbk'))

    def button1Click(self, event):
        subprocess.Popen([r'C:\WINDOWS\system32\notepad.exe',
                          r"C:\Windows\System32\drivers\etc\hosts"])

    def button2Click(self, event):
        self.update()

    def button3Click(self, event):
        subprocess.Popen([r'C:\WINDOWS\system32\notepad.exe',
                          r"E:\py\tools\lid\add.txt"])

    def button4Click(self, event):
        import pyperclip
        from lidGUI import run_ping
        self.pingOut = Text(self.myContainer1, width=60, height=15)
        self.pingOut.grid(row=3, column=0, sticky=NW, columnspan=len(self.text_list))
        run_ping(self.pingOut, pyperclip.paste())

    def button5Click(self, event):
        hu.write()
        self.topText.set(u'�Ѱ�default����hosts')


if __name__ == '__main__':
    root = Tk()
    root.title(u'Hosts����')
    myapp = MyApp(root)
    root.mainloop()
