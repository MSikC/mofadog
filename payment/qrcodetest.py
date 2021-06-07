# -*- coding:utf-8 -*-
import qrcode
import base64
from dashboard.models import Node, Order


class Qr_base64:
    def __init__(self, order, to_save_path):

        self.order = order
        self.to_save_path = to_save_path

    def base64code(self, node):
        base64_str = self.order.method + ':' + self.order.sspwd + '@' + node.domain_name + ':' + str(self.order.port)
        encodestr = base64.b64encode(base64_str)
        return encodestr.decode()

    def qr_create(self, node):

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=7,   #这里可以设置生成二维码的大小，数字越大生成的二维码越大
            border=4,
        )
        #node.Remark
        shareqrcode_str = 'ss://' + self.base64code(node)
        filename = self.to_save_path + '/' + self.base64code(node) + '.png'

        qr.add_data(shareqrcode_str)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(filename)

