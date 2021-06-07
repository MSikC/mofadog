# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import History_order, Activation_code, Pay
from django.contrib import admin

# Register your models here.
admin.site.register(History_order)
admin.site.register(Activation_code)
admin.site.register(Pay)