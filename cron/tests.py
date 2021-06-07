# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Cron_beat
import datetime
from django.utils import timezone
import cronbeat

# Create your tests here.#

class CronmodelTestCase(TestCase):
    def setUp(self):
        Cron_beat.objects.create(beat_date=timezone.now())

    def test_str(self):
        print Cron_beat.objects.all()[0].__str__()

    def test_cron_beat(self):
    	beat = cronbeat.beat()
    	print beat.beat_date
