# -*- coding: utf-8 -*-
import requests
import threading
import sys
import signal
import time


##python findthepath.py -u http://127.0.0.1/find -t 3 -o 10 -d path.txt -s save.txt
def _init_(banner):
    path_list = ['-u', '', '-t', '', '-s', '', '-d', '', '-o', '']
    a = sys.argv[1]
    b = sys.argv[3]
    c = sys.argv[5]
    d = sys.argv[7]
    l = sys.argv[9]
    if a in path_list:
        e = path_list.index(a) + 1
        path_list[e] = sys.argv[2]
    else:
        print(banner)
        sys.exit(0)
    if b in path_list:
        f = path_list.index(b) + 1
        path_list[f] = sys.argv[4]
    else:
        print(banner)
        sys.exit(0)
    if c in path_list:
        g = path_list.index(c) + 1
        path_list[g] = sys.argv[6]
    else:
        print(banner)
        sys.exit(0)
    if d in path_list:
        h = path_list.index(d) + 1
        path_list[h] = sys.argv[8]
    else:
        print(banner)
        sys.exit(0)
    if l in path_list:
        j = path_list.index(l) + 1
        path_list[j] = sys.argv[10]
    else:
        print(banner)
        sys.exit(0)

    url = path_list[1]  # 网址
    thrd = int(path_list[3])  # 线程数
    global save
    save = open(path_list[5], 'a')  # 查询到的地址保存到文件的路径
    dict_file = path_list[7]  # 字典的路径
    over_time = int(path_list[9])  # 超时时间
    return url, thrd, save, dict_file, over_time


def _dict(dict_file):
    file = open(dict_file, 'r')
    files = file.readlines()
    num = len(files)  # 字典中fuzz的数量
    return num, files


def _send_(files, thred, i, url, save, over_time):
    flag = 0  # 丢包次数
    for admin in files[i * thred:(i + 1) * thred]:

        if flags:
            break
        try:
            admin = admin.strip('\n')
            new_url = url + '/' + admin
            s = requests.get(url=new_url, timeout=over_time)

            if s.status_code != 404:
                print('find address --', admin, '| stadus -- ', s.status_code)
                save.write(admin + '\n')
                '''
                如果不是404则将其写入save文件
                '''
        except:
            print('find address --', admin, '| stadus -- ')
            save.write(admin + '\n')
            '''
            如果不是404则将其写入save文件
            '''
            print(flag)
            flag += 1
            if flag % 10000 == 0:
                print('Already lose', flag, 'packets')
                # 每丢10000个包提醒一次
    global over
    over += 1
    if over == thrd:
        print("------------------------------------------Down--------------------------------------------------")
        # 结束
        save.close()
        print('Please input Ctrl+C to quit')


def _send():
    banner = '''
    --------------------------------------
    |       Please input:                |
    |       -u url                       | 
    |       -t thread count              |
    |       -s save to file              |
    |       -d catalog dictionary        |
    |       -o timeout to request        |
    -------------------------------------|
    ##python findthepath.py -u http://127.0.0.1/find -t 3 -o 10 -d path.txt -s save.txt
            '''
    global thrd
    try:
        url, thrd, save, dict_file, over_time = _init_(banner)
    except:
        print(banner)
        sys.exit(0)
    # 获取初始数据,若缺少则返回banner并退出
    num, files = _dict(dict_file)  # 使用文件,此处调用没太大意义
    thread_list = []
    if num % thrd == 0:
        thred = num // thrd
    else:
        thred = num // thrd
        thrd += 1
    # 每个线程要尝试的fuzz次数,非整除则加一
    print('''
    ___     _                _    _____   _                 ___            _      _      
   | __|   (_)    _ _     __| |  |_   _| | |_      ___     | _ \  __ _    | |_   | |_    
   | _|    | |   | ' \   / _` |    | |   | ' \    / -_)    |  _/ / _` |   |  _|  | ' \   
  _|_|_   _|_|_  |_||_|  \__,_|   _|_|_  |_||_|   \___|   _|_|_  \__,_|   _\__|  |_||_|  
_| """ |_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_| """ |_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
========================================================================================
    ''')
    for i in range(0, thrd):
        t = threading.Thread(target=_send_, args=(files, thred, i, url, save, over_time))
        thread_list.append(t)
        t.setDaemon(True)
        t.start()
        # 开启线程
    time.sleep(1000000)


def signal_handler(signal, frame):
    global flags
    global save
    print('You pressed Ctrl+C!')
    flags = True
    try:
        save.close()
    except:
        pass
    sys.exit(0)
#遇到Ctrl+C停止运行

if __name__ == '__main__':
    over = 0
    flags = False
    signal.signal(signal.SIGINT, signal_handler)#获取键盘响应
    _send()
