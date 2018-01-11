#!/usr/bin/env python
# -*- coding: gbk -*-

"""Network Adapter Information Module

pywin32 and wmi needed to run this script.

This module shows information of one current active network adapter, including the
name of DNS.  It also contain details in its attributes.

Example:
    python lid.py

Start the file will lead to a simple CMD interface.

"""
import os
import wmi
import subprocess
import hosts_update

wmi = wmi.WMI()


def url2domain(url):
    """Process url into domain suitable for ping in WMI

    Args:
        url (str):

    Returns:
        domain string
    """
    import validators
    from urllib.parse import urlparse

    err = ValueError(url)
    error_class = validators.utils.ValidationFailure
    domain = ''
    try:
        url = urlparse(url)
    except Exception:
        raise err
    else:
        if url.netloc != '':
            domain = url.netloc
        elif url.path != '':
            domain = url.path
            if domain.find(r'/'):
                domain = domain.split(r'/')[0]
    if isinstance(validators.domain(domain), error_class) and (
            isinstance(validators.ipv4(domain), error_class)):
        raise err
    else:
        return domain


def ping(url):
    """Ping the url using WMI functionality.

       Args:
           url (str):

       Returns:
           result parsed into dict
    """
    result = wmi.Win32_PingStatus(Address=url2domain(url))[0]
    return {'ip': result.ProtocolAddress,
            'time': result.ResponseTime,
            'domain': url, }

class Dns:
    ali = "Ali"
    one = "One"
    tencent = "Tencent"
    local = "Acrylic"
    pabo = 'PaBo'

    # DNS地址必须为tuple，如果只有一个IP，则必须在IP后且括号内加上逗号，如('xxx',)
    dict = {ali: ('223.5.5.5', '223.6.6.6'),
            one: ('114.215.126.16', '42.236.82.22'),
            tencent: ('119.29.29.29',),
            local: ('127.0.0.1', '223.6.6.6'),
            pabo: ('123.207.164.150', '140.143.87.229',), }

    def __init__(self):
        self.preferences = [self.pabo, self.tencent, ]  # preferred DNS servers
        for each in wmi.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            if each.DefaultIPGateway is not None:
                # self.index = each.Index
                # self.ip = each.IPAddress[0]
                self.server = each.DNSServerSearchOrder
                self.now = each
                return

        self.server = ''  # 用wmi ping None貌似会陷入死循环
        return

    def __repr__(self):
        """Provide DNS information for print.

        Returns:
            string of DNS server IP
        """
        if self.server == '':
            return 'No Internet Connection'
        for key, value in self.dict.items():
            if self.server == value:
                # print(key)
                return key + ' DNS'
        return str(self.server)

    def refresh(self):
        """Refresh DNS pool for the system or Acrylic

        Returns:
            Result of refreshment
        """
        if self.__repr__() == self.local:
            subprocess.Popen(['D:\Program Files (x86)\Acrylic-Portable\AcrylicController.exe',
                              'PurgeAcrylicCacheDataSilently'])
        else:
            text = os.popen('ipconfig /flushdns').readlines()[-1]
            if text.startswith('Successfully') or text.startswith('已成功'):
                return '刷新成功'
            else:
                return '刷新失败'

    def switch(self):
        """Switch DNS among preferred ones.

        Returns:
            Result of action
        """
        switches = [self.dict[x] for x in (self.preferences + [self.preferences[0]])]

        if self.server in switches:
            server = switches[switches.index(self.server) + 1]
        else:
            server = switches[0]

        return_code = self.now.SetDNSServerSearchOrder(server)[0]
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
    7.编辑default.txt
    8.查看hosts
    回车：退出
'''
    # 8.编辑Acrylic
    acrylic_dir = 'D:\Program Files (x86)\Acrylic-Portable\AcrylicConfiguration.ini'
    pre_msg = ''


    def ping_print(url):
        """Format the result of ping"""
        try:
            out = ping(url2domain(url))
        except ValueError as e:
            print('异常网址：', e)
        else:
            print('\n正在 Ping %s，[%s]' % (out['domain'], out['ip']))
            for i in range(1, 4):
                print('%s：时间 %s ms' % (i, out['time']))


    def run(choice):
        """Process choice from user"""
        if choice == '':
            exit()
        else:
            choice = int(choice)

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
            # ping_print('119.29.29.29')
            os.system('pause')
            return
        elif choice == 4:
            pre_msg = dns.refresh()
            return
        elif choice == 5:
            hosts_update.update()
            return
        elif choice == 6:
            hosts_update.write()
            return
        elif choice == 7:
            hosts_update.edit()
        elif choice == 8:
            hosts_update.view()
        #     subprocess.Popen([r'C:\WINDOWS\system32\notepad.exe',acrylic_dir])
        # elif choice == 9:
        #     subprocess.Popen(['D:\Program Files (x86)\Acrylic-Portable\AcrylicController.exe',
        #                       'StartAcrylicServiceSilently'])
        else:
            raise ValueError('选项错误！')

    os.system('cls')
    while 1:
        dns = Dns()
        print("%s 当前DNS为 %s，请选择：" % (pre_msg, dns))
        try:
            run(input(input_message))
        except ValueError as error:
            print(error)
            os.system('pause')
        os.system('cls')
