# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Log(models.Model):
    ip = models.CharField(max_length=15)
    time = models.CharField(max_length=32)
    request = models.CharField(max_length=320)
    useragent = models.CharField(max_length=500)

    def __str__(self):
        return "%s-%s-%s-%s" % (self.ip, self.time, self.request, self.useragent)