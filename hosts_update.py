#! /usr/bin/env python
# -*- coding: gbk -*-

"""Windows Hosts Update Module

This module compare local hosts file with online source and automatically
decide whether to update the local file with adjustments and additional hosts
rules in default.txt of current folder.  If download timeout, it will try to
reach via proxy.

It can forced update local hosts, has a simple CMD interface with Silent Mode.

Example:
    $ python hosts_update.py [-s]

CMD interface will pop up after downloading from server without any parameter.
 Any parameter will lead to silent mode, that is, fully automatic update
 without interface or options.

TODO:

"""

import os
import urllib

deletes = [#'w3schools.com', 'www.w3schools.com'
    # 'db.tt', 'dropbox.com', 'www.dropbox.com', 'm.dropbox.com', 'dl-debug.dropbox.com',
    # 'linux.dropbox.com', 'd.dropbox.com', 'd.v.dropbox.com', 'dl-doc.dropbox.com',
    # 'api-d.dropbox.com', 'api.dropboxapi.com', 'api.dropbox.com', 'api.v.dropbox.com',
    # 'api-notify.dropbox.com', 'www.dropboxstatic.com', 'cfl.dropboxstatic.com',
    # 'dbxlocal.dropboxstatic.com', 'api-content.dropbox.com', 'api-content-photos.dropbox.com',
    # 'photos.dropbox.com', 'bolt.dropbox.com', 'photos-thumb.dropbox.com',
    # 'photos-thumb.x.dropbox.com', 'block.dropbox.com', 'block.v.dropbox.com',
    # 'cf.dropboxstatic.com', 'client-cf.dropbox.com', 'dl.dropbox.com', 'dl-web.dropbox.com',
    # 'dl.dropboxusercontent.com', 'photos-1.dropbox.com', 'photos-2.dropbox.com',
    # 'photos-3.dropbox.com', 'photos-4.dropbox.com', 'photos-5.dropbox.com',
    # 'photos-6.dropbox.com', 'status.dropbox.com', 'marketing.dropbox.com', 'blogs.dropbox.com',
    # 'forums.dropbox.com', 'snapengage.dropbox.com', 'notify.dropbox.com',
    # 'client-lb.dropbox.com', 'client-web.dropbox.com', 'client.dropbox.com',
    # 'client.v.dropbox.com', 'log.getdropbox.com', 'tumblr.com', 'tumblr.co', 'api.tumblr.com', 'www.tumblr.com',
    # 'cynicallys.tumblr.com', 'mx.tumblr.com', 'vt.tumblr.com', 'vt.media.tumblr.com', 'vtt.tumblr.com',
    # 'ls.srvcs.tumblr.com', 'px.srvcs.tumblr.com', 'assets.tumblr.com', 'secure.assets.tumblr.com',
    # 'secure.static.tumblr.com', 'media.tumblr.com', '24.media.tumblr.com', '30.media.tumblr.com', '31.media.tumblr.com',
    # '32.media.tumblr.com', '33.media.tumblr.com', '36.media.tumblr.com', '37.media.tumblr.com', '38.media.tumblr.com',
    # '39.media.tumblr.com', '40.media.tumblr.com', '41.media.tumblr.com', '42.media.tumblr.com', '43.media.tumblr.com',
    # '44.media.tumblr.com', '45.media.tumblr.com', '46.media.tumblr.com', '47.media.tumblr.com', '48.media.tumblr.com',
    # '49.media.tumblr.com', '50.media.tumblr.com', '65.media.tumblr.com', '66.media.tumblr.com', '67.media.tumblr.com',
    # '68.media.tumblr.com', '90.media.tumblr.com', '94.media.tumblr.com', '95.media.tumblr.com', '96.media.tumblr.com',
    # '97.media.tumblr.com', '98.media.tumblr.com', '99.media.tumblr.com'
    ]
delete_ends=['tumblr.com',]
# 待删除域名

alter = {  'twitter.com': ['t.co','card-dev.twitter.com'],
    #'www.google.com': [],
           }
replace={#'61.91.161.217':'216.58.200.33'
         }

"""dict: Domains to be altered and its source.

Domains in the values are to be altered according to the IP of its key,
 usually another accessible domain of the same website.

 Values are list variables.
"""

expend = {
    # '16.docs.google.com':
    #           ["17.docs.google.com", "18.docs.google.com", "19.docs.google.com",
    #            "20.docs.google.com", "21.docs.google.com", "22.docs.google.com",
    #            "23.docs.google.com", "24.docs.google.com", "25.docs.google.com",
    #            "26.docs.google.com", "27.docs.google.com", "28.docs.google.com",
    #            "29.docs.google.com", "30.docs.google.com", "31.docs.google.com",
    #            "32.docs.google.com", "33.docs.google.com", "34.docs.google.com",
    #            "35.docs.google.com", "36.docs.google.com", "37.docs.google.com",
    #            "38.docs.google.com", "39.docs.google.com", "40.docs.google.com"],
          'twitter.com': ['cards-dev.twitter.com']}
"""dict: Additional domains to be added.

The keys are the existing domain in online source file, values are domains to be added
with the same IP of the key.

Values are list variables.
"""

win_hosts_dir = r'C:\Windows\System32\drivers\etc\hosts'
"""str: Directory of hosts file in Windows system.

Besides, it also serves as the destination of file to be written/overwritten.

Value is string variable.
"""

