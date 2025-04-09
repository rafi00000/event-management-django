from django.urls import path
from django.http import HttpResponse
from event.views import organizer_dashboard, home, create_task, addCategory, update_task, delete_task, rsvp_event, participant_dashboard, admin_dashboard, assign_role, create_group, group_list
from event.views import all_events, remove_participant_from_event, remove_group, role_based_dashboard, EventDetailView

urlpatterns = [
    path("organizer-dashboard/",  organizer_dashboard, name="organizer-dashboard"),
     path("create-event/", CreateEventView.as_view(), name="create-event"),
    path("add-category/", AddCategoryView.as_view(), name="add-category"),
    path("event-detail/<int:pk>", EventDetailView.as_view(), name="event-detail"),
    path("update-task/<int:id>", update_task, name="update-task"),
    path("delete-task/<int:id>", delete_task, name="delete-task"),
    path('rsvp/<int:event_id>/', rsvp_event, name='rsvp_event'),
    path("participant-dashboard/", participant_dashboard, name="participant-dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin/<int:user_id>/assign-role/", assign_role, name="assign-role"),
    path("admin/create-group/", create_group, name="create-group"),
    path("admin/group-list/", group_list, name="group-list"),
    path("all-events/", all_events, name="all-events"),
    path("remove-participant/<int:event_id>/<int:user_id>/", remove_participant_from_event, name="remove-participant"),
    path("remove-group/<str:group_name>/", remove_group, name="remove-group"),
    path("dashboard/", role_based_dashboard, name="role-based-dashboard"),

]
