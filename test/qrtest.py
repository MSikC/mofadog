# -*- coding:utf-8 -*-
import chardet
import codecs
import qrcode
import base64
import sys


class Qrtest:
    def base64code_test(self,base64_str):

        encodestr = base64.b64encode(base64_str)
        #print type(encodestr)
        #print type(encodestr.decode())
        return encodestr.decode()
    def qr_create_test(self):

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=7,   #这里可以设置生成二维码的大小，数字越大生成的二维码越大
            border=4,
        )
        #node.Remark
        a = u'美国节点'

        uri = self.base64code_test('aes-256-cfb:12345@138.128.194.77:5003')
        #remark = self.base64code_test(a)
        shareqrcode_str = 'ss://' + uri + '#' + 'america'
        #print type(shareqrcode_str)
        filename = uri + '.png'

        qr.add_data(shareqrcode_str)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(filename)

if __name__ =='__main__':
    test = Qrtest()
    test.qr_create_test()