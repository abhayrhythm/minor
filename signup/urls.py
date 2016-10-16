
from django.conf.urls import url, include
from django.contrib import admin
from signup import views


app_name = 'signup'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^success/$',views.success,name='success'),
    url(r'^loginsuccess/$',views.loginsuccess,name='loginsuccess'),
    url(r'^process/',include('preprocess.urls'),name='process'),
]
