# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from dashboard.models import Node, Order
from .models import History_order
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .views import firewall_open_port
# Create your tests here.


class HistoryorderModeltest(TestCase):
    def setUp(self):
        u = User()
        u.save()
        History_order.objects.create(user=u,
                                     plan='T',
                                     order_date=timezone.now()-timedelta(days=1),
                                     valid_date=timezone.now()-timedelta(days=1),
                                     dead_date=timezone.now()+timedelta(days=1)
                                     )
    def test_status(self):
        ho = History_order.objects.all()[0]
        self.assertEqual(ho.status(),1)

    def test_tzinfo(self):
        ho = History_order.objects.all()[0]
        self.assertEqual(ho.order_date.tzinfo,None)

    def test_firewall_open_port(self):
        port = 20002
        shell_output = firewall_open_port(20002)
        print shell_output
        self.assertEqual(str(port) in shell_output, True)