file_dir= r"E:\py\tools\lid3\\"

def dlhosts():
    """Download and return hosts file from online source.

    Download the file from Github or Coding.net, use GoAgent Proxy with urllib2.ProxyHandler
     if direct download timeout after 5 seconds. GoAgent proxy needed.  If
     timeout without GoAgent, the program would stuck in here.

    Return:
        list: list format of hosts file.
    """
    from urllib.request import ProxyHandler, urlopen, build_opener

    url = {'github':'https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts',
               #'https://raw.githubusercontent.com/racaljk/hosts/master/hosts',
           'coding': "https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts"
                     # "https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts"
           }
    hosts_url = url['coding']
    try:
        return urlopen(hosts_url, timeout=5).readlines()
    except Exception:
        proxy_handler = ProxyHandler({"https": 'https://127.0.0.1:8087'})
        opener = build_opener(proxy_handler)
        return opener.open(hosts_url).readlines()

        # return open('E:\hosts').readlines()


def judge(dl=None):
    """Judge whether to update.

    Judge by comparing the time stamp in the online source file and local file.

    Args:
        dl (list[=dlhosts()]): optional, the online source hosts file in list format.

    Returns:
        bool: if online source file updates later than local file, return True,
         otherwise False.
    """
    if dl==None:
        dl= dlhosts()
    prev = open(win_hosts_dir, 'r').readlines()
    if len(prev) == 0:
        return True
    elif len(dl) == 0 or prev[2] == dl[2]:
        return False
    else:
        return True


def write(dl=None):
    try:
        add = open(file_dir+"default.txt", 'r').readlines()
    except IOError:
        add = []
        print('error')

    if dl == None:
        dl=add
    else:
        dl+=add

    save = open(win_hosts_dir, 'w')
    for i,each in enumerate(dl):
        if isinstance(each,bytes):
            dl[i]=dl[i].decode('utf-8')
    save.writelines(dl)
    save.close()


def update(dl=None, alter_switch=True):
    """Update the local hosts file.

    Update with optional hosts file in list format with additional
    adjustments and additional lines according to default.txt in the same folder.
    If default.txt doesn't exist, nothing in that file will be added without
    error.

    Args:
        dl (list[=dlhosts()]): optional, the online source hosts file in list format.

    Returns:
        None.
    """
    global deletes
    err=None
    replace_list=replace.keys()

    if dl==None:
        dl=dlhosts()

    try:
        add = open('default.txt','r').readlines()#r'E:\py\tools\lid\default.txt', 'r').readlines()
    except IOError as error:
        print (error)
        err=error
        add = []

    if alter_switch:
        for (key, value) in alter.items():
            deletes += value
            if key in expend:
                expend.update({key: (value + expend[key])})
            else:
                expend.update({key: value})

    l = len(dl)
    i = 0
    while i < l:
        line = dl[i].decode('utf-8')  # 一行IP和域名
        if line[0] == '#' or line == '\n':
            i += 1
            continue

        cut = line.split('\t')  # -> [IP,域名]
        ip=cut[0]
        domain = cut[1][:-1]

        if ip in replace_list:
            dl[i]=replace[ip] + '\t' + domain + '\n'

        if domain in deletes:
            del dl[i]
            l -= 1
            i -= 1
            deletes.remove(domain)

        if domain in expend.keys():
            for item in expend[domain]:
                add.append(ip + '\t' + item + '\n')

        i += 1

    write(dl + add)
    return err


if __name__ == '__main__':
    """CMD interface.

    Firstly, download file from online source.  If local file is updated,
     print '已刷新 hosts', otherwise print '未更新 hosts' and the time
     online source file and local file was updated.

     Three options are
      显示hosts: open hosts file with notepad.exe of windows.
      强制刷新: force update with obsolete online source hosts file.
      打开add列表: open default.txt containing additional hosts lines in
        current folder.  If default.txt doesn't exist, throw an error.
      清空

    Exit with Enter button.
    """
    import sys

    dl = dlhosts()
    os.system('cls')

    if judge(dl):
        update(dl)
        if len(sys.argv) != 1:
            exit()
        print('已刷新 hosts')
    else:
        if len(sys.argv) != 1:
            exit()

        import time

        print('未更新 hosts')
        print('上次是', dl[2].split(' ')[-1], '今天是', time.strftime('%Y-%m-%d'))

    import subprocess

    input_message = '''
0.显示hosts
1.强制刷新
2.打开add列表
3.清空hosts
4.打开default列表
回车：退出
        '''


    def run(choice):
        if choice == '':
            exit()
        elif choice == '0':
            subprocess.Popen([r'C:\WINDOWS\system32\notepad.exe',
                              win_hosts_dir])
            return
        elif choice == '1':
            update(dl, True)
            return
        elif choice == '2':
            subprocess.Popen([r'C:\WINDOWS\system32\notepad.exe',
                              file_dir + "default.txt"])
            return
        elif choice == '3':
            write()
            return
        elif choice=="4":
            subprocess.Popen([r'C:\WINDOWS\system32\notepad.exe',
                              file_dir + "default.txt"])
        else:
            raise IndexError('选项错误！')


    # run('1')
    while 1:
        try:
            run(input(input_message))
        except IndexError as error:
            print(error)
            os.system('pause')
        finally:
            os.system('cls')


