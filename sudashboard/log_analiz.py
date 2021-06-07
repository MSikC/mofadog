# -*- coding: utf-8 -*-
import re
import os
from .models import Log
import datetime

class Log_write:
    log_dir = '/var/log/httpd/'
    path = os.getcwd()
    log_history = '/root/myproject/sudashboard/history'


    def get_path(self):
        return self.path

    def str_to_datetime(self, time):
        return datetime.datetime.strptime(time.split(' ')[0], '%d/%b/%Y:%H:%M:%S')

    def get_pointer_time(self):
        try:
            pointer_time_str = Log.objects.latest('id').time
            pointer_time = self.str_to_datetime(pointer_time_str)
        except:
            pointer_time = datetime.datetime(2010,11,12,13,14,15,16)
        return pointer_time



    def get_history_log_order(self):

        flist = os.listdir(self.log_dir)
        logs = []
        for file in flist:
            if file != 'access_log' and 'error' not in file:
                logs.append(file)

        logs = sorted(logs)
        logs.append('access_log')
        return logs

    def log_parse(self):
        log_tuple_list = []
        logs = self.get_history_log_order()



        f_his = open(self.log_history, 'r')
        hrl = f_his.read()
        f_his.close()

        for log in logs:
            if log in hrl.split('|'):
                pass
            else:
                hisrtory_stamp_flag = True

                f = open(self.log_dir + log)
                for x in f:
                    time = x.split('"')[0].split(' - - ')[1][1:-2]
                    if self.str_to_datetime(time) > self.get_pointer_time():
                        hisrtory_stamp_flag = False
                        ip = x.split('"')[0].split(' - - ')[0]
                        rq = x.split('"')[1] + x.split('"')[2]
                        ua = x.split('"')[5]
                        log_tuple = (ip, time, rq, ua)
                        log_tuple_list.append(log_tuple)
                    else:
                        pass
                if hisrtory_stamp_flag and log != 'access_log' and log not in hrl.split('|'):
                    w_his = open(self.log_history, 'a+')
                    w_his.write(log + '|')
                    w_his.close()

        return log_tuple_list

    def log_insert(self):
        parse_lists = self.log_parse()
        log_lists = []

        for n in parse_lists:
            l = Log(ip=n[0], time=n[1], request=n[2], useragent=n[3])
            log_lists.append(l)
        Log.objects.bulk_create(log_lists)


def log_main():
    log = Log_write()
    log.log_insert()



if __name__ == '__main__':
    log_main()
