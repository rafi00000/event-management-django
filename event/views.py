from django.shortcuts import render, redirect
from django.http import HttpResponse
from event.forms import CreateEventForm, AddCategory, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from event.models import Event
from datetime import date, datetime
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.views.generic import DetailView, CreateView, View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator




# Create your views here.

class HomeView(View):
    def get(self, request):
        query = request.GET.get('q', 'new')
        if query == 'new':
            search_event = Event.objects.select_related("category").all()
        else:
            search_event = Event.objects.select_related("category").filter(name__icontains=query)

        context = {
            "search_event": search_event,
        }
        return render(request, "home.html", context)


@method_decorator(login_required, name='dispatch')
class OrganizerDashboardView(View):
    def get(self, request):
        today = date.today()
        q = request.GET.get("q")

        if q == "total_event":
            today_events = Event.objects.select_related("category")
        elif q == "upcoming_event":
            today_events = Event.objects.select_related("category").filter(date__gt=today)
        elif q == "past_event":
            today_events = Event.objects.select_related("category").filter(date__lt=today)
        else:
            today_events = Event.objects.select_related("category").filter(date=today)

        context = {
            "total_events": Event.objects.count(),
            "upcoming_events": Event.objects.filter(date__gt=today).count(),
            "past_events": Event.objects.filter(date__lt=today).count(),
            "today_events": today_events
        }
        return render(request, "dashboards/organizer_dashboard.html", context)


@method_decorator(login_required, name='dispatch')
class CreateEventView(CreateView):
    model = Event
    form_class = CreateEventForm
    template_name = "create-event.html"
    success_url = reverse_lazy("create-event")

    def form_valid(self, form):
        messages.success(self.request, "Event created Successfully")
        return super().form_valid(form)


@login_required
def update_task(request, id):
    event = Event.objects.get(id=id)
    event_form = CreateEventForm(instance=event)
    if request.method == "POST":
        event_form = CreateEventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated")
            return redirect("home-page")
    context = {
        "event_form": event_form
    }
    return render(request, "create-event.html", context)

@login_required
def delete_task(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event Deleted Successfully")
        return redirect("home-page")

@method_decorator(login_required, name='dispatch')
class AddCategoryView(View):
    def get(self, request):
        form = AddCategory()
        return render(request, "addCategory.html", {"category_form": form})

    def post(self, request):
        form = AddCategory(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added")
            return redirect("add-category")
        return render(request, "addCategory.html", {"category_form": form})


class EventDetailView(DetailView):
    model = Event
    template_name = "event-detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        total_participants = event.participants.all()
        context["total_participants"] = total_participants
        return context
        
@login_required
def rsvp_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user not in event.participants.all():
        event.participants.add(request.user)
        messages.success(request, "You have RSVP'd to this event")
    else:
        messages.warning(request, "You have already RSVP'd to this event")
    return redirect("home-page")

@login_required
def participant_dashboard(request):
    if request.user:
        participant_events = request.user.events.all()
    else:
        participant_events = []
    context = {
        "events": participant_events
    }
    return render(request, "dashboards/participant-dashboard.html", context)

@login_required
def admin_dashboard(request):
    users = User.objects.all()
    context = {
        "users": users
    }
    return render(request, "dashboards/admin-dashboard.html", context)

@login_required
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, "Role assigned successfully")
            return redirect("admin-dashboard")
    return render(request, "dashboards/assign_role.html", {"form": form})

@login_required
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} created successfully")
            return redirect("create-group")
    return render(request, "dashboards/create_group.html", {"form": form})

@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, "dashboards/group_list.html", {"groups": groups})


def all_events(request):
    events = Event.objects.all()
    context = {
        "today_events": events
    }
    return render(request, "data_temp/all_events.html", context)

@login_required
def remove_participant_from_event(request, event_id, user_id):
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=user_id)
    event.participants.remove(user)
    messages.success(request, "Participant removed successfully")
    return redirect("event-detail", id=event_id)

@login_required
def remove_group(request, group_name):
    group = Group.objects.get(name=group_name)
    group.delete()
    messages.success(request, f"Group {group_name} removed successfully")
    return redirect("group-list")


@login_required
def role_based_dashboard(request):
    if request.user.groups.filter(name='Organizer').exists():
        return redirect('organizer-dashboard')
    elif request.user.groups.filter(name='Participant').exists():
        return redirect('participant-dashboard')
    elif request.user.groups.filter(name='Admin').exists():
        return redirect('admin-dashboard')
    else:
        messages.error(request, "You do not have access to any dashboard")
        return redirect('home-page')