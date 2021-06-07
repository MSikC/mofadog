# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from log_analiz import Log_write
from .models import Log
from .views import
# Create your tests here.

class LogTestCase(TestCase):

    def test_get_path(self):
        log_case = Log_write()
        self.assertEqual(log_case.get_path(), '/root/myproject')

    def test_get_pointer_time(self):
        log_case = Log_write()
        print log_case.get_pointer_time()

    def test_get_history_log_order(self):
        log_case = Log_write()
        print log_case.get_history_log_order()

    def test_log_parse(self):
        log_case = Log_write()
        log_list = log_case.log_parse()
        print len(log_list)
        print log_list[0]
    def test_log_insert(self):
        log_case = Log_write()
        log_case.log_insert()
        print Log.objects.count()
        print Log.objects.latest('id')
        acl = log_case.log_dir + 'access_log'
        with open(acl, 'r') as f:

            lines = f.readlines()
            print lines[-1]

