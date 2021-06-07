# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
from django.utils import timezone
@python_2_unicode_compatible
# Create your models here.


class Cron_beat(models.Model):

    beat_date = models.DateTimeField("beat date", default=timezone.now)
    total_flow = models.BigIntegerField(default=0)
    beat_date_flow = models.BigIntegerField(default=0)

    def __str__(self):
        return datetime.datetime.strftime(timezone.localtime(self.beat_date),'%Y-%m-%d %H:%M:%S')


