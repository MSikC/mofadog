# -*- coding:utf-8 -*-
from dashboard.models import Order
from sudashboard.log_analiz import log_main
from .models import Cron_beat
import datetime
from django.utils import timezone

def beat():
    #log
    log_main()


    #beat
    beat_time = timezone.now()
    total_flow = 0
    for order in Order.objects.all():
        total_flow += order.flow_up + order.flow_down
        if beat_time > order.dead_date:
            order.enable = False
            order.save()

    beat = Cron_beat(beat_date=beat_time, total_flow=total_flow, beat_date_flow=0)
    beat.save()
    last_beat_pk = beat.pk - 1
    try:
        last_beat = Cron_beat.objects.get(pk=last_beat_pk)
        beat.beat_date_flow = beat.total_flow - last_beat.total_flow
        beat.save()

    except:
        pass

    return beat

def month_beat():
    for order in Order.objects.all():
        order.flow_up = 0
        order.flow_down = 0
        order.save()