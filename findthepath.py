# -*- encoding: utf-8 -*-

import threading
from optparse import OptionParser
import requests
import time
import signal
import sys
class find_the_path():
    def __init__(self):
        global save_flag
        save_flag = True
        banner = '''    
    -----------------------------------------
    |       Please input:                  |
    |       -u --url Target url            | 
    |       -t --thread Thread count       |
    |       -s --save Save to file         |
    |       -d --dict Catalog dictionary   |
    |       -o --timeout Timeout to request|
    |--------------------------------------|
    ##python findthepath.py -u http://127.0.0.1/find -t 3 -o 10 -d path.txt -s save.txt
            '''
        parser = OptionParser(usage=banner,version='2.0')
        parser.add_option('-u','--url',dest='url',help='Please enter the target url')
        parser.add_option('-d','--dict',dest='dict_path',help='Please enter the path of dictionary')
        parser.add_option('-t','--thread',dest='thread',help='Please select the number of threads',type='int')
        parser.add_option('-s','--save',dest='save_path',help='Please enter the path to save the url')
        parser.add_option('-o','--timeout',dest='timeout',help='Please enter the request time')
        options,args = parser.parse_args()
        dict_path = options.dict_path
        save_path = options.save_path
        timeout = options.timeout
        if timeout == None:
            self.timeout=5
        else:
            self.timeout=timeout
        if dict_path == None:
            dict_path = 'path.txt'
        self.url = options.url
        try:
            self.dict_file = open(dict_path,'r',encoding='utf-8')
        except:
            print('Please enter the path of dictionary')
            sys.exit()
        if self.url ==None:
            print('Please enter the target url')
            sys.exit()
        self.thread_num = options.thread
        if self.thread_num == None:
            self.thread_num = 1
        try:
            self.save_file = open(save_path,'a')
        except:
            save_flag = False
    def find(self):
        global flag,save_flag
        while True:
            line = self.dict_file.readline().strip('\n')
            if line == '':
                flag = True
                break
            elif flag:
                break
            else:
                url = self.url+'/'+line
                try:
                    r = requests.get(url,timeout=self.timeout)
                    if r.status_code != 404:
                        print(line,r.status_code)
                        if save_flag:
                            self.save_file.write(url+'\n')
                except:
                    pass
    def shutdown(self):
        global flag
        flag = True
    def run(self):
        global flag
        flag = False
        thread_list = []
        print('''
     ___     _                _    _____   _                 ___            _      _      
   | __|   (_)    _ _     __| |  |_   _| | |_      ___     | _ \  __ _    | |_   | |_    
   | _|    | |   | ' \   / _` |    | |   | ' \    / -_)    |  _/ / _` |   |  _|  | ' \   
  _|_|_   _|_|_  |_||_|  \__,_|   _|_|_  |_||_|   \___|   _|_|_  \__,_|   _\__|  |_||_|  
_| """ |_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_| """ |_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
========================================================================================
##########################################start##########################################''')
        for i in range(self.thread_num):
            t = threading.Thread(target=self.find)
            t.start()
            thread_list.append(t)
        signal.signal(signal.SIGINT,self.shutdown)
        while not flag:
            time.sleep(10)
        print('#########################################down#########################################')
        try:
            self.save_file.close()
        except:
            pass
if __name__ == '__main__':
    find_the_path().run()
