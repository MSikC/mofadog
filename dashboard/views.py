# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from .models import Order, Node, Notice
from payment.models import History_order
import time
from datetime import datetime, timedelta, tzinfo
from django.http import HttpResponse
from . import qrname
from django.utils import timezone
import json
import os
import StringIO
import zipfile




def bkmg(transfer):
    Bytelist = ['B', 'K', 'M', 'G']
    bl_index = 0
    while transfer >= 1024:
        transfer = float(transfer)/1024
        bl_index += 1

    return str(round(transfer,2)) + Bytelist[bl_index]

# Create your views here.
def plan_get(plan_id):
    plan_d = {
        'T':'试用',
        'M':'月',
        'Y':'年'
    }
    return plan_d[plan_id]

def dt_to_timestamp(dt):
    return time.mktime(dt.timetuple())


def json_config(order, nodes):
    with open('/root/myproject/mysite/static/download/jsonandclient/emptyjson.json') as json_file:
        data = json.load(json_file)

    for node in nodes:
        data['configs'].append(
            {
                "server": node.ip,
                "server_port": order.port,
                "password": order.sspwd,
                "method": order.method,
                "plugin": "",
                "plugin_opts": "",
                "remarks": "",
                "timeout": 5
            }
        )

    txt = '''   ****************************
    欢迎使用Mofadog膜法上网
    ****************************
    
    %s, 您好
    您正在使用%s套餐
    您的套餐过期时间为：%s
    
    过期后，魔法上网将会提示500错误
    
    续费即可继续上网，官网地址：
    http://mofadog.com/
    
    查看流量情况，套餐剩余时间，使用教程，用户后台：
    http://mofadog.com/accounts/profile/'''%(order.user.username.encode(), plan_get(order.plan), order.dead_date.strftime("%Y-%m-%d %H:%M:%S"))
    return data, txt

def client_make(data, txt, user):
    path = '/root/myproject/mysite/static/download/client/' + user.username
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)

    #readme_make

    f = open(path + '/ReadMe.txt', 'w')
    f.write(txt)
    f.close()


    with open(path + '/gui-config.json', 'w') as json_file:
        json_file.write(json.dumps(data))
    ssexe = '/root/myproject/mysite/static/download/jsonandclient/Shadowsocks.exe'
    # Files (local path) to put in the .zip

    filenames = [path + '/gui-config.json', path + '/ReadMe.txt', ssexe]
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt

    zip_subdir = "shadoesocks_mofadog"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp






def Home(request):
    """View for the Index page of the website"""


    #导航
    if request.user.is_superuser:
        return redirect('/sudashboard/O')
    if request.user.is_anonymous():
        return redirect('/accounts/login')

    if request.user.order_set.count() == 0:
        return redirect('/payment/T/')



    order = Order.objects.get(user=request.user)


    #最近连接时间
    lastconntimestamp = order.lastConnTime
    if lastconntimestamp == 0:
        lastconntime = '未连接'
    else:
        lastconntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastconntimestamp))



    order_date = order.order_date
    order_deaddate = order.dead_date


    plan = order.plan
    if plan == 'T':
        plan_try = True

        #remaining time percent, try seconds
        remaining_s = (dt_to_timestamp(order_deaddate) - dt_to_timestamp(timezone.now()))
        remaining_time = round(remaining_s / 60, 1)
        total_seconds = (order_deaddate - order_date).seconds
        remaining_per = round(float(remaining_s) * 100 / float(total_seconds), 1)

    else:
        plan_try = False
        
        #remaining time percent, not try, days
        remaining_time = (order_deaddate - timezone.now()).days + 1
        total_day = (order_deaddate - order_date).days
        remaining_per = round(float(remaining_time) * 100 / float(total_day), 1)

    if remaining_per > 100:
        remaining_per = 100



    total_flows = order.flow_up + order.flow_down
    flow_text = bkmg(total_flows)
    rest_flow = order.transfer - total_flows
    rest_flow_text = bkmg(rest_flow)
    try_rest_transfer_per = round(rest_flow * 100 / float(order.transfer),1)









    #node_list
    nodes = Node.objects.all()
    sspwd = order.sspwd
    port = order.port
    method = order.method

    #qrcode
    qrcodes = []
    for node in nodes:
        qrcodes.append(qrname.base64code(node,order)+'.png')

    zipped = zip(nodes,qrcodes)

    context = {
        'lastconntime':lastconntime,
        'flow_text':flow_text,
        'order_date':order_date,
        'order_deaddate':order_deaddate,
        'remaining_time':remaining_time,
        'remaining_per':remaining_per,
        'plan_try':plan_try,
        'try_rest_transfer_per':try_rest_transfer_per,
        'rest_flow_text':rest_flow_text,

        'sspwd':sspwd,
        'port':port,
        'method':method,

        'zipped':zipped,
    }
    return render(request, "dashboard/index.html", context)




class SettingView(View):
    def get(self, request):
        method_list = [
            'rc4-md5',
            'aes-256-cfb',
            'aes-192-cfb',
            'aes-128-cfb',
            'chacha20',
        ]
        order = Order.objects.get(user=request.user)
        order_method = order.method
        order_sspwd = order.sspwd

        context = {
            'method_list': method_list,
            'order_method': order_method,
            'order_sspwd': order_sspwd,
        }

        return render(request, "dashboard/setting.html", context)


class SspwdView(View):
    def get(self, request):
        return redirect('/accounts/profile/setting')
    def post(self,request):
        order = Order.objects.get(user=request.user)
        order.sspwd = request.POST['newsspwd']
        order.save()
        return redirect('/accounts/profile/setting')

class MethodView(View):

    def get(self, request):
        return redirect('/accounts/profile/setting')
    def post(self,request):
        try:
            order = Order.objects.get(user=request.user)
            order.method = request.POST['group1']
            order.save()
            return redirect('/accounts/profile/setting')
        except:
            return redirect('/accounts/profile/setting')

def Orders(request):
    history_orders = History_order.objects.filter(user=request.user)

    status_list = []
    for ho in history_orders:
        if ho.status() == 1:
            status_list.append("正在生效")
        elif ho.status() == 0:
            status_list.append("未生效")
        elif ho.status() == -1:
            status_list.append("已失效")

    plan_list = []
    price_list = []
    for ho in history_orders:
        if ho.plan == 'T':
            plan_list.append('试用')
            price_list.append('0')
        elif ho.plan == 'M':
            plan_list.append('月')
            price_list.append('9.8')
        elif ho.plan == 'Y':
            plan_list.append('年')
            price_list.append('88.8')
        

    zipped = zip(plan_list, history_orders, status_list, price_list)
    context = {
        'zipped':zipped,
    }
    return render(request, "dashboard/orders.html", context)

def Notices(request):
    notices = Notice.objects.order_by('-pub_date')
    return render(request, "dashboard/notice.html", {'notices':notices})

class FeedbackView(View):
    def get(self, request):
        questions = request.user.question_set.all()
        context = {
            'questions':questions
        }
        return render(request, "dashboard/feedback.html", context)
    def post(self, request):
        q = request.user.question_set.create(question_text=request.POST['question'],pub_date=timezone.now())
        q.save()
        return redirect('/accounts/profile/feedback')



def Zipdownload(request):
    order = Order.objects.get(user=request.user)
    nodes = Node.objects.all()
    data, txt = json_config(order, nodes)
    resp = client_make(data, txt, request.user)
    return resp
