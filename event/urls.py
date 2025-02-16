from django.urls import path
from django.http import HttpResponse
from event.views import organizer_dashboard, home

urlpatterns = [
    path("",  home, name="home-page"),
    path("organizer-dashboard/",  organizer_dashboard, name="organizer-dashboard"),
]
