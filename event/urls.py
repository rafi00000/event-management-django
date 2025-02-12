from django.urls import path
from django.http import HttpResponse
from event.views import home

urlpatterns = [
    path("",  home)
]
