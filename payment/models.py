# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

@python_2_unicode_compatible

# Create your models here.
class History_order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=4)
    order_date = models.DateTimeField("order date", default=timezone.now)
    valid_date = models.DateTimeField("valid_date", default=timezone.now)
    dead_date = models.DateTimeField("daed_date", default=timezone.now)

    def __str__(self):
        return self.user.username

    def status(self):
        now = timezone.now()
        if now <= self.dead_date and now >= self.valid_date:
            return 1
        elif now < self.valid_date:
            return 0
        elif now > self.dead_date:
            return -1

class Activation_code(models.Model):
    activation_code = models.CharField(max_length=32)
    user = models.CharField(max_length=256, default='')
    activate_time_stamp = models.IntegerField(default=0)
    plan = models.CharField(max_length=5, default='M')
    enable = models.BooleanField(default=True)
    def __str__(self):
        return self.activation_code

class Pay(models.Model):
    orderNumber = models.CharField(max_length=32)
    money = models.IntegerField(default=0)
    username = models.CharField(max_length=256, default='')
    payconfirm = models.BooleanField(default=False)
    payChannel = models.CharField(max_length=32)
    def __str__(self):
        return self.orderNumber
