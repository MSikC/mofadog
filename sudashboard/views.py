# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Log
from cron.models import Cron_beat
from django.shortcuts import render, redirect
import log_analiz
from django.utils import timezone
import datetime
import time
from payment.models import Activation_code
from payment.activate import generate_activation_code
from dashboard.models import Order
from django.core import serializers
# Create your views here.

def b_to_m(transfer):
    m_transfer = float(transfer)/1024/1024
    return round(m_transfer,2)

def intmonth_to_strmonth(num):
    month_dir = {
        '1':'Jan',
        '2':'Feb',
        '3':'Mar',
        '4':'Apr',
        '5':'May',
        '6':'Jun',
        '7': 'Jul',
        '8': 'Aug',
        '9': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec',
    }
    return month_dir[num]

def Create_json(request):
    if request.user.is_superuser:
        acodes_json = serializers.serialize("json", Activation_code.objects.filter(enable=True))
        json_file_name = generate_activation_code() + '.json'
        with open('/root/myproject/mysite/static/json/' + json_file_name, 'wb') as f:
            f.write(acodes_json)
        return redirect('/static/json/'+json_file_name)
    else:
        return redirect('/')

def Httpdlog(request, y_id, m_id, d_id):

    if request.user.is_superuser:
        #log_case = log_analiz.Log_write()
        #log_case.log_insert()
        logs = Log.objects.filter(time__startswith=d_id + '/' + intmonth_to_strmonth(m_id) + '/' + y_id)


        context = {
            "logs":logs,
        }
        return render(request, "sudashboard/superuser.html", context)
    else:
        return redirect('/')

def Flow_overview(request, y_id, m_id, d_id):
    if request.user.is_superuser:
        dt = datetime.datetime(int(y_id), int(m_id), int(d_id))
        dt_aware = timezone.make_aware(dt)
        crons = Cron_beat.objects.filter(beat_date__range = (dt_aware, dt_aware+datetime.timedelta(days=1)))
        m_flows = []
        for c in crons:
            m = c.beat_date_flow/1024/1024
            m_flows.append(m)
        zipped = zip(crons,m_flows)
        total_m_flows = sum(m_flows)
        context = {
            "zipped":zipped,
            'total_m_flows':total_m_flows
        }
        return render(request, "sudashboard/flow_overview.html", context)
    else:
        return redirect('/')

def Activations(request):
    if request.user.is_superuser:
        m_ac_list = []
        y_ac_list = []
        for i in range(100):
            ac_m = Activation_code(activation_code = generate_activation_code())
            ac_y = Activation_code(activation_code = generate_activation_code(),plan = 'Y')
            m_ac_list.append(ac_m)
            y_ac_list.append(ac_y)
        Activation_code.objects.bulk_create(m_ac_list)
        Activation_code.objects.bulk_create(y_ac_list)

        return redirect('/sudashboard/U')
    else:
        return redirect('/')

def Acode_overview(request,y_id, m_id, d_id):
    if request.user.is_superuser:
        acodes = Activation_code.objects.all()
        context = {
            'acodes':acodes,
        }
        return render(request, "sudashboard/acode_overview.html", context)
    else:
        return redirect('/')

def Order_overview(request,y_id, m_id, d_id):
    if request.user.is_superuser:
        orders = Order.objects.all()
        last_conn_datetimes = []
        bkmgs = []
        for o in orders:
            last_conn_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(o.lastConnTime))
            last_conn_datetimes.append(last_conn_datetime)
            bkmgs.append(b_to_m(o.flow_up + o.flow_down))
        zipped = zip(orders,last_conn_datetimes, bkmgs)
        context = {
            'zipped':zipped,
        }
        return render(request, "sudashboard/order_overview.html", context)
    else:
        return redirect('/')

def Url_redirect(request, page_id):
    if request.user.is_superuser:

        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        y = datetime.datetime.now().year
        if d < 10:
            d = '0' + str(d)
        else:
            d = str(d)
        return redirect('/sudashboard/' + str(y) + '/' + str(m) + '/' + str(d) + '/' + page_id)

    else:
        return redirect('/')