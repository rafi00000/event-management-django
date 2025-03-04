from django.urls import path
from django.http import HttpResponse
from event.views import organizer_dashboard, home, create_task, addParticipant, addCategory, update_task, delete_task, event_detail

urlpatterns = [
    path("",  home, name="home-page"),
    path("organizer-dashboard/",  organizer_dashboard, name="organizer-dashboard"),
    path("create-event/", create_task, name="create-event"),
    path("add-participant/", addParticipant, name="add-participant"),
    path("event-detail/<int:id>", event_detail, name="event-detail"),
    path("add-category/", addCategory, name="add-category"),
    path("update-task/<int:id>", update_task, name="update-task"),
    path("delete-task/<int:id>", delete_task, name="delete-task")
]
