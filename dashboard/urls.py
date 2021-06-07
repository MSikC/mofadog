from django.conf.urls import url
from . import views


app_name = 'dashboard'
urlpatterns = [
    url(r'^$', views.Home, name="index"),

    url(r'^setting/$', views.SettingView.as_view(), name="setting"),
    url(r'^setting/sspwd/$', views.SspwdView.as_view(), name="sspwd"),
    url(r'^setting/method/$', views.MethodView.as_view(), name="method"),
    url(r'^orders/$', views.Orders, name="orders"),
    url(r'^notice/$', views.Notices, name="notice"),
    url(r'^feedback/$', views.FeedbackView.as_view(), name="feedback"),
    url(r'^zipdownload/$', views.Zipdownload, name="zipdownload"),



]