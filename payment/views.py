# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from dashboard.models import Order, Node
from django.views.generic import View
from datetime import datetime, timedelta
import random
import string
import time
from .models import History_order, Activation_code, Pay
from .qrcodetest import Qr_base64
import os
import commands
from django.utils import timezone
from django.contrib.auth.models import User
from . import payconfig
import hashlib

# Create your views here.
def get_b(num,mod):
    if mod == 'M':
        return num*1024*1024
    elif mod == 'G':
        return num*1024*1024*1024

def money_plan(var):
    m_p_d = {
        100:'T',
        980:'M',
        8880:'Y'
    }
    p_m_d = {
        'T':100,
        'M':980,
        'Y':8880
    }
    try:
        int(var)
        return m_p_d[var]
    except:
        return p_m_d[var]



def generate_verification_code():
    myslice = random.sample(string.ascii_letters + string.digits, 6)
    verification_code = ''.join(myslice) # list to string
    # print code_list
    # print type(myslice)
    return verification_code

def generate_activation_code():
    activation_code = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    return activation_code


def firewall_open_port(port):
    os.system('firewall-cmd --permanent --add-port=%s/tcp'%str(port))
    os.system('firewall-cmd --reload')
    (status, output) = commands.getstatusoutput('firewall-cmd --list-port')
    return output

def get_avail_port():
    firewall_port = range(20001, 25000)
    order_ports = []
    for order in Order.objects.all():
        order_ports.append(order.port)
    avail_ports = list(set(set(firewall_port).difference(set(order_ports))))
    avail_port = avail_ports[0]
    return avail_port

def get_or_generate_order(user, **kwargs):
    '''
    kwarg = {
        'plan_id':'T',

    }
    '''

    plan_id = kwargs['plan_id']
    plan_d = {
        "T": timedelta(hours=3),
        "M": timedelta(days=31),
        "Y": timedelta(days=380),
    }
    now = timezone.now()
    order, created = Order.objects.get_or_create(user=user)
    #Generating Test order or nottest order in the first place.
    #created return Ture.
    if created:
        order.port = get_avail_port()
        order.sspwd = generate_verification_code()
        order.method = 'chacha20'
        order.order_date = now
        order.valid_date = order.order_date


    else:
        dead_date = order.dead_date

        if now > dead_date:
            order.valid_date = now
        else:
            order.valid_date = order.dead_date

        order.order_date = now
    order.plan = plan_id
    order.dead_date = order.valid_date + plan_d[plan_id]
    #order.flow_down = 0
    #order.flow_up = 0
    order.transfer = get_b(500,'G')
    order.enable = True
    order.save()

    user.history_order_set.create(plan=plan_id, order_date=order.order_date, valid_date=order.valid_date, dead_date=order.dead_date)

    generate_qrcode(user)




class PaymentView(View):
    def get(self, request, plan_id):
        try_is_valid = True
        if request.user.is_anonymous():
            return redirect('/accounts/login')


        return render(request, "payment/index.html", {"plan_id":plan_id})

    def post(self, request, plan_id):
        plan_d = {
            "T": timedelta(hours=3),
            "M": timedelta(days=31),
            "Y": timedelta(days=380),
        }

        if request.user.is_anonymous():
            return redirect('/accounts/login')


        if request.POST['testpassword'] == 'try':
            if request.user.order_set.count() == 0:
                get_or_generate_order(request.user, plan_id='T')
                return redirect('/accounts/profile/')
            elif History_order.objects.filter(user=request.user, plan='T').count() == 0:
                now = timezone.now()
                order = Order.objects.get(user=request.user)
                if now <= order.dead_date:
                    return render(request, "payment/try_invalid_during_activations.html")
                else:
                    get_or_generate_order(request.user, plan_id='T')
                    return redirect('/accounts/profile/')
            else:

                try_is_invalid = True
                return render(request, "payment/index.html", {"try_is_invalid":try_is_invalid})

        else:#in datebase
            post_acode = request.POST['testpassword']
            try:
                acode = Activation_code.objects.get(activation_code=post_acode)
            except:
                return render(request, "payment/acode_not_exists.html")

            if acode.enable == False:
                return render(request, "payment/acode_is_disable.html")

            acode.user = request.user.username
            acode.activate_time_stamp = int(time.time())
            acode.enable = False
            acode.save()


            plan_id = acode.plan
            get_or_generate_order(request.user, plan_id=plan_id)


            return redirect('/accounts/profile/')


def generate_qrcode(user):
    order = Order.objects.get(user=user)
    tosavepath = '/root/myproject/mysite/static/qrcode/' + order.user.email
    qr_base64 = Qr_base64(order, tosavepath)
    try:
        os.mkdir(tosavepath)
    except:
        pass
    for node in Node.objects.all():
        qr_base64.qr_create(node)

def Qrcoderenew(request):
    generate_qrcode(request.user)
    return redirect('/accounts/profile/')


class Paymentnotify(View):
    def get(self, request):
        raise Http404("404 not found")
    @csrf_exempt
    def post(self, request):

        payChannel = request.POST['payChannel']#String返回支付通道代码
        Money = request.POST['Money']#Int用户付款金额（单位分）
        orderNumber = request.POST['orderNumber']#String商户自主生成的订单号
        attachData = request.POST['attachData']#String商户自定义附加数据
        callbackSign = request.POST['callbackSign']#String回调签名查看算法1.Money 2.attachData 3.orderNumber 4.payChannel 5.payKey

        payorder = Pay.objects.get(orderNumber=orderNumber)
        stringSignTemp = str(payorder.money) + payorder.username + payorder.orderNumber + payorder.payChannel + payconfig.payKey
        m = hashlib.md5()
        m.update(stringSignTemp)
        paymodelSign = m.hexdigest()

        if callbackSign == paymodelSign:
            #checkdouplepay

            if payorder.payconfirm == False:
                get_or_generate_order(User.objects.get(username=attachData), plan_id=money_plan(Money))
                payorder.payconfirm = True
                payorder.save()
            else:
                pass




            #    pass
            #else
            #

            return HttpResponse("SUCCESS")

@csrf_exempt
def Paymentreturn(request):
    return HttpResponseRedirect(reverse('payment:paymentreturn'))

def Return_url_handler(request):
    return render(request, "payment/return.html")

def Apipay(request, plan_id):
    odnend_4 = str(random.randint(1000, 9999))
    dt = datetime.now()
    orderNumber = dt.strftime("%Y%m%d%H%M%S%f") + odnend_4


    payChannel = 'qqpay'
    Subject = plan_id
    Money = money_plan(plan_id)
    attachData = request.user.username

    Pay.objects.create(orderNumber=orderNumber, money=Money, username=attachData, payconfirm=False, payChannel=payChannel)

    stringSignTemp = str(Money) + payconfig.Notify_url + payconfig.Return_url + Subject + attachData + orderNumber + payChannel + str(payconfig.payId) + payconfig.payKey
    # String	是	45	MD5签名 查看算法	5879063c6a8592ada2e96525aad347c0
    m = hashlib.md5()
    m.update(stringSignTemp)
    Sign = m.hexdigest()

    context = {
        'payId': payconfig.payId,
        'payChannel': payChannel,#
        'Subject': Subject,
        'Money': Money,
        'orderNumber': orderNumber,
        'attachData': attachData,
        'Notify_url': payconfig.Notify_url,
        'Return_url': payconfig.Return_url,
        'Sign': Sign
    }
    return render(request, "payment/apipay.html", context)








