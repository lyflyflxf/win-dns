#!/usr/bin/env python
# -*- coding: gbk -*-

"""Network Adapter Information Module

pywin32 and wmi needed to run this script.

This module shows information of one current active network adapter, including the
name of DNS.  It also contain details in its attributes.

Example:
    python lid.py

Start the file will lead to a simple CMD interface.

Todo:

"""
import os
import wmi
import subprocess

import hosts_update

wmi = wmi.WMI()

def url2domain(url):
    import validators
    from urllib.parse import urlparse

    error = ValueError(url)
    error_class = validators.utils.ValidationFailure

    domain=''

    try:
        url = urlparse(url)
    except:
        raise error
    else:
        if url.netloc != '':
            domain = url.netloc
        elif url.path != '':
            domain = url.path
            if domain.find(r'/'):
                domain = domain.split(r'/')[0]
    # else:
    #     raise error

    if isinstance(validators.domain(domain), error_class) and (
            isinstance(validators.ipv4(domain), error_class)):
        raise error
    else:
        return domain


def ping(url):
    """Ping the url 3 times with maximal 255 TTL using windows ping command.

       Args:
           url (str):

       Returns:

       """
    result = wmi.Win32_PingStatus(Address=url2domain(url))[0]

    return {'ip': result.ProtocolAddress,
            'time': result.ResponseTime,
            'domain': url, }

def update():
    hosts_update.update()


def purge():
    hosts_update.write()


class Dns():
    ali = "Ali"
    one = "One"
    tencent = "Tencent"
    local = "Local"
    pabo = 'PaBo'

    '''DNS地址必须为tuple，如果只有一个IP，则必须在IP后且括号内加上逗号，如('xxx',)'''
    dict = {ali: ('223.5.5.5', '223.6.6.6'),
            one: ('114.215.126.16', '42.236.82.22'),
            tencent: ('119.29.29.29',),
            local: ('127.0.0.1', '223.6.6.6'),
            pabo: ('123.207.164.150','140.143.87.229', ), }

    def __init__(self):
        for each in wmi.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            if each.DefaultIPGateway is not None:
                # self.index = each.Index
                # self.ip = each.IPAddress[0]
                self.server = each.DNSServerSearchOrder
                self.now=each
                return

        self.server = '' #用wmi ping None貌似会陷入死循环
        return

    def set(self, i):
        options=[self.local,self.pabo]

        return_code= self.now.SetDNSServerSearchOrder(self.dict[options[i]])[0]

        if return_code == 0:
            return '修改成功'
        else:
            return '修改失败，错误代码：' + return_code

    def __repr__(self):
        if self.server=='':
            return 'No Internet Connection'
        for key,value in self.dict.items():
            if self.server == value:
                # print(key)
                return key + ' DNS'
        return str(self.server)

    def refresh(self):
        if self.__repr__() == 'Local':
            subprocess.Popen(['D:\Program Files (x86)\Acrylic-Portable\AcrylicController.exe',
                              'PurgeAcrylicCacheDataSilently'])
        else:
            text = os.popen('ipconfig /flushdns').readlines()[-1]
            if text.startswith('Successfully') or text.startswith('已成功'):
                return '刷新成功'
            else:
                return '刷新失败'

    def switch(self):
        """

              Returns:

              """
        l= [self.dict[x] for x in [self.tencent,self.pabo]]

        if self.server in l:
            l.pop(l.index(self.server))

        return_code = self.now.SetDNSServerSearchOrder(l[len(l) - 1])[0]
        self.refresh()
        if return_code == 0:
            return '修改成功'
        else:
            return '修改失败，错误代码：' + str(return_code)


if __name__ == '__main__':
    input_message = '''
    1.Tencent/PaBo间切换
    2.PING剪切板域名
    3.用PING检查网络
    4.刷新DNS
    5.更新hosts
    6.清空hosts
    7.编辑hosts
    8.编辑DNS规则
    回车：退出
'''

    acrylic_dir = 'D:\Program Files (x86)\Acrylic-Portable\AcrylicConfiguration.ini'
    pre_msg = ''

    def ping_print(url):
        try:
            out = ping(url2domain(url))
        except ValueError as e:
            print('异常网址：',e)
        else:
            print('\n正在 Ping %s，[%s]' % (out['domain'], out['ip']))
            for i in range(1, 4):
                print('%s：时间 %s ms' % (i, out['time']))


    def run(choice):
        if choice == '':
            exit()
        else:
            choice=int(choice)

        global pre_msg

        if choice == 1:
            pre_msg = dns.switch()
            return
        elif choice == 2:
            import pyperclip
            ping_print(pyperclip.paste())
            os.system('pause')
            return
        elif choice == 3:
            for ip in dns.server:
                ping_print(ip)
            ping_print('119.29.29.29')
            os.system('pause')
            return
        elif choice == 4:
            pre_msg = dns.refresh()
            return
        elif choice == 5:
            update()
            return
        elif choice == 6:
            purge()
            return
        elif choice == 7:
            subprocess.Popen([r"D:\Program Files (x86)\notepad++\notepad++.exe", ])
        elif choice == 8:
            subprocess.Popen([r'C:\WINDOWS\system32\notepad.exe',acrylic_dir])
        # elif choice == 9:
        #     subprocess.Popen(['D:\Program Files (x86)\Acrylic-Portable\AcrylicController.exe',
        #                       'StartAcrylicServiceSilently'])

        else:
            raise ValueError('选项错误！')


    os.system('cls')
    while 1:
        dns = Dns()
        print("%s 当前DNS为 %s，请选择："%(pre_msg, dns))

        try:
            run(input(input_message))
        except ValueError as error:
            print(error)
            os.system('pause')

        os.system('cls')
