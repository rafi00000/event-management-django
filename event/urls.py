from django.urls import path
from django.http import HttpResponse
from event.views import organizer_dashboard, home, create_task, addParticipant, addCategory

urlpatterns = [
    path("",  home, name="home-page"),
    path("organizer-dashboard/",  organizer_dashboard, name="organizer-dashboard"),
    path("create-event/", create_task, name="create-event"),
    path("add-participant/", addParticipant, name="add-participant"),
    path("add-category/", addCategory, name="add-category")
]
