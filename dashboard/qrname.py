# -*- coding:utf-8 -*-
import qrcode
import base64
from dashboard.models import Node, Order

def base64code(node, order):
    base64_str = order.method + ':' + order.sspwd + '@' + node.domain_name + ':' + str(order.port)
    encodestr = base64.b64encode(base64_str)
    return encodestr.decode()