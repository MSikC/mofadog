from django.conf.urls import url
from . import views


app_name = 'payment'
urlpatterns = [
    url(r'^(?P<plan_id>[TMY])/$', views.PaymentView.as_view(), name='payment'),
    url(r'^qrcoderenew/$', views.Qrcoderenew, name='qrcoderenew'),
    url(r'^notify/$', views.Paymentnotify.as_view(), name='paymentnotify'),
    url(r'^apipay/(?P<plan_id>[TMY])/$', views.Apipay, name='apipay'),
    url(r'^return/$', views.Return_url_handler, name='paymentreturn')

]