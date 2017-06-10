from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.greeting),
    url(r'^morning/$', views.morning_greeting),
    url(r'^evening/$', views.evening_greeting),
]

