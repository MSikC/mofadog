# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import time
import datetime
from django.utils import timezone

# Create your models here.
@python_2_unicode_compatible
class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    port = models.IntegerField(default=0)
    sspwd = models.CharField(max_length=32)
    lastConnTime = models.IntegerField(default=0)
    flow_up = models.BigIntegerField(default=0)
    flow_down = models.BigIntegerField(default=0)
    transfer = models.BigIntegerField(default=0)
    enable = models.BooleanField(default=True)
    method = models.CharField(max_length=32)
    plan = models.CharField(max_length=4)
    order_date = models.DateTimeField("order date", default=timezone.now)
    valid_date = models.DateTimeField("valid_date", default=timezone.now)
    dead_date = models.DateTimeField("daed_date", default=timezone.now)

    def __str__(self):
        return self.user.username

class Node(models.Model):

    ip = models.CharField(max_length=15)
    Remark = models.CharField(max_length=50)
    domain_name = models.CharField(max_length=32)
    group = models.CharField(max_length=4)

    def __str__(self):
        return self.ip


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',default=timezone.now)
    answer_text = models.CharField(max_length=200,null=True)

    def __unicode__(self):
        return u"%s"%self.question_text

class Notice(models.Model):
    pub_date = models.DateTimeField('date published', default=timezone.now)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    group = models.CharField(max_length=4, null=True)

    def __unicode__(self):
        return u"%s"%self.title
