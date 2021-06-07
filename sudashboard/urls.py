from django.conf.urls import url
from . import views

app_name = 'sudashboard'
urlpatterns = [
    url(r'^(?P<page_id>[A-Z])/$', views.Url_redirect, name='url_redierct'),
    url(r'^generate_activations_code/$', views.Activations, name='Activations'),
    url(r'^create_json/$', views.Create_json, name='Create_json'),
    url(r'^(?P<y_id>[0-9]{4})/(?P<m_id>[0-9]+)/(?P<d_id>[0-9]+)/I/$', views.Httpdlog, name='httpdlog'),
    url(r'^(?P<y_id>[0-9]{4})/(?P<m_id>[0-9]+)/(?P<d_id>[0-9]+)/F/$', views.Flow_overview, name='flow_overview'),
    url(r'^(?P<y_id>[0-9]{4})/(?P<m_id>[0-9]+)/(?P<d_id>[0-9]+)/A/$', views.Acode_overview, name='acode_overview'),
    url(r'^(?P<y_id>[0-9]{4})/(?P<m_id>[0-9]+)/(?P<d_id>[0-9]+)/O/$', views.Order_overview, name='order_overview'),


]