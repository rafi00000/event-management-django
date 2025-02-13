from django.urls import path
from django.http import HttpResponse
from event.views import organizer_dashboard

urlpatterns = [
    path("",  organizer_dashboard, name="organizer-dashboard")
]
