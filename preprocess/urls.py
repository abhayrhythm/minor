
from django.conf.urls import url
from django.contrib import admin
from preprocess import views

app_name = 'preprocess'

urlpatterns = [
    url(r'^$',views.process,name='process'),
]
