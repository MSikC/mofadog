from django.conf.urls import url
from . import views
from django.http import HttpResponse


#app_name = 'pages'
urlpatterns = [
    url(r'^$', views.Home, name="index"),

    #url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/register/$', views.RegistrationViewUniqueEmail.as_view(),name='registration_register'),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *<br>Disallow: /"))
]